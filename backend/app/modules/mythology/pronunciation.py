import json
from pathlib import Path
from typing import Dict, Any
from backend.app.config import settings

class PronunciationManager:
    def __init__(self):
        dict_path = settings.CONFIG_DIR / "pronunciation_dict.json"
        if dict_path.exists():
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.mappings: Dict[str, Any] = data.get("mappings", {})
        else:
            self.mappings = {}

    def apply_pronunciation_rules(self, text: str) -> str:
        """
        Substitutes or normalizes known phonetic edge cases in Hindi narration.
        """
        processed_text = text
        for word, meta in self.mappings.items():
            if word in processed_text:
                # Can be used to inject phonetic hints or normalize spelling
                sub = meta.get("ssml_sub", word)
                processed_text = processed_text.replace(word, sub)
        return processed_text

    def wrap_in_ssml(self, text: str, voice_profile: Dict[str, Any] = None) -> str:
        """
        Wraps text in SSML with rate, pitch, and prosody parameters.
        """
        pitch = voice_profile.get("pitch", "0Hz") if voice_profile else "0Hz"
        rate = voice_profile.get("rate", "0%") if voice_profile else "0%"
        
        enhanced_text = self.apply_pronunciation_rules(text)
        
        ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="hi-IN">'
            f'<prosody pitch="{pitch}" rate="{rate}">'
            f'{enhanced_text}'
            f'</prosody>'
            f'</speak>'
        )
        return ssml
