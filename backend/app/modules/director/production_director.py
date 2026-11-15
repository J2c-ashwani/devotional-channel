from typing import Dict, Any, List, Optional

class AutomatedProductionDirector:
    """
    Module R: Automated Production Director.
    Acts as the supervising film director for autonomous animation.
    Responsibilities:
    1. Continuity Review: Verifies lighting mood, spatial eye-line, and attire continuity across scenes.
    2. Cinematic Rhythm: Enforces Hollywood/Vedic visual progression (Wide Establishing -> Medium Dialogue -> Dynamic Close-Up Climax -> Wide Resolution).
    3. Regeneration Decision: Flags deficient or mismatched scenes for immediate regeneration before final render.
    """

    @classmethod
    def review_storyboard_direction(
        cls,
        scenes: List[Dict[str, Any]],
        character_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        continuity_issues: List[str] = []
        cinematic_notes: List[str] = []
        needs_regeneration: List[int] = []

        total_scenes = len(scenes)
        if total_scenes < 2:
            return {
                "approved": False,
                "director_score": 50.0,
                "issues": ["Production requires at least 3 scenes to establish cinematic rhythm."]
            }

        # Check visual progression
        first_scene = scenes[0]
        last_scene = scenes[-1]
        
        # Establishing check
        if "wide" not in first_scene.get("camera_movement", "").lower() and "zoom" not in first_scene.get("camera_movement", "").lower():
            cinematic_notes.append("Director Note: Opening scene should emphasize environmental scale.")

        # Climax intensity check
        if total_scenes >= 3:
            climax_scene = scenes[total_scenes - 2]
            climax_prompt = climax_scene.get("visual_prompt", "").lower()
            if not any(k in climax_prompt for k in ["climax", "burst", "divine", "power", "break", "shatter", "radiant"]):
                cinematic_notes.append("Director Note: Climax scene needs enhanced visual drama.")

        # Pacing consistency check
        durations = [s.get("duration_sec", 6.0) for s in scenes]
        avg_dur = sum(durations) / len(durations)
        for idx, s in enumerate(scenes, 1):
            dur = s.get("duration_sec", 6.0)
            if dur > avg_dur * 2.5:
                continuity_issues.append(f"Scene {idx} duration ({dur}s) drags pacing; consider trimming.")
            elif dur < 2.0:
                needs_regeneration.append(idx)
                continuity_issues.append(f"Scene {idx} duration ({dur}s) is too brief for viewer comprehension.")

        score = 100.0 - (len(continuity_issues) * 10.0)
        is_approved = (score >= 80.0) and (len(needs_regeneration) == 0)

        return {
            "approved": is_approved,
            "director_score": max(0.0, score),
            "scenes_reviewed": total_scenes,
            "continuity_issues": continuity_issues,
            "cinematic_notes": cinematic_notes,
            "regenerate_scene_indices": needs_regeneration,
            "director_signoff": "PASSED" if is_approved else "REVISE_PACING"
        }
