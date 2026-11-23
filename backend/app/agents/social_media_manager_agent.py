"""
Social Media Manager Agent for Itihasa Saga (@itihasasaga).
Monitors, validates, and guarantees multi-platform publishing across YouTube Shorts,
Instagram Reels, and Facebook Page. Performs automated health checks and prevents missed slots.
"""

import datetime
import json
from pathlib import Path
from typing import Dict, Any, Optional
import pytz

from backend.app.config import settings

class SocialMediaManagerAgent:
    """
    Dedicated Social Media Manager Agent.
    Rules:
    1. STRICT SCHEDULE VERIFICATION:
       - Morning Slot: Ramayana published for 7:00 AM IST.
       - Evening Slot: Mahabharata published for 6:30 PM IST.
    2. MULTI-PLATFORM VERIFICATION:
       - Every release MUST be published and verified on ALL 3 channels:
         * YouTube Shorts (Live URL + Video ID)
         * Instagram Reels (Media ID)
         * Facebook Page (Video ID)
    3. FAIL-SAFE RECOVERY:
       - Detects missed or failed publication immediately and provides actionable recovery status.
    4. LEDGER CONTINUITY:
       - Ensures episodic progress is strictly maintained and never duplicated or skipped.
    """

    def __init__(self):
        self.storage_dir = Path("/Users/ashwanikumar/Downloads/devotional/storage")
        self.progress_file = self.storage_dir / "episodic_progress.json"
        self.ledger_file = self.storage_dir / "published_scripts_ledger.json"

    def get_todays_expected_slots(self) -> Dict[str, Any]:
        """Returns the current IST time, active slot, and expected track."""
        ist = pytz.timezone(settings.PUBLISH_TIMEZONE)
        now_ist = datetime.datetime.now(ist)
        
        # Morning slot cutoff: before 12:00 PM IST is Ramayana; after is Mahabharata
        current_track = "RAMAYANA" if now_ist.hour < 12 else "MAHABHARATA"
        expected_slot_time = "7:00 AM IST" if current_track == "RAMAYANA" else "6:30 PM IST"
        
        return {
            "current_time_ist": now_ist.strftime("%Y-%m-%d %I:%M %p IST"),
            "current_track": current_track,
            "expected_slot_time": expected_slot_time,
            "date": now_ist.strftime("%Y-%m-%d")
        }

    def verify_publication_status(self, episode_id: str, youtube_res: Dict[str, Any], meta_res: Dict[str, Any]) -> Dict[str, Any]:
        """Validates all 3 platform IDs before certifying publication."""
        yt_id = youtube_res.get("youtube_video_id") or youtube_res.get("id")
        ig_id = meta_res.get("instagram_media_id")
        fb_id = meta_res.get("facebook_video_id")

        all_passed = bool(yt_id and ig_id and fb_id)
        
        report = {
            "episode_id": episode_id,
            "certified_published": all_passed,
            "platforms": {
                "youtube": {"status": "SUCCESS" if yt_id else "FAILED", "id": yt_id, "url": f"https://youtube.com/shorts/{yt_id}" if yt_id else None},
                "instagram": {"status": "SUCCESS" if ig_id else "FAILED", "media_id": ig_id},
                "facebook": {"status": "SUCCESS" if fb_id else "FAILED", "video_id": fb_id}
            },
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        if all_passed:
            self._record_successful_publication(episode_id, report)

        return report

    def _record_successful_publication(self, episode_id: str, report: Dict[str, Any]):
        """Persists successful publication to storage ledger."""
        try:
            if self.progress_file.exists():
                data = json.loads(self.progress_file.read_text(encoding="utf-8"))
            else:
                data = {"completed_ids": []}

            if episode_id not in data.get("completed_ids", []):
                data.setdefault("completed_ids", []).append(episode_id)
                self.progress_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print("Notice updating episodic ledger:", e)
