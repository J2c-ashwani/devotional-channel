from typing import Dict, Any, List, Optional

class HardRuleEnforcer:
    """
    Evaluates hard blockers that instantly reject and quarantine a video regardless of numerical score.
    """

    @classmethod
    def evaluate_hard_blockers(
        cls,
        fact_check_result: Dict[str, Any],
        copyright_result: Dict[str, Any],
        policy_result: Dict[str, Any],
        render_result: Dict[str, Any],
        audio_result: Dict[str, Any],
        is_duplicate: bool
    ) -> Optional[str]:
        # 1. Fact checking blocker
        if fact_check_result.get("hard_blocker", False):
            return f"Fact-Checking Failure: {fact_check_result.get('blocker_reason')}"

        # 2. Copyright blocker
        if not copyright_result.get("certified", False):
            return f"Copyright Safety Failure: {copyright_result.get('reason')}"

        # 3. Policy & Community Guidelines blocker
        if not policy_result.get("passed", False):
            return f"YouTube Policy Violation: {', '.join(policy_result.get('violations', []))}"

        # 4. Technical rendering blocker
        if not render_result.get("success", False) or render_result.get("file_size_bytes", 0) < 50000:
            return "Technical Rendering Failure: Corrupted, missing, or empty video file."

        # 5. Audio failure blocker
        if not audio_result.get("success", False):
            return "Audio Quality Failure: Incomplete, clipping, or missing voice track."

        # 6. Duplicate content blocker
        if is_duplicate:
            return "Duplicate Content Failure: Topic or script already published previously."

        return None
