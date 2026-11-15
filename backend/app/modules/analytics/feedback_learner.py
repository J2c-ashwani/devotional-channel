from typing import List, Dict, Any

class FeedbackLearner:
    """
    Module P: Analytics Learning & Optimization Loop.
    Feeds real audience retention and CTR performance back into topic scoring
    and hook pacing strategies.
    """

    @classmethod
    def evaluate_retention_and_adapt(cls, performance_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not performance_history:
            return {
                "recommendation": "Maintain baseline dramatic pacing.",
                "hook_pacing_multiplier": 1.0,
                "priority_deities": ["Lord Shiva", "Lord Krishna", "Lord Rama"]
            }

        avg_ctr = sum(p.get("click_through_rate_pct", 0) for p in performance_history) / len(performance_history)
        avg_retention = sum(p.get("average_percentage_viewed", 0) for p in performance_history) / len(performance_history)

        adjustments = []
        if avg_retention > 80.0:
            adjustments.append("High audience retention detected (>80%): Narrative pacing is optimal.")
            hook_multiplier = 1.05
        elif avg_retention < 60.0:
            adjustments.append("Audience drop-off detected: Tighten first 2 seconds hook; eliminate slow introductions.")
            hook_multiplier = 0.90
        else:
            hook_multiplier = 1.0

        if avg_ctr > 12.0:
            adjustments.append("Exceptional CTR (>12%): Thumbnail contrasting banners and Hindi title phrasing are highly effective.")
        else:
            adjustments.append("CTR below target (<=12%): Increase color contrast and emotional character focus on thumbnails.")

        return {
            "average_ctr": round(avg_ctr, 2),
            "average_retention_pct": round(avg_retention, 2),
            "hook_pacing_multiplier": hook_multiplier,
            "insights": adjustments,
            "preferred_themes": ["Cosmic sacrifice", "Unsung warrior dilemmas", "Spiritual liberation"]
        }
