#!/usr/bin/env python3
"""
Single-Shot Live Multi-Platform Publisher for Ramayana Episode 3 (ramayana_ep03).
Publishes the verified 1080p Vertex Text-to-Video Master to:
  1. YouTube Shorts (Public Immediate)
  2. Instagram Reels (@itihasasaga)
  3. Facebook Page (Itihasa Saga)
Verifies all 3 IDs and records completion in EpisodicLedger + OriginalityGuard.
"""

import json
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.upload_to_youtube import upload_to_youtube
from backend.app.modules.meta.uploader import MetaReelUploader
from backend.app.modules.mythology.episodic_ledger import EpisodicLedger
from backend.app.modules.scriptwriting.originality_guard import OriginalityGuard
from backend.app.agents.social_media_manager_agent import SocialMediaManagerAgent

EPISODE_ID = "ramayana_ep03"
REVIEW_VIDEO = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep03_Hindi_REVIEW.mp4")
FINAL_VIDEO = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep03_Hindi_FINAL.mp4")

TITLE = "श्री राम और माता सीता का दिव्य विवाह! 🌺💍 | रामायण भाग 3 #shorts"
DESCRIPTION = (
    "परशुराम जी के प्रस्थान के बाद राजा जनक ने अयोध्या निमंत्रण भेजा, और महाराज दशरथ भव्य बारात लेकर मिथिला पधारे! "
    "महर्षि विश्वामित्र के आशीर्वाद से शुभ मुहूर्त में माता सीता और प्रभु श्री राम का दिव्य विवाह संपन्न हुआ।\n\n"
    "पावन अग्नि के समक्ष लिए गए अमर वचनों और भावुक विदाई के बाद जब श्री राम-सीता अयोध्या लौटे, तो पूरी नगरी दीपों से जगमगा उठी... "
    "पर कल के राज्याभिषेक से पहले ही नियति कौन-सा महाषड्यंत्र रचने वाली थी?\n\n"
    "🔔 भाग 4 देखने के लिए @itihasasaga को अभी सब्सक्राइब और फॉलो करें!\n\n"
    "📜 प्रामाणिक स्रोत: वाल्मीकि रामायण (बालकाण्ड सर्ग 71-77)\n\n"
    "#ramayana #shreeram #sitaramvivah #matasita #mithila #ayodhya #itihasasaga #sanatandharma #shorts #reels #viralshorts"
)
TAGS = [
    "रामायण", "श्री राम विवाह", "सीता स्वयंवर", "माता सीता", "मिथिला", "अयोध्या",
    "ramayana", "sita ram vivah", "itihasa saga", "sanatan dharma", "shorts"
]


def main():
    if EpisodicLedger.is_completed(EPISODE_ID):
        print(f"❌ Single-Shot Duplicate Guard: '{EPISODE_ID}' is already marked completed. Aborting duplicate publish!")
        sys.exit(1)

    if not REVIEW_VIDEO.exists():
        print(f"❌ Missing verified review master: {REVIEW_VIDEO}")
        sys.exit(1)

    shutil.copy2(REVIEW_VIDEO, FINAL_VIDEO)
    print(f"✅ Staged Final Master: {FINAL_VIDEO} ({FINAL_VIDEO.stat().st_size / (1024*1024):.2f} MB)")

    # 1. YouTube Shorts Immediate Public Publish
    yt_id = upload_to_youtube(FINAL_VIDEO, TITLE, DESCRIPTION, TAGS, lang="hi", privacy="public")
    yt_res = {"success": bool(yt_id), "youtube_video_id": yt_id, "url": f"https://youtube.com/shorts/{yt_id}"}

    # 2. Instagram Reels + Facebook Page Immediate Publish
    meta = MetaReelUploader()
    caption = f"{TITLE}\n\n{DESCRIPTION}"
    ig_id = meta.publish_instagram_reel(FINAL_VIDEO, caption)
    fb_id = meta.publish_facebook_reel(FINAL_VIDEO, caption)
    meta_res = {"instagram_media_id": ig_id, "facebook_video_id": fb_id}

    # 3. Social Media Manager Audit & Ledger Certification
    smm = SocialMediaManagerAgent()
    audit = smm.verify_publication_status(EPISODE_ID, yt_res, meta_res)
    if audit.get("certified_published"):
        EpisodicLedger.mark_completed(EPISODE_ID)
        OriginalityGuard.save_script_to_history(
            script_id=EPISODE_ID,
            title_hindi="श्री राम और माता सीता का दिव्य विवाह: जनकपुरी में आनंदोत्सव और अयोध्या आगमन",
            hook_hindi="परशुराम जी के जाने के बाद, राजा जनक ने अयोध्या निमंत्रण भेजा—और भव्य बारात लेकर मिथिला पधारे महाराज दशरथ!",
            full_script=DESCRIPTION
        )

    print("\n=== MULTI-PLATFORM PUBLISH RECEIPT ===")
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    if not audit.get("certified_published"):
        sys.exit(1)


if __name__ == "__main__":
    main()
