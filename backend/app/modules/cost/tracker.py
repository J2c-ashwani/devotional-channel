import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.app.config import settings

class CostTracker:
    """
    Module Q: Micro-unit Cost Tracker & Persistent Monthly Ledger.
    Calculates operational expenditure per token, character, frame, and compute second,
    and persists job costs to a monthly ledger so BudgetGuard enforces real spend.
    """

    PRICING_RATES = {
        "LLM_PROMPT_PER_1K": 0.00015,
        "LLM_COMPLETION_PER_1K": 0.00060,
        "IMAGE_GENERATION_PER_IMAGE": 0.030,
        "VIDEO_GENERATION_PER_SEC": 0.050,
        "TTS_CHARS_PER_1K": 0.015,
        "RENDER_COMPUTE_PER_MIN": 0.005
    }

    @classmethod
    def _get_ledger_path(cls) -> Path:
        return Path(settings.STORAGE_DIR) / "cost_ledger.json"

    @classmethod
    def _load_ledger(cls) -> List[Dict[str, Any]]:
        ledger_path = cls._get_ledger_path()
        if not ledger_path.exists():
            return []
        try:
            data = json.loads(ledger_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    @classmethod
    def _save_ledger(cls, entries: List[Dict[str, Any]]) -> None:
        ledger_path = cls._get_ledger_path()
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(ledger_path.parent), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2)
            os.replace(tmp_name, ledger_path)
        except Exception:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise

    @classmethod
    def get_monthly_spend(cls, year_month: Optional[str] = None) -> float:
        """Returns accumulated USD spend for the given YYYY-MM (defaults to current UTC month)."""
        target_month = year_month or datetime.utcnow().strftime("%Y-%m")
        entries = cls._load_ledger()
        total = sum(
            float(e.get("total_cost_usd", 0.0))
            for e in entries
            if isinstance(e, dict) and e.get("month") == target_month
        )
        return round(total, 4)

    @classmethod
    def record_job_cost(
        cls,
        job_id: str,
        format_type: str,
        cost_report: Dict[str, Any],
        status: str = "COMPLETED"
    ) -> float:
        """Appends a job's calculated cost to the persistent ledger and returns updated monthly spend."""
        ts = cost_report.get("timestamp") or datetime.utcnow().isoformat()
        month = ts[:7] if len(ts) >= 7 else datetime.utcnow().strftime("%Y-%m")
        entries = cls._load_ledger()
        entries.append({
            "job_id": job_id,
            "format_type": format_type,
            "status": status,
            "month": month,
            "total_cost_usd": round(float(cost_report.get("total_cost_usd", 0.0)), 4),
            "breakdown": cost_report.get("breakdown", {}),
            "timestamp": ts
        })
        cls._save_ledger(entries)
        return cls.get_monthly_spend(month)

    @classmethod
    def estimate_job_cost(cls, format_type: str) -> float:
        """Returns a conservative pre-run cost estimate for budget gating."""
        fmt = (format_type or "SHORT").upper()
        if fmt == "MONTHLY_SPECIAL":
            return 15.0
        if fmt == "LONG_FORM":
            return 5.0
        return 0.50

    @classmethod
    def calculate_job_cost(
        cls,
        tokens_used: int,
        images_generated: int,
        video_seconds: float,
        tts_characters: int,
        render_seconds: float
    ) -> Dict[str, Any]:
        llm_cost = (tokens_used / 1000.0) * cls.PRICING_RATES["LLM_PROMPT_PER_1K"]
        image_cost = images_generated * cls.PRICING_RATES["IMAGE_GENERATION_PER_IMAGE"]
        video_cost = video_seconds * cls.PRICING_RATES["VIDEO_GENERATION_PER_SEC"]
        tts_cost = (tts_characters / 1000.0) * cls.PRICING_RATES["TTS_CHARS_PER_1K"]
        compute_cost = (render_seconds / 60.0) * cls.PRICING_RATES["RENDER_COMPUTE_PER_MIN"]

        total_cost = llm_cost + image_cost + video_cost + tts_cost + compute_cost

        return {
            "total_cost_usd": round(total_cost, 4),
            "breakdown": {
                "llm_usd": round(llm_cost, 4),
                "image_usd": round(image_cost, 4),
                "video_usd": round(video_cost, 4),
                "tts_usd": round(tts_cost, 4),
                "compute_usd": round(compute_cost, 4)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
