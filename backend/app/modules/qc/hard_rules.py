from typing import Dict, Any, List, Optional

class HardRuleEnforcer:
    """
    Evaluates hard blockers that instantly reject and quarantine a video regardless of numerical score.
    Enforces the Single-Shot Perfection Protocol (SSPP) so defective or rushed content is NEVER published.
    """

    MIN_SHORTS_DURATION_SEC = 60.0
    MAX_SHORTS_DURATION_SEC = 90.0
    MAX_WORDS_PER_SEC_SPOKEN = 2.6  # Guarantees crisp unhurried Hindi without mid-word cutoffs in Vertex Omni

    @classmethod
    def evaluate_hard_blockers(
        cls,
        fact_check_result: Dict[str, Any],
        copyright_result: Dict[str, Any],
        policy_result: Dict[str, Any],
        render_result: Dict[str, Any],
        audio_result: Dict[str, Any],
        is_duplicate: bool,
        format_type: str = "SHORT",
        director_review: Optional[Dict[str, Any]] = None,
        script_data: Optional[Dict[str, Any]] = None,
        topic_title: str = ""
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

        # 6. Duplicate content blocker (Prevents algorithmic penalty on Instagram / YouTube)
        if is_duplicate:
            return "Duplicate Content Failure: Topic or script already published previously. Suppressed to prevent algorithmic penalty."

        # 7. Single-Shot Perfection Duration Blocker (Strictly 60-90s for Shorts)
        if "duration_sec" in render_result and format_type == "SHORT":
            actual_duration = float(render_result["duration_sec"])
            if actual_duration < cls.MIN_SHORTS_DURATION_SEC:
                return (
                    f"Duration Failure: Video length ({actual_duration:.1f}s) is below mandatory 60.0s minimum. "
                    f"Rushed clips are strictly prohibited by Single-Shot Perfection Protocol."
                )
            if actual_duration > cls.MAX_SHORTS_DURATION_SEC:
                return f"Duration Failure: Video length ({actual_duration:.1f}s) exceeds 90.0s Shorts limit."

        # 8. Scriptural Iconography Blocker (Prabhu Shri Rama vs Shri Krishna separation)
        if script_data:
            full_text = f"{script_data.get('full_screenplay_devanagari', '')} {topic_title}".lower()
            if "राम" in full_text or "rama" in full_text:
                if "peacock feather" in full_text or "mayur pankh" in full_text or "मयूर पंख" in full_text:
                    return "Iconography Failure: Prabhu Shri Rama canonically wears Surya-vamsha Kirita Mukuta; peacock feather is strictly prohibited."

        # 9. Director Signoff Blocker
        if director_review and not director_review.get("director_signoff", True):
            return f"Director Review Failure: {director_review.get('rejection_reason', 'Production Director withheld signoff')}"

        # 10. Pure Talking-Head Character Dialogue Blocker (Locked across BOTH Ramayana & Mahabharata)
        if script_data:
            scenes = script_data.get("scenes", [])
            for sc in scenes:
                speaker = sc.get("dialogue_speaker")
                dialogue = sc.get("dialogue_hindi")
                if speaker and dialogue and sc.get("is_pure_narrator", False):
                    return (
                        f"Talking-Head Rule Failure: Scene '{sc.get('scene_name')}' contains dialogue for '{speaker}', "
                        f"but was flattened into third-person narration. Characters MUST speak in talking heads with their own voice."
                    )

                # 11. Spoken Hindi Word-Density Blocker for Vertex Text-to-Video Scenes
                if format_type == "SHORT" and sc.get("render_mode") == "vertex_omni_t2v":
                    spoken = f"{sc.get('narrator_text_hindi', '')} {dialogue or ''}".strip()
                    word_count = len(spoken.split())
                    dur_sec = max(1.0, float(sc.get("duration_sec", 12.0)))
                    if word_count / dur_sec > cls.MAX_WORDS_PER_SEC_SPOKEN:
                        return (
                            f"Audio Pacing Failure: Scene '{sc.get('scene_name')}' packs {word_count} words into {dur_sec:.1f}s "
                            f"({word_count/dur_sec:.2f} w/s > {cls.MAX_WORDS_PER_SEC_SPOKEN} w/s limit), risking clipped Vertex audio."
                        )

        return None
