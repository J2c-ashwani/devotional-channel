import json
from typing import Dict, Any, Optional, List
from backend.app.config import settings

class CharacterRegistry:
    """
    Module G (Enhanced): Character Consistency & Multi-Angle Sheet Engine.
    Stores approved reference portraits, angles (front, 3/4, side),
    expressions (serene, raudra, compassionate), and clothing reference sheets.
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
            
            if name_str in topic_title or short_id in topic_title.lower():
                matched.append(char)
            elif ("राम" in topic_title or "धनुष" in topic_title or "जनक" in topic_title or "सीता" in topic_title) and "rama" in char_id:
                matched.append(char)
            elif "शिव" in topic_title and "shiva" in char_id:
                matched.append(char)
            elif "कृष्ण" in topic_title and "krishna" in char_id:
                matched.append(char)
            elif "कर्ण" in topic_title and "karna" in char_id:
                matched.append(char)
            elif "अर्जुन" in topic_title and "arjuna" in char_id:
                matched.append(char)
            elif "भीष्म" in topic_title and "arjuna" in char_id:
                matched.append(char)
            elif "हनुमान" in topic_title and "hanuman" in char_id:
                matched.append(char)
            elif "घटोत्कच" in topic_title and "krishna" in char_id:
                matched.append(char)

        # Prioritize protagonist if specifically acting in title (e.g. 'राम ने', 'कृष्ण ने', 'अर्जुन ने')
        def score_char(c):
            c_name = c.get("name", "")
            c_id = c.get("id", "")
            score = 0
            if "श्री राम" in topic_title and "rama" in c_id:
                score += 20
            elif "राम ने" in topic_title and "rama" in c_id:
                score += 25
            elif "कृष्ण" in topic_title and "krishna" in c_id:
                score += 20
            elif "शिव जी" in topic_title and "shiva" in c_id:
                score += 20
            elif "हनुमान" in topic_title and "hanuman" in c_id:
                score += 20
            return score

        matched.sort(key=score_char, reverse=True)
        if not matched and len(self.characters) > 0:
            matched.append(list(self.characters.values())[0])
        return matched

class CharacterPromptBuilder:
    """
    Constructs multi-angle, expression-conditioned image prompts with strict visual conditioning.
    """

    APPROVED_ANGLES = ["front_portrait", "three_quarter_heroic", "profile_determined", "wide_action_stance"]
    APPROVED_EXPRESSIONS = ["serene_yogic", "raudra_battle_fury", "karuna_compassion", "focused_archer_dhyana"]

    @classmethod
    def build_consistent_prompt(
        cls,
        character: Dict[str, Any],
        scene_action: str,
        camera_angle: str = "three_quarter_heroic",
        expression: str = "serene_yogic",
        attire_variant: str = "standard"
    ) -> str:
        dna = character.get("visual_dna", {})
        char_name = character.get("name", character.get("name_hindi", "Lord Rama"))
        
        dna_clauses = [
            f"Face: {dna.get('facial_characteristics', '')}",
            f"Skin: {dna.get('skin_tone', '')}",
            f"Hair: {dna.get('hairstyle', '')}",
            f"Attire: {dna.get('clothing', '')}",
            f"Jewellery: {dna.get('jewellery', '')}",
            f"Physique: {dna.get('body_proportions', '')}",
            f"Iconography: {', '.join(dna.get('accessories', []))}"
        ]
        
        full_dna_spec = " | ".join(dna_clauses)
        
        prompt = (
            f"Masterpiece 3D cinematic render of {char_name}. "
            f"Angle: [{camera_angle}], Expression: [{expression}]. "
            f"Visual DNA: [{full_dna_spec}]. "
            f"Action in Scene: {scene_action}. "
            f"Rendering Specs: Octane 3D hyper-detail, volumetric god-rays, cinematic photorealism, subsurface skin scattering, zero anatomical deformities, exact reference match."
        )
        return prompt
