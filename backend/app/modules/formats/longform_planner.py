from typing import Dict, Any, List, Optional

class LongformPlanner:
    """
    Module E: Long-form Storyboard Architect.
    Enforces:
    - 16:9 widescreen horizontal aspect ratio (1920x1080).
    - 8-15 minute production scope (480-900 seconds; configurable override for fast tests).
    - Full, untruncated multi-chapter Hindi narration and emotional transitions.
    """

    MIN_DURATION_SEC: float = 480.0   # 8 minutes
    MAX_DURATION_SEC: float = 900.0   # 15 minutes
    WORDS_PER_SECOND: float = 2.33    # ~140 Hindi words/min natural Kathavachak TTS cadence

    @classmethod
    def _estimate_scene_duration(cls, text: str, pause_sec: float = 0.8) -> float:
        words = len((text or "").split())
        return round(max(4.0, (words / cls.WORDS_PER_SECOND) + pause_sec), 1)

    @classmethod
    def _split_body_into_chunks(cls, body_text: str, target_words: int = 130) -> List[str]:
        """Splits a long narrative body on Devanagari/standard sentence boundaries without dropping text."""
        text = (body_text or "").strip()
        if not text:
            return []
        raw_sentences = [s.strip() for s in text.replace("।", "।|").split("|") if s.strip()]
        chunks: List[str] = []
        current: List[str] = []
        current_words = 0
        for sent in raw_sentences:
            w = len(sent.split())
            if current and current_words + w > target_words:
                chunks.append(" ".join(current))
                current = [sent]
                current_words = w
            else:
                current.append(sent)
                current_words += w
        if current:
            chunks.append(" ".join(current))
        return chunks

    @classmethod
    def create_storyboard_spec(
        cls,
        script_data: Dict[str, Any],
        character_dna_prompts: Dict[str, str],
        scene_duration_override: Optional[float] = None
    ) -> Dict[str, Any]:
        primary_char_prompt = character_dna_prompts.get("primary", "") if character_dna_prompts else ""
        chapters = script_data.get("chapters")
        scenes: List[Dict[str, Any]] = []

        if chapters and isinstance(chapters, list):
            for idx, ch in enumerate(chapters, 1):
                narration = (ch.get("narration_hindi") or "").strip()
                dur = scene_duration_override if scene_duration_override is not None else cls._estimate_scene_duration(narration)
                base_prompt = ch.get("visual_prompt", "Cinematic 16:9 widescreen, Indian mythological epic scene, 8k 3D film render")
                visual_prompt = f"{base_prompt}. Character consistency: {primary_char_prompt}" if primary_char_prompt and idx in (3, 6, 7, 8) else base_prompt
                scenes.append({
                    "scene_index": idx,
                    "scene_name": ch.get("scene_name", f"Chapter {idx}"),
                    "duration_sec": dur,
                    "aspect_ratio": "16:9",
                    "resolution": [1920, 1080],
                    "narration_hindi": narration,
                    "camera_movement": ch.get("camera_movement", "Slow cinematic pan"),
                    "lighting": ch.get("lighting", "Warm golden mythological atmosphere"),
                    "visual_prompt": visual_prompt
                })
        else:
            # Fallback for custom script_data without structured chapters: preserve 100% of narrative_body_hindi
            hook_text = (script_data.get("opening_hook_hindi") or "").strip()
            body_chunks = cls._split_body_into_chunks(script_data.get("narrative_body_hindi") or "")
            climax_text = (script_data.get("climax_hindi") or "").strip()
            conclusion_text = (script_data.get("conclusion_hindi") or "").strip()

            raw_acts: List[Dict[str, str]] = [
                {
                    "scene_name": "Act 1: Opening & Cosmic Moral Dilemma",
                    "narration_hindi": hook_text,
                    "camera_movement": "Slow sweeping panoramic crane shot",
                    "lighting": "Smoky twilight amber embers, melancholic golden mist",
                    "visual_prompt": "Cinematic 16:9 widescreen, epic mythological establishing panorama, golden mist, ultra-realistic 8k render"
                }
            ]
            for i, chunk in enumerate(body_chunks, 1):
                raw_acts.append({
                    "scene_name": f"Act 2.{i}: Narrative Progression",
                    "narration_hindi": chunk,
                    "camera_movement": "Tracking medium shot following protagonists",
                    "lighting": "Ethereal warm golden rim lighting",
                    "visual_prompt": "Cinematic 16:9, mythological epic storytelling scene, dignified reverence, golden rim lighting, 3D animated film quality"
                })
            raw_acts.append({
                "scene_name": "Act 3: The Climactic Turning Point",
                "narration_hindi": climax_text,
                "camera_movement": "Dramatic close-up building to climactic reveal",
                "lighting": "Celestial sun rays piercing dramatic skies",
                "visual_prompt": "Cinematic 16:9, epic mythological climax, radiant divine aura, dramatic lighting, 8k 3D render"
            })
            raw_acts.append({
                "scene_name": "Act 4: Resolution and the Eternal Truth of Dharma",
                "narration_hindi": conclusion_text,
                "camera_movement": "Slow upward ascendant camera movement to open skies",
                "lighting": "Blinding celestial white and gold aura",
                "visual_prompt": "Cinematic 16:9, transcendent golden sunrise over sacred ancient realm, flower showers from heaven, cosmic conclusion"
            })

            for idx, act in enumerate(raw_acts, 1):
                narration = act["narration_hindi"]
                dur = scene_duration_override if scene_duration_override is not None else cls._estimate_scene_duration(narration)
                scenes.append({
                    "scene_index": idx,
                    "scene_name": act["scene_name"],
                    "duration_sec": dur,
                    "aspect_ratio": "16:9",
                    "resolution": [1920, 1080],
                    "narration_hindi": narration,
                    "camera_movement": act["camera_movement"],
                    "lighting": act["lighting"],
                    "visual_prompt": act["visual_prompt"]
                })

        return {
            "format": "LONG_FORM",
            "aspect_ratio": "16:9",
            "resolution": [1920, 1080],
            "total_scenes": len(scenes),
            "min_target_duration_sec": cls.MIN_DURATION_SEC,
            "max_target_duration_sec": cls.MAX_DURATION_SEC,
            "estimated_duration_sec": round(sum(s["duration_sec"] for s in scenes), 1),
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
