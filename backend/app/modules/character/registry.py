import json
from typing import Dict, Any, Optional, List
from backend.app.config import settings

class CharacterRegistry:
    """
    Module G: Permanent Character Database Registry.
    Maintains canonical visual DNA, iconography, and voice traits.
    """

    def __init__(self):
        bible_path = settings.CONFIG_DIR / "character_bible.json"
        with open(bible_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.characters: Dict[str, Dict[str, Any]] = {c["id"]: c for c in data.get("characters", [])}

    def get_character_by_id(self, char_id: str) -> Optional[Dict[str, Any]]:
        return self.characters.get(char_id)

    def find_characters_for_topic(self, topic_title: str) -> List[Dict[str, Any]]:
        matched = []
        for char_id, char in self.characters.items():
            name_str = char.get("name", char.get("name_hindi", ""))
            short_id = char_id.replace("char_", "")
            
            # Check direct match
            if name_str in topic_title or short_id in topic_title.lower():
                matched.append(char)
            elif "शिव" in topic_title and "shiva" in char_id:
                matched.append(char)
            elif "राम" in topic_title and "rama" in char_id:
                matched.append(char)
            elif "कृष्ण" in topic_title and "krishna" in char_id:
                matched.append(char)
            elif "कर्ण" in topic_title and "karna" in char_id:
                matched.append(char)
            elif "अर्जुन" in topic_title and "arjuna" in char_id:
                matched.append(char)
            elif "भीष्म" in topic_title and "arjuna" in char_id: # kurukshetra warrior group
                matched.append(char)
            elif "हनुमान" in topic_title and "hanuman" in char_id:
                matched.append(char)
            elif "घटोत्कच" in topic_title and "krishna" in char_id:
                matched.append(char)

        if not matched and len(self.characters) > 0:
            matched.append(list(self.characters.values())[0])
        return matched

class CharacterPromptBuilder:
    """
    Injects immutable visual DNA into scene generation prompts to ensure 100% character consistency.
    """

    @classmethod
    def build_consistent_prompt(cls, character: Dict[str, Any], scene_action: str, camera_angle: str) -> str:
        dna = character.get("visual_dna", {})
        char_name = character.get("name", character.get("name_hindi", "Lord Shiva"))
        
        dna_clauses = [
            f"Face: {dna.get('facial_characteristics', '')}",
            f"Skin: {dna.get('skin_tone', '')}",
            f"Hair: {dna.get('hairstyle', '')}",
            f"Attire: {dna.get('clothing', '')}",
            f"Jewellery: {dna.get('jewellery', '')}",
            f"Physique: {dna.get('body_proportions', '')}",
            f"Key Attributes: {', '.join(dna.get('accessories', []))}"
        ]
        
        full_dna_spec = " | ".join(dna_clauses)
        
        prompt = (
            f"Hyper-detailed 3D cinematic rendering of {char_name}. "
            f"Visual DNA: [{full_dna_spec}]. "
            f"Action: {scene_action}. "
            f"Camera & Composition: {camera_angle}. "
            f"Style: Cinematic 3D octane render, photorealistic mythological realism, dramatic volumetric lighting, 8k resolution, no distortions, no extra limbs."
        )
        return prompt
