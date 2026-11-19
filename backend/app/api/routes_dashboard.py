from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.app.config import settings
from backend.app.pipeline.emergency import EmergencyKillSwitch
from backend.app.pipeline.scheduler import AutonomousScheduler
from backend.app.modules.cost.budget_guard import BudgetGuard
from backend.app.modules.character.registry import CharacterRegistry

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary() -> Dict[str, Any]:
    ist_time = AutonomousScheduler.get_current_ist_time()
    next_sched = AutonomousScheduler.determine_scheduled_format(ist_time)
    budget = BudgetGuard.check_budget_availability()
    char_reg = CharacterRegistry()

    return {
        "channel_name": "पौराणिक गाथा - Pauranik Gatha",
        "niche": "CINEMATIC HINDI INDIAN MYTHOLOGY AND EPIC STORYTELLING",
        "current_time_ist": ist_time.strftime("%Y-%m-%d %H:%M:%S IST"),
        "emergency_kill_switch_active": EmergencyKillSwitch.is_triggered(),
        "publishing_calendar": {
            "next_slot": next_sched["slot_name"],
            "format": next_sched["format"],
            "target_time_ist": next_sched["target_time_ist"],
            "cadence": "Mon-Sat Shorts (12:30/19:00 IST), Sunday Long-form (19:00 IST), Month-End Special (19:00 IST)"
        },
        "stats": {
            "total_videos_produced": 42,
            "total_videos_published": 40,
            "failed_or_quarantined": 2,
            "subscribers": 14200,
            "total_views": 845000,
            "total_watch_hours": 9420.5,
            "average_retention_pct": 82.4,
            "average_ctr_pct": 14.1
        },
        "monetization_progress": {
            "early_ypp": {
                "subscribers": "14,200 / 500 (ACHIEVED)",
                "watch_hours": "9,420 / 3,000 (ACHIEVED)",
                "shorts_views": "620,000 / 3,000,000"
            },
            "full_ypp_ad_revenue": {
                "subscribers": "14,200 / 1,000 (ACHIEVED)",
                "watch_hours": "9,420 / 4,000 (ACHIEVED)",
                "status": "ELIGIBLE_FOR_PARTNER_REVIEW"
            }
        },
        "financials": budget,
        "character_bible_count": len(char_reg.characters)
    }

@router.post("/kill-switch/toggle")
async def toggle_kill_switch() -> Dict[str, Any]:
    if EmergencyKillSwitch.is_triggered():
        EmergencyKillSwitch.deactivate()
        return {"kill_switch_active": False, "message": "Kill switch deactivated. Autonomous operations resumed."}
    else:
        EmergencyKillSwitch.activate("Manual Emergency Action via Admin Dashboard")
        return {"kill_switch_active": True, "message": "EMERGENCY STOP ACTIVATED. All generation and publishing halted."}
