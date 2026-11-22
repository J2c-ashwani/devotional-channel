#!/usr/bin/env python3
"""
Publish Mahabharata Episode 1 to Instagram Reels and Facebook Page
using the already uploaded video in GCS:
reels/1795371694_Itihasa_Saga_Mahabharata_Ep01_Hindi_FINAL.mp4
"""

import os
import sys
import time
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path
from google.cloud import storage

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
sys.path.insert(0, str(BASE_DIR))

# Load .env.local
env = {}
with open(BASE_DIR / ".env.local") as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k] = v

access_token = env.get("META_PERMANENT_ACCESS_TOKEN")
ig_account_id = env.get("INSTAGRAM_ACCOUNT_ID")
fb_page_id = env.get("FACEBOOK_PAGE_ID")
gcs_bucket_name = "itihasa-saga-storage-514907"
blob_name = "reels/1795371694_Itihasa_Saga_Mahabharata_Ep01_Hindi_FINAL.mp4"

caption = (
    "जब शांतनु ने तोड़ा देवी गंगा का वचन! ⚡🌊 | महाभारत भाग 1\n\n"
    "हस्तिनापुर नरेश राजा शांतनु और देवी गंगा का वह अलौकिक वचन, जिसने पूरे महाभारत की नींव रखी! 🌊\n"
    "जब गंगा ने अपने सात पुत्रों को नदी में बहा दिया, शांतनु मौन रहे। लेकिन आठवें पुत्र के जन्म पर जब राजा ने वचन तोड़कर गंगा को रोका... तब जन्मा वह महायोद्धा, जिसे संसार 'भीष्म' के नाम से जानेगा!\n\n"
    "🔔 महाभारत • भाग 2 (देवव्रत की 'भीष्म प्रतिज्ञा') देखने के लिए फॉलो करें: @itihasasaga\n\n"
    "#mahabharata #bhishma #ganga #shantanu #itihasasaga #sanatandharma #shorts #reels #viralshorts #hindumythology"
)

# 1. Generate high-speed signed URL
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(BASE_DIR / "service-account.json")
gcs_client = storage.Client(project=env.get("GOOGLE_CLOUD_PROJECT", "devotional-youtube-514907"))
bucket = gcs_client.bucket(gcs_bucket_name)
blob = bucket.blob(blob_name)
signed_url = blob.generate_signed_url(expiration=datetime.timedelta(hours=4), method="GET")
print("✅ Signed URL generated from GCS:")
print(signed_url[:80] + "...")

# 2. Publish to Instagram Reels
print("\n" + "="*60)
print("📸 1. PUBLISHING TO INSTAGRAM REELS (@itihasasaga)...")
print("="*60)

create_url = f"https://graph.facebook.com/v19.0/{ig_account_id}/media"
params = urllib.parse.urlencode({
    "media_type": "REELS",
    "video_url": signed_url,
    "caption": caption,
    "share_to_feed": "true",
    "access_token": access_token
}).encode("utf-8")

req = urllib.request.Request(create_url, data=params, method="POST")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    creation_id = data.get("id")
    print(f"✅ Instagram Container created with ID: {creation_id}")

print("⏳ Waiting for Instagram to process video...")
for attempt in range(30):
    time.sleep(5)
    status_url = f"https://graph.facebook.com/v19.0/{creation_id}?fields=status_code&access_token={access_token}"
    with urllib.request.urlopen(status_url) as resp:
        status_data = json.loads(resp.read().decode())
        code = status_data.get("status_code")
        print(f"Status: {code} ({attempt*5}s)")
        if code == "FINISHED":
            break
        elif code == "ERROR":
            raise RuntimeError(f"Instagram video processing failed: {status_data}")

publish_url = f"https://graph.facebook.com/v19.0/{ig_account_id}/media_publish"
pub_params = urllib.parse.urlencode({
    "creation_id": creation_id,
    "access_token": access_token
}).encode("utf-8")

pub_req = urllib.request.Request(publish_url, data=pub_params, method="POST")
with urllib.request.urlopen(pub_req) as resp:
    pub_data = json.loads(resp.read().decode())
    ig_media_id = pub_data.get("id")
    print("\n" + "="*60)
    print(f"🎉 SUCCESS! Instagram Reel Published!")
    print(f"Instagram Media ID: {ig_media_id}")
    print("="*60)

# 3. Publish to Facebook Page
print("\n" + "="*60)
print("📘 2. PUBLISHING TO FACEBOOK PAGE (Itihasa Saga)...")
print("="*60)

fb_url = f"https://graph.facebook.com/v19.0/{fb_page_id}/videos"
fb_params = urllib.parse.urlencode({
    "file_url": signed_url,
    "description": caption,
    "title": "जब शांतनु ने तोड़ा देवी गंगा का वचन! ⚡🌊 | महाभारत भाग 1",
    "access_token": access_token
}).encode("utf-8")

fb_req = urllib.request.Request(fb_url, data=fb_params, method="POST")
with urllib.request.urlopen(fb_req) as resp:
    fb_data = json.loads(resp.read().decode())
    fb_vid_id = fb_data.get("id")
    print("\n" + "="*60)
    print(f"🎉 SUCCESS! Facebook Video Published!")
    print(f"Facebook Video ID: {fb_vid_id}")
    print("="*60)

print("\n🚀 ALL PLATFORMS PUBLISHED SUCCESSFULLY!")
