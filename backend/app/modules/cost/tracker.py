from typing import Dict, Any, List
from datetime import datetime
from backend.app.config import settings

class CostTracker:
    """
    Module Q: Micro-unit Cost Tracker.
    Calculates operational expenditure per token, character, frame, and compute second.
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
