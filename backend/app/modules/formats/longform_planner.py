from typing import Dict, Any, List, Optional

class LongformPlanner:
    """
    Module E: Long-form Storyboard Architect.
    Enforces:
    - 16:9 widescreen horizontal aspect ratio (1920x1080).
    - 8-15 minute production scope (configurable for testing).
    - Deep multi-scene chapters and emotional transitions.
    """

    @classmethod
    def create_storyboard_spec(
        cls,
        script_data: Dict[str, Any],
        character_dna_prompts: Dict[str, str],
        scene_duration_override: Optional[float] = None
    ) -> Dict[str, Any]:
        d1 = scene_duration_override or 60.0
        d2 = scene_duration_override or 120.0
        d3 = scene_duration_override or 240.0
        d4 = scene_duration_override or 120.0

        scenes = [
            {
                "scene_index": 1,
                "scene_name": "Act 1: Aftermath & Cosmic Moral Dilemma",
                "duration_sec": d1,
                "aspect_ratio": "16:9",
                "resolution": [1920, 1080],
                "narration_hindi": script_data["opening_hook_hindi"],
                "camera_movement": "Slow sweeping panoramic crane shot across Kurukshetra",
                "lighting": "Smoky twilight amber embers, tragic melancholic dusk",
                "visual_prompt": "Cinematic 16:9 widescreen, epic historical battlefield of Kurukshetra at sunset, broken chariots, banners in the wind, melancholic golden mist, ultra-realistic 8k render"
            },
            {
                "scene_index": 2,
                "scene_name": "Act 2: The Path to the Patriarch",
                "duration_sec": d2,
                "aspect_ratio": "16:9",
                "resolution": [1920, 1080],
                "narration_hindi": script_data["narrative_body_hindi"][:150],
                "camera_movement": "Tracking medium shot following Krishna and Yudhishthira walking",
                "lighting": "Ethereal glow from Krishna's presence",
                "visual_prompt": "Cinematic 16:9, Lord Krishna guiding the Pandavas through sacred battlefield, dignified grief, golden rim lighting, 3D animated film quality"
            },
            {
                "scene_index": 3,
                "scene_name": "Act 3: The Discourse on the Bed of Arrows",
                "duration_sec": d3,
                "aspect_ratio": "16:9",
                "resolution": [1920, 1080],
                "narration_hindi": script_data["climax_hindi"],
                "camera_movement": "Intimate close-up on Bhishma's serene face, then cutting to listening listeners",
                "lighting": "Celestial sun rays penetrating the gloom",
                "visual_prompt": "Cinematic 16:9, Grandfather Bhishma resting on bed of arrows, divine countenance, serene yogic calm, surrounded by reverent Pandavas and sages, dramatic lighting"
            },
            {
                "scene_index": 4,
                "scene_name": "Act 4: Liberation and the Eternal Truth of Dharma",
                "duration_sec": d4,
                "aspect_ratio": "16:9",
                "resolution": [1920, 1080],
                "narration_hindi": script_data["conclusion_hindi"],
                "camera_movement": "Slow upward ascendant camera movement to open skies",
                "lighting": "Blinding celestial white and gold aura of ascension",
                "visual_prompt": "Cinematic 16:9, Heavenly realm opening above holy battlefield, flower showers from heaven, transcendent golden light, sacred cosmic conclusion"
            }
        ]

        return {
            "format": "LONG_FORM",
            "aspect_ratio": "16:9",
            "resolution": [1920, 1080],
            "total_scenes": len(scenes),
            "estimated_duration_sec": sum(s["duration_sec"] for s in scenes),
            "scenes": scenes
        }

class SpecialPlanner:
    """
    Module F: Monthly Cinematic Special (30-45 minutes).
    Premium episodic production combining multiple story chapters into an epic filmic experience.
    """
    @classmethod
    def create_storyboard_spec(cls, topic_data: Dict[str, Any], character_dna_prompts: Dict[str, str]) -> Dict[str, Any]:
        return {
            "format": "MONTHLY_SPECIAL",
            "aspect_ratio": "16:9",
            "resolution": [1920, 1080],
            "total_acts": 5,
            "estimated_duration_sec": 1800,
            "premium_grade": True
        }
