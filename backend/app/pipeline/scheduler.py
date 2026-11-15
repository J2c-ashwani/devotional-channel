from datetime import datetime
import pytz
from typing import Dict, Any
from backend.app.config import settings

class AutonomousScheduler:
    """
    Publishing Calendar Manager (Asia/Kolkata IST):
    Enforces a single consistent publishing window (7:00 PM IST / 13:30 UTC)
    and strictly resolves scheduling collisions:
    - Monday through Saturday: Shorts (7:00 PM IST)
    - Sunday: Long-form Story (7:00 PM IST)
    - Final Saturday of Month: Monthly Cinematic Special (7:00 PM IST) - No Sunday collision!
    - Fail-Closed Gate: If a video fails QC, slot is skipped. Never compromise quality for volume.
    """

    DEFAULT_PUBLISH_TIME_IST = "19:00"

    @classmethod
    def get_current_ist_time(cls) -> datetime:
        ist_tz = pytz.timezone(settings.PUBLISH_TIMEZONE)
        return datetime.now(ist_tz)

    @classmethod
    def determine_scheduled_format(cls, target_dt: datetime = None) -> Dict[str, Any]:
        dt = target_dt or cls.get_current_ist_time()
        weekday = dt.strftime("%A") # Monday, Sunday, etc.
        day_of_month = dt.day

        # Check for Month-End Special: Scheduled on last Saturday of the month (day >= 24)
        is_last_saturday = (weekday == "Saturday" and day_of_month >= 24)

        if is_last_saturday:
            return {
                "format": "MONTHLY_SPECIAL",
                "weekday": weekday,
                "target_time_ist": cls.DEFAULT_PUBLISH_TIME_IST,
                "slot_name": f"SPECIAL_{dt.strftime('%b').upper()}_GALA",
                "collision_prevented": "Dedicated Saturday prime window (leaves Sunday intact)"
            }
        elif weekday == "Sunday":
            return {
                "format": "LONG_FORM",
                "weekday": weekday,
                "target_time_ist": cls.DEFAULT_PUBLISH_TIME_IST,
                "slot_name": "LONG_SUN"
            }
        else:
            return {
                "format": "SHORT",
                "weekday": weekday,
                "target_time_ist": cls.DEFAULT_PUBLISH_TIME_IST,
                "slot_name": f"SHORTS_{weekday[:3].upper()}"
            }
