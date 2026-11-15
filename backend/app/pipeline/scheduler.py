from datetime import datetime
import pytz
from typing import Dict, Any
from backend.app.config import settings

class AutonomousScheduler:
    """
    Publishing Calendar Manager (Asia/Kolkata IST):
    - Monday - Saturday: Shorts (12:30 or 19:00 IST)
    - Sunday: Long-form Story (19:00 IST)
    - End of Month: Monthly Cinematic Special (19:00 IST)
    """

    @classmethod
    def get_current_ist_time(cls) -> datetime:
        ist_tz = pytz.timezone(settings.PUBLISH_TIMEZONE)
        return datetime.now(ist_tz)

    @classmethod
    def determine_scheduled_format(cls, target_dt: datetime = None) -> Dict[str, Any]:
        dt = target_dt or cls.get_current_ist_time()
        weekday = dt.strftime("%A") # Monday, Sunday, etc.
        day_of_month = dt.day

        # Check for Month-End Special (last Sunday or day >= 28)
        is_month_end = day_of_month >= 28 and weekday == "Sunday"

        if is_month_end:
            return {
                "format": "MONTHLY_SPECIAL",
                "weekday": weekday,
                "target_time_ist": "19:00",
                "slot_name": f"SPECIAL_{dt.strftime('%b').upper()}"
            }
        elif weekday == "Sunday":
            return {
                "format": "LONG_FORM",
                "weekday": weekday,
                "target_time_ist": "19:00",
                "slot_name": "LONG_SUN"
            }
        else:
            return {
                "format": "SHORT",
                "weekday": weekday,
                "target_time_ist": "19:00", # default evening peak
                "slot_name": f"SHORTS_{weekday[:3].upper()}"
            }
