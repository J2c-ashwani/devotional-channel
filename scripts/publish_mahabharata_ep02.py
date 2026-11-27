#!/usr/bin/env python3
"""
Single-Shot Live Multi-Platform Publisher for Mahabharata Episode 2 (mahabharata_ep02).
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

EPISODE_ID = "mahabharata_ep02"
REVIEW_VIDEO = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Mahabharata_Ep02_Hindi_REVIEW.mp4")
FINAL_VIDEO = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Mahabharata_Ep02_Hindi_FINAL.mp4")

TITLE = "देवव्रत की भीषण 'भीष्म प्रतिज्ञा'! 🙏🔥 | महाभारत भाग 2 #shorts"
DESCRIPTION = (
    "वर्षों बाद देवी गंगा ने महाराज शांतनु को महावीर पुत्र देवव्रत लौटाया। पर जब शांतनु सत्यवती के विवाह हेतु व्याकुल हुए, "
    "तो निषादराज ने शर्त रखी कि सत्यवती का पुत्र ही हस्तिनापुर का सम्राट बने!\n\n"
    "पिता के सुख के लिए युवराज देवव्रत ने न केवल हस्तिनापुर के राजसिंहासन का त्याग किया, बल्कि आजीवन अखंड ब्रह्मचर्य की "
    "महाभीषण 'भीष्म प्रतिज्ञा' ली—जिस पर आकाश से देवताओं ने पुष्प वर्षा की!\n\n"
    "आगे गुरु द्रोण के किस शिष्य ने गुरु-दक्षिणा में अनूठा बलिदान दिया? जानिए भाग 3 (एकलव्य) में!\n\n"
    "🔔 भाग 3 देखने के लिए @itihasasaga को अभी सब्सक्राइब और फॉलो करें!\n\n"
    "📜 प्रामाणिक स्रोत: महाभारत (आदि पर्व, संभव पर्व अध्याय 100)\n\n"
    "#mahabharata #bhishma #bhishmapratigya #devavrata #hastinapur #eklavya #itihasasaga #sanatandharma #shorts #reels #viralshorts"
)
TAGS = [
    "महाभारत", "भीष्म प्रतिज्ञा", "देवव्रत", "हस्तिनापुर", "सत्यवती", "शांतनु", "एकलव्य",
    "mahabharata", "bhishma pratigya", "itihasa saga", "sanatan dharma", "shorts"
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
            title_hindi="देवव्रत की 'भीष्म प्रतिज्ञा': पिता के सुख के लिए आजीवन ब्रह्मचर्य और राज्य का त्याग",
            hook_hindi="वर्षों बाद देवी गंगा ने शांतनु को महावीर पुत्र देवव्रत लौटाया। पर आगे सत्यवती के विवाह हेतु राजा शांतनु व्याकुल हो उठे!",
            full_script=DESCRIPTION
        )

    print("\n=== MULTI-PLATFORM PUBLISH RECEIPT ===")
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    if not audit.get("certified_published"):
        sys.exit(1)


if __name__ == "__main__":
    main()
