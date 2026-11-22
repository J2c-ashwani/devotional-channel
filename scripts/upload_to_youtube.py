#!/usr/bin/env python3
"""
Direct YouTube Shorts Uploader for Itihasa Saga (@itihasasaga).
Uploads any episode (Ramayana, Mahabharata, etc.) to YouTube with optimal metadata, tags, and category.
Includes robust socket timeouts and automatic chunk resume retry.
"""

import sys
import time
import socket
import ssl
import argparse
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Ensure 120s socket timeout for high-resolution video chunk uploads
socket.setdefaulttimeout(120.0)

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

EPISODES = {
    "english": {
        "video": Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ep01_English_FINAL.mp4"),
        "title": "When Lord Rama Broke the Divine Pinaka Bow! 🏹⚡ | Ramayana Part 1 #shorts",
        "description": (
            "In the royal court of Mithila, 5,000 mighty warriors failed to even budge the celestial Pinaka bow of Lord Shiva. "
            "As King Janaka wept in despair, Sage Vishvamitra commanded young Prince Rama to rise. What happened next shook the three worlds!\n\n"
            "🔔 Subscribe to @itihasasaga for Part 2!\n\n"
            "#ramayana #lordrama #mithila #sitaswayamvar #itihasasaga #sanatandharma #shorts #reels #mythology"
        ),
        "tags": ["ramayana", "lord rama", "mithila", "sita swayamvar", "pinaka bow", "itihasa saga", "sanatan dharma", "shorts"],
    },
    "hindi": {
        "video": Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ep01_Hindi_FINAL.mp4"),
        "title": "जब श्री राम ने तोड़ा शिवजी का पिनाक धनुष! 🏹⚡ | रामायण भाग 1 #shorts",
        "description": (
            "मिथिला की राजसभा में रावण और बाणासुर सहित तीनों लोकों के महारथी भगवान शिव के पिनाक धनुष को हिला भी न सके। "
            "जब राजा जनक ने निराश होकर पूछा 'क्या यह पृथ्वी वीरों से शून्य हो गई है?', तब महर्षि विश्वामित्र ने श्री राम को आज्ञा दी। "
            "फिर जो हुआ, उसने तीनों लोकों को हिला दिया!\n\n"
            "🔔 भाग 2 देखने के लिए @itihasasaga को अभी सब्सक्राइब करें!\n\n"
            "#ramayana #shreeram #mithila #dhanushbhang #itihasasaga #sanatan #shorts #reels #viralshorts"
        ),
        "tags": ["रामायण", "श्री राम", "मिथिला", "धनुषभंग", "पिनाक", "इतिहास सागा", "sanatan", "shorts"],
    }
}

def upload_to_youtube(video_path: Path, title: str, description: str, tags: list, lang: str = "hi", privacy: str = "public"):
    if not settings.YOUTUBE_REFRESH_TOKEN or settings.YOUTUBE_REFRESH_TOKEN == "mock_refresh_token":
        print("❌ Error: YouTube is not authorized yet. Run scripts/connect_youtube.py first!")
        sys.exit(1)

    if not video_path.exists():
        print(f"❌ Video file missing: {video_path}")
        sys.exit(1)

    print(f"\n🎬 Uploading Video to YouTube (@itihasasaga)...")
    print(f"File: {video_path} ({video_path.stat().st_size / (1024*1024):.1f} MB)")
    print(f"Title: {title}")
    print(f"Privacy: {privacy}")

    creds = Credentials(
        token=None,
        refresh_token=settings.YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.YOUTUBE_CLIENT_ID,
        client_secret=settings.YOUTUBE_CLIENT_SECRET,
        scopes=SCOPES,
    )
    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "24",  # Entertainment
            "defaultLanguage": lang,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        }
    }

    # 1MB chunk size ensures reliable delivery even on variable latency connections
    media = MediaFileUpload(
        str(video_path),
        chunksize=1024 * 1024,
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print("⏳ Uploading chunks to YouTube...")
    response = None
    retry_count = 0
    max_retries = 10

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"Uploaded {pct}%...")
            retry_count = 0
        except (TimeoutError, ssl.SSLError, socket.timeout, Exception) as e:
            retry_count += 1
            if retry_count > max_retries:
                print(f"❌ Max retries ({max_retries}) exceeded during upload: {e}")
                raise e
            wait_time = min(30, retry_count * 5)
            print(f"⚠️ Network glitch/timeout ({e}). Auto-resuming in {wait_time}s (Attempt {retry_count}/{max_retries})...")
            time.sleep(wait_time)

    vid_id = response.get("id")
    url = f"https://youtube.com/shorts/{vid_id}"
    print("\n" + "="*60)
    print(f"🎉 SUCCESS! Video is LIVE on YouTube!")
    print(f"Video URL: {url}")
    print("="*60)
    return vid_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Shorts to YouTube")
    parser.add_argument("--video", type=str, default=None, help="Path to video file")
    parser.add_argument("--title", type=str, default=None, help="Video title")
    parser.add_argument("--description", type=str, default=None, help="Video description")
    parser.add_argument("--tags", type=str, default=None, help="Comma-separated tags")
    parser.add_argument("--lang", choices=["english", "hindi"], default="hindi")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="public")
    args = parser.parse_args()

    if args.video:
        video_path = Path(args.video)
        title = args.title or "Itihasa Saga #shorts"
        description = args.description or title
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else ["itihasa saga", "shorts"]
        upload_to_youtube(video_path, title, description, tags, lang="hi" if args.lang == "hindi" else "en", privacy=args.privacy)
    else:
        ep = EPISODES.get(args.lang.lower())
        if not ep:
            print(f"Unknown language: {args.lang}. Choose 'english' or 'hindi'.")
            sys.exit(1)
        upload_to_youtube(ep["video"], ep["title"], ep["description"], ep["tags"], lang="hi" if args.lang == "hindi" else "en", privacy=args.privacy)
