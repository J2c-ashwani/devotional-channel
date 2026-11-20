#!/usr/bin/env python3
"""
Meta Graph API Uploader for Itihasa Saga (@itihasasaga).
Publishes cinematic Reels to Instagram Business/Creator Account and Facebook Page
using the permanent, non-expiring Page Access Token and Google Cloud Storage Signed URLs.
"""

import os
import time
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path
from google.cloud import storage

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class MetaReelUploader:
    def __init__(self):
        # Load environment variables
        self.env = {}
        env_path = BASE_DIR / ".env.local"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        k, v = line.strip().split("=", 1)
                        self.env[k] = v

        self.access_token = self.env.get("META_PERMANENT_ACCESS_TOKEN")
        self.ig_account_id = self.env.get("INSTAGRAM_ACCOUNT_ID")
        self.fb_page_id = self.env.get("FACEBOOK_PAGE_ID")
        self.gcs_bucket_name = "itihasa-saga-storage-514907"

        # Initialize GCS client
        creds_file = self.env.get("GOOGLE_APPLICATION_CREDENTIALS", str(BASE_DIR / "service-account.json"))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_file
        self.gcs_client = storage.Client(project=self.env.get("GOOGLE_CLOUD_PROJECT", "devotional-youtube-514907"))

    def upload_to_gcs_and_get_url(self, local_video_path: Path) -> str:
        """Uploads video to GCS bucket and generates a 2-hour signed public URL for Meta to ingest"""
        bucket = self.gcs_client.bucket(self.gcs_bucket_name)
        blob_name = f"reels/{int(time.time())}_{local_video_path.name}"
        blob = bucket.blob(blob_name)
        
        print(f"☁️ Uploading {local_video_path.name} to Google Cloud Storage ({blob_name})...")
        blob.upload_from_filename(str(local_video_path), content_type="video/mp4")
        
        signed_url = blob.generate_signed_url(expiration=datetime.timedelta(hours=2), method="GET")
        print("✅ Generated high-speed Signed URL for Meta ingestion!")
        return signed_url

    def publish_instagram_reel(self, video_path: Path, caption: str) -> str:
        """Publishes a Reel to Instagram via official Instagram Graph API"""
        print(f"\n📸 Publishing to Instagram (@itihasasaga)...")
        video_url = self.upload_to_gcs_and_get_url(video_path)

        # 1. Create Media Container
        create_url = f"https://graph.facebook.com/v19.0/{self.ig_account_id}/media"
        params = urllib.parse.urlencode({
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": self.access_token
        }).encode("utf-8")

        req = urllib.request.Request(create_url, data=params, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            creation_id = data.get("id")
            print(f"Container created with ID: {creation_id}")

        # 2. Wait for Meta to download and process the video container
        print("⏳ Waiting for Instagram to process video...")
        for attempt in range(24):  # up to 2 minutes
            time.sleep(5)
            status_url = f"https://graph.facebook.com/v19.0/{creation_id}?fields=status_code&access_token={self.access_token}"
            with urllib.request.urlopen(status_url) as resp:
                status_data = json.loads(resp.read().decode())
                code = status_data.get("status_code")
                print(f"Status: {code} ({attempt*5}s)")
                if code == "FINISHED":
                    break
                elif code == "ERROR":
                    raise RuntimeError(f"Instagram video processing failed: {status_data}")

        # 3. Publish the container
        publish_url = f"https://graph.facebook.com/v19.0/{self.ig_account_id}/media_publish"
        pub_params = urllib.parse.urlencode({
            "creation_id": creation_id,
            "access_token": self.access_token
        }).encode("utf-8")

        pub_req = urllib.request.Request(publish_url, data=pub_params, method="POST")
        with urllib.request.urlopen(pub_req) as resp:
            pub_data = json.loads(resp.read().decode())
            media_id = pub_data.get("id")
            print(f"🎉 SUCCESS! Instagram Reel Published! Media ID: {media_id}")
            return media_id

    def publish_facebook_reel(self, video_path: Path, caption: str) -> str:
        """Publishes a Reel / Video to Facebook Page via Graph API"""
        print(f"\n📘 Publishing to Facebook Page (Itihasa Saga)...")
        video_url = self.upload_to_gcs_and_get_url(video_path)

        url = f"https://graph.facebook.com/v19.0/{self.fb_page_id}/videos"
        params = urllib.parse.urlencode({
            "file_url": video_url,
            "description": caption,
            "title": caption.split("\n")[0][:100],
            "access_token": self.access_token
        }).encode("utf-8")

        req = urllib.request.Request(url, data=params, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            vid_id = data.get("id")
            print(f"🎉 SUCCESS! Facebook Video Published! Video ID: {vid_id}")
            return vid_id
