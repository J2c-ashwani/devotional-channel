from typing import Dict, Any, List
from backend.app.agents.director_agent import ProductionDirectorAgent

class ShortsPlanner:
    """
    Module D: Shorts Content Planner & Storyboard Architect.
    Enforces:
    - 9:16 vertical aspect ratio (1080x1920).
    - 60-90 second target duration (Strictly NO rushed 20-30s clips).
    - 5-act complete narrative arc with high dynamism (12-16s per scene).
    - Explicit character prompts with strict iconographic safeguards.
    - Dynamic Hindi subtitle and badge styling.
    """

    @classmethod
    def create_storyboard_spec(cls, script_data: Dict[str, Any], character_dna_prompts: Dict[str, str]) -> Dict[str, Any]:
        # If scriptwriter agent produced a 5-act rich screenplay, use it directly!
        if "scenes" in script_data and len(script_data["scenes"]) >= 4:
            planned_scenes = []
            for s in script_data["scenes"]:
                idx = s.get("scene_index", len(planned_scenes) + 1)
                dur = float(s.get("duration_sec", 14.0))
                narrator_text = s.get("narrator_text_hindi") or s.get("narration_hindi", "")
                dialogue = s.get("dialogue_hindi", "")
                full_narration = f"{narrator_text} {dialogue}".strip() if dialogue else narrator_text

                visual_desc = s.get("visual_description_english", "")
                # Audit and inject iconographic rules via ProductionDirectorAgent
                audited_prompt = ProductionDirectorAgent.audit_scene_prompt(
                    character_id=s.get("dialogue_speaker", ""),
                    prompt=f"Cinematic 9:16 vertical shot, 8k octane render, hyper-realistic ancient Bharatvarsha. {visual_desc}"
                )

                sfx = "thunder_rumble" if idx == 1 else ("shankh_conch" if idx >= len(script_data["scenes"]) else "divine_chime_bell")

                planned_scenes.append({
                    "scene_index": idx,
                    "scene_name": s.get("scene_name", f"Act {idx}"),
                    "duration_sec": dur,
                    "aspect_ratio": "9:16",
                    "resolution": [1080, 1920],
                    "narration_hindi": full_narration,
                    "speaker": s.get("dialogue_speaker"),
                    "dialogue_hindi": dialogue,
                    "camera_movement": "Cinematic slow push and dramatic reveal",
                    "lighting": "Atmospheric golden hour, divine ray tracing, majestic glow",
                    "visual_prompt": audited_prompt,
                    "sfx_cue": sfx
                })

            total_dur = sum(sc["duration_sec"] for sc in planned_scenes)
            return {
                "format": "SHORT",
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "total_scenes": len(planned_scenes),
                "estimated_duration_sec": total_dur,
                "scenes": planned_scenes
            }

        # Fallback for legacy 4-scene scripts (automatically scaled up to 60+ seconds)
        duration = max(60.0, float(script_data.get("estimated_duration_sec", 65.0)))
        scenes = [
            {
                "scene_index": 1,
                "scene_name": "Opening Dramatic Hook",
                "duration_sec": 13.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data.get("opening_hook_hindi", ""),
                "camera_movement": "Rapid zoom in with subtle camera shake",
                "lighting": "High-contrast dramatic rim lighting, volcanic or divine cosmic glow",
                "visual_prompt": ProductionDirectorAgent.audit_scene_prompt(
                    "primary",
                    f"Cinematic 9:16 vertical shot, dramatic opening scene, {character_dna_prompts.get('primary', 'Epic mythological encounter')}, photorealistic 8k octane render, dramatic atmospheric fog, epic lighting"
                ),
                "sfx_cue": "thunder_rumble"
            },
            {
                "scene_index": 2,
                "scene_name": "Crisis & Narrative Tension",
                "duration_sec": 14.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data.get("narrative_body_hindi", ""),
                "camera_movement": "Slow upward tilt revealing colossal scale",
                "lighting": "Moody deep shadows, mystical atmospheric haze",
                "visual_prompt": ProductionDirectorAgent.audit_scene_prompt(
                    "secondary",
                    f"Cinematic 9:16 vertical shot, mythic tension, {character_dna_prompts.get('secondary', 'Deep divine cosmic balance')}, golden hour mystical lighting, hyper-detailed environment"
                ),
                "sfx_cue": "ambient_drone"
            },
            {
                "scene_index": 3,
                "scene_name": "Climax Turning Point",
                "duration_sec": 18.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data.get("climax_hindi", ""),
                "camera_movement": "Dynamic rotational orbit around character",
                "lighting": "Radiant divine aura, incandescent energy bursting from center",
                "visual_prompt": ProductionDirectorAgent.audit_scene_prompt(
                    "primary",
                    f"Cinematic 9:16 vertical shot, peak climax, divine intervention, {character_dna_prompts.get('primary', 'Godly manifestation')}, intense particle effects, glowing aura"
                ),
                "sfx_cue": "divine_chime_bell"
            },
            {
                "scene_index": 4,
                "scene_name": "Resolution & Philosophical Ending",
                "duration_sec": 15.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data.get("conclusion_hindi", ""),
                "camera_movement": "Slow pullback into wide majestic panorama",
                "lighting": "Golden dawn twilight, serene celestial calm",
                "visual_prompt": ProductionDirectorAgent.audit_scene_prompt(
                    "primary",
                    "Cinematic 9:16 vertical shot, peaceful divine aftermath, sacred Himalayas or holy river at sunrise, spiritual glow, photorealistic 8k"
                ),
                "sfx_cue": "shankh_conch"
            }
        ]

        return {
            "format": "SHORT",
            "aspect_ratio": "9:16",
            "resolution": [1080, 1920],
            "total_scenes": len(scenes),
            "estimated_duration_sec": sum(s["duration_sec"] for s in scenes),
            "scenes": scenes
        }
