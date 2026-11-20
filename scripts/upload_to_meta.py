#!/usr/bin/env python3
"""
CLI tool to publish videos to Instagram and Facebook for Itihasa Saga.
Usage:
  python3 scripts/upload_to_meta.py --target instagram --video path/to/video.mp4
  python3 scripts/upload_to_meta.py --target all --video path/to/video.mp4
"""

import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.modules.meta.uploader import MetaReelUploader

DEFAULT_CAPTION = (
    "जब श्री राम ने तोड़ा शिवजी का पिनाक धनुष! 🏹⚡ | रामायण भाग 1\n\n"
    "मिथिला की राजसभा में रावण और बाणासुर सहित तीनों लोकों के महारथी भगवान शिव के पिनाक धनुष को हिला भी न सके। "
    "जब राजा जनक ने निराश होकर पूछा 'क्या यह पृथ्वी वीरों से शून्य हो गई है?', तब महर्षि विश्वामित्र ने श्री राम को आज्ञा दी। "
    "फिर जो हुआ, उसने तीनों लोकों को हिला दिया!\n\n"
    "🔔 भाग 2 देखने के लिए फॉलो करें: @itihasasaga\n\n"
    "#ramayana #shreeram #mithila #dhanushbhang #itihasasaga #sanatan #shorts #reels #viralshorts"
)

def main():
    parser = argparse.ArgumentParser(description="Upload Reels to Instagram and Facebook")
    parser.add_argument("--target", choices=["instagram", "facebook", "all"], default="all")
    parser.add_argument("--video", type=str, default="/Users/ashwanikumar/Downloads/Itihasa_Saga_Ep01_Hindi_FINAL.mp4")
    parser.add_argument("--caption", type=str, default=DEFAULT_CAPTION)
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        print(f"❌ Video not found: {video_path}")
        sys.exit(1)

    uploader = MetaReelUploader()
    if args.target in ["instagram", "all"]:
        uploader.publish_instagram_reel(video_path, args.caption)
    if args.target in ["facebook", "all"]:
        uploader.publish_facebook_reel(video_path, args.caption)

if __name__ == "__main__":
    main()
