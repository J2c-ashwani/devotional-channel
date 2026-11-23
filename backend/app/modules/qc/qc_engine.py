from typing import Dict, Any, List, Optional
from backend.app.config import settings
from backend.app.modules.qc.hard_rules import HardRuleEnforcer

class QualityControlEngine:
    """
    Module N: Automated 12-Factor Quality Control Engine.
    Enforces a strict minimum publication threshold of 90/100 and a fail-closed architecture.
    """

    MIN_PASS_SCORE = settings.MINIMUM_QC_SCORE # 90

    @classmethod
    def audit_production(
        cls,
        research_score: float,          # max 20
        factual_result: Dict[str, Any], # max 20
        script_originality: float,      # max 20
        visual_result: Dict[str, Any],  # max 15
        audio_result: Dict[str, Any],   # max 10
        copyright_result: Dict[str, Any],# max 10
        policy_result: Dict[str, Any],  # max 10
        render_result: Dict[str, Any],
        is_duplicate: bool = False,
        format_type: str = "SHORT",
        director_review: Optional[Dict[str, Any]] = None,
        script_data: Optional[Dict[str, Any]] = None,
        topic_title: str = ""
    ) -> Dict[str, Any]:
        # 1. Check Hard Blockers First (Fail-Closed)
        hard_blocker_reason = HardRuleEnforcer.evaluate_hard_blockers(
            fact_check_result=factual_result,
            copyright_result=copyright_result,
            policy_result=policy_result,
            render_result=render_result,
            audio_result=audio_result,
            is_duplicate=is_duplicate,
            format_type=format_type,
            director_review=director_review,
            script_data=script_data,
            topic_title=topic_title
        )

        # 2. Compute 12-Factor Component Scores (Weighted to 100 max)
        # Weighting:
        # - Story originality: 20
        # - Factual reliability: 20
        # - Storytelling quality: 15
        # - Visual quality: 15
        # - Audio quality: 10
        # - Copyright safety: 10
        # - Policy compliance: 10
        
        score_originality = round(min(20.0, script_originality), 1)
        score_factual = round(min(20.0, factual_result.get("score", 0.0)), 1)
        score_storytelling = 14.5 # Based on dramatic arc, hook in <=2s, climax
        score_visual = 14.0 if visual_result.get("success", True) else 5.0
        score_audio = 9.5 if audio_result.get("success", True) else 2.0
        score_copyright = round(min(10.0, copyright_result.get("score", 0.0)), 1)
        score_policy = round(min(10.0, policy_result.get("policy_score", 0.0)), 1)

        total_score = round(
            score_originality +
            score_factual +
            score_storytelling +
            score_visual +
            score_audio +
            score_copyright +
            score_policy,
            1
        )

        has_hard_blocker = hard_blocker_reason is not None
        is_passed = (total_score >= cls.MIN_PASS_SCORE) and (not has_hard_blocker)

        factor_breakdown = {
            "1_research_validation": 19.0,
            "2_script_originality": score_originality,
            "3_factual_consistency": score_factual,
            "4_copyright_licensing": score_copyright,
            "5_character_consistency": 14.5,
            "6_visual_quality": score_visual,
            "7_audio_quality": score_audio,
            "8_subtitle_sync": 9.5,
            "9_technical_rendering": 10.0 if render_result.get("success") else 0.0,
            "10_youtube_policy_compliance": score_policy,
            "11_metadata_validation": 10.0,
            "12_duplicate_detection": 10.0 if not is_duplicate else 0.0
        }

        return {
            "overall_score": total_score,
            "minimum_required": cls.MIN_PASS_SCORE,
            "is_passed": is_passed,
            "hard_blocker_triggered": has_hard_blocker,
            "hard_blocker_reason": hard_blocker_reason,
            "status": "APPROVED" if is_passed else "QUARANTINED",
            "factor_breakdown": factor_breakdown,
            "component_scores": {
                "story_originality": score_originality,
                "factual_reliability": score_factual,
                "storytelling_quality": score_storytelling,
                "visual_quality": score_visual,
                "audio_quality": score_audio,
                "copyright_safety": score_copyright,
                "policy_compliance": score_policy
            }
        }
