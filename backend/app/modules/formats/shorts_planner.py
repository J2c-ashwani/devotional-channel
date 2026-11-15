from typing import Dict, Any, List

class ShortsPlanner:
    """
    Module D: Shorts Content Planner & Storyboard Architect.
    Enforces:
    - 9:16 vertical aspect ratio (1080x1920).
    - 30-60 second target duration.
    - Scene breakdown with high dynamism (6-8s per scene).
    - Dynamic Hindi subtitle styling.
    """

    @classmethod
    def create_storyboard_spec(cls, script_data: Dict[str, Any], character_dna_prompts: Dict[str, str]) -> Dict[str, Any]:
        duration = script_data.get("estimated_duration_sec", 45)
        
        # Split into 4 high-energy visual scenes
        scenes = [
            {
                "scene_index": 1,
                "scene_name": "Opening Dramatic Hook",
                "duration_sec": 8.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data["opening_hook_hindi"],
                "camera_movement": "Rapid zoom in with subtle camera shake",
                "lighting": "High-contrast dramatic rim lighting, volcanic or divine cosmic glow",
                "visual_prompt": f"Cinematic 9:16 vertical shot, dramatic opening scene, {character_dna_prompts.get('primary', 'Epic mythological encounter')}, photorealistic 8k octane render, dramatic atmospheric fog, epic lighting",
                "sfx_cue": "thunder_rumble"
            },
            {
                "scene_index": 2,
                "scene_name": "Crisis & Narrative Tension",
                "duration_sec": 14.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data["narrative_body_hindi"],
                "camera_movement": "Slow upward tilt revealing colossal scale",
                "lighting": "Moody deep shadows, mystical atmospheric haze",
                "visual_prompt": f"Cinematic 9:16 vertical shot, mythic tension, {character_dna_prompts.get('secondary', 'Deep divine cosmic balance')}, golden hour mystical lighting, hyper-detailed environment",
                "sfx_cue": "ambient_drone"
            },
            {
                "scene_index": 3,
                "scene_name": "Climax Turning Point",
                "duration_sec": 14.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data["climax_hindi"],
                "camera_movement": "Dynamic rotational orbit around character",
                "lighting": "Radiant divine aura, incandescent energy bursting from center",
                "visual_prompt": f"Cinematic 9:16 vertical shot, peak climax, divine intervention, {character_dna_prompts.get('primary', 'Godly manifestation')}, intense particle effects, glowing aura",
                "sfx_cue": "divine_chime_bell"
            },
            {
                "scene_index": 4,
                "scene_name": "Resolution & Philosophical Ending",
                "duration_sec": 9.0,
                "aspect_ratio": "9:16",
                "resolution": [1080, 1920],
                "narration_hindi": script_data["conclusion_hindi"],
                "camera_movement": "Slow pullback into wide majestic panorama",
                "lighting": "Golden dawn twilight, serene celestial calm",
                "visual_prompt": f"Cinematic 9:16 vertical shot, peaceful divine aftermath, sacred Himalayas or holy river at sunrise, spiritual glow, photorealistic 8k",
                "sfx_cue": "shankh_conch"
            }
        ]

        return {
            "format": "SHORT",
            "aspect_ratio": "9:16",
            "resolution": [1080, 1920],
            "total_scenes": len(scenes),
            "estimated_duration_sec": duration,
            "scenes": scenes
        }
