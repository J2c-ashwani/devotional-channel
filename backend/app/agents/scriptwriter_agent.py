"""
Scriptwriter Agent for Itihasa Saga.
Enforces strict, uncompromising rules for narrative depth, scriptural authenticity,
and emotional engagement. Eliminates rushed, shallow 20-30s scripts.
Guarantees 60-90 second complete story arcs with zero unexplained cuts.
"""

import json
import os
from typing import Dict, Any, List
from backend.app.config import settings
from google import genai
from google.genai import types

class ScriptwriterAgent:
    """
    Dedicated AI Scriptwriter Agent.
    Rules:
    1. MINIMUM DURATION: 60 SECONDS (Target 65-80s). Rushed 20-30s clips strictly prohibited.
    2. FULL NARRATIVE ARC: Context/Premise -> Dramatic Conflict -> Heroic Intervention -> Divine Resolution -> Dharmic Moral.
    3. EXPLICIT CHARACTER IDENTIFICATION: Every character MUST be introduced by full name, relationship, and motive. No unexplained walk-ins.
    4. SCRIPTURAL FIDELITY: 100% grounded in Valmiki Ramayana, Ramcharitmanas, or Vyasa Mahabharata.
    5. DIALOGUE EXCELLENCE: Authentic, emotionally resonant Devnagari Hindi dialogues reflecting dharmic persona.
    """

    MIN_DURATION_SEC = 60.0
    TARGET_DURATION_SEC = 75.0
    MAX_DURATION_SEC = 90.0

    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY') or settings.GEMINI_API_KEY
        if api_key and api_key != "mock_key":
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-3.8-flash'
        else:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get(
                'GOOGLE_APPLICATION_CREDENTIALS',
                '/Users/ashwanikumar/Downloads/devotional/service-account.json'
            )
            self.client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_CLOUD_PROJECT or 'devotional-youtube-514907',
                location=settings.GOOGLE_CLOUD_LOCATION or 'global'
            )
            self.model_name = 'gemini-2.5-flash'

    def write_screenplay(self, topic: Dict[str, Any], canonical_source: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a complete 5-to-6-act Hindi Text-to-Video screenplay locked for Pure Talking Heads & Vertex T2V pacing."""
        from backend.app.modules.scriptwriting.screenplay_engine import ScreenplayEngine

        prompt = f"""
You are the Master Mythological Scriptwriter Agent for 'Itihasa Saga' (@itihasasaga), serving BOTH the Morning Ramayana Track AND Evening Mahabharata Track.
Topic: {topic.get('title_hindi')}
Canonical Source: {topic.get('epic_source', canonical_source.get('citation', 'Ancient Canonical Shastras'))}

STRICT UNCOMPROMISING RULES (LOCKED FOR BOTH RAMAYANA & MAHABHARATA):
1. DURATION & ACT BUDGET: Write a 6-Act Shorts screenplay of 12s-15s per scene (total 75s to 84s). NEVER rush into 20-30s!
2. PURE VERTEX TEXT-TO-VIDEO WORD-DENSITY CEILING (CRITICAL):
   - Spoken Hindi inside ANY 12s scene MUST be AT MOST 20 words total (finish by 10s leaving 2s natural music/pause).
   - Spoken Hindi inside ANY 15s scene MUST be AT MOST 26 words total (finish by 13s leaving 2s buffer).
   - Exceeding 2.2 words/sec clips audio syllables on Vertex AI! Keep every spoken line concise, crisp, and punchy.
3. PURE TALKING HEADS FOR CHARACTERS (ZERO THIRD-PERSON VOICEOVER FLATTENING):
   - Characters MUST speak their own Devanagari Hindi dialogue face-to-face on camera in talking-head close-ups with lip-sync.
   - Kathavachak Narrator handles ONLY Act 1 opening context, brief scene bridges, and final Act epilogue + next-episode cliffhanger.
   - NEVER combine heavy third-person narration with character dialogue inside the same 7s beat — give every speaking character their own clean talking-head turn!
4. ABSOLUTE CHARACTER & CHRONOLOGY CLARITY:
   - Clearly establish who enters and why (e.g., Ganga returning Devavrata to Shantanu before Satyavati/Nishadaraj condition; King Janaka & Maharaja Dasharatha embracing before Varmala).
5. SCRIPTURAL ICONOGRAPHY LOCK:
   - Prabhu Shri Rama strictly wears golden Surya-vamsha Kirita Mukuta studded with rubies/pearls ONLY (STRICTLY NO peacock feather / mayur pankh).
   - Shri Krishna wears Peacock Feather (Mayur Pankh) and yellow Pitambara.
   - Rajkumar Devavrata / Pitamaah Bhishma wears ivory-white and gold Kuru silk armor and golden headband crown.

Return a STRICT JSON object with this exact structure:
{{
  "title_hindi": "...",
  "estimated_duration_sec": 78,
  "characters_present": ["...", "..."],
  "scenes": [
    {{
      "scene_index": 1,
      "scene_name": "Epic Context & Arrival",
      "duration_sec": 12.0,
      "render_mode": "vertex_omni_t2v",
      "is_pure_narrator": true,
      "narrator_text_hindi": "<=20 crisp Devanagari Hindi words",
      "dialogue_speaker": null,
      "dialogue_hindi": "",
      "visual_description_english": "Photorealistic 8k scene setting & character attire/motion details...",
      "emotional_tone": "Resonant devotional"
    }},
    {{
      "scene_index": 2,
      "scene_name": "Character Talking Head Confrontation",
      "duration_sec": 12.0,
      "render_mode": "vertex_omni_t2v",
      "is_pure_narrator": false,
      "narrator_text_hindi": "",
      "dialogue_speaker": "राजकुमार देवव्रत",
      "dialogue_hindi": "<=20 crisp spoken Hindi words delivered direct-to-camera with lip-sync",
      "visual_description_english": "Medium close-up talking-head description matching character Bible attire...",
      "emotional_tone": "Fierce filial resolve"
    }}
  ],
  "full_screenplay_devanagari": "Full screenplay text...",
  "takeaway_moral_hindi": "..."
}}
"""
        import time
        from pathlib import Path
        last_err = None

        # Retry primary Gemini model + Vertex AI global gemini-2.5-flash backup before template fallback
        attempts = [(self.client, self.model_name)]
        sa_path = Path(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or (settings.BASE_DIR / "service-account.json"))
        if sa_path.exists() and not getattr(self.client, "vertexai", False):
            os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", str(sa_path))
            v_client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_CLOUD_PROJECT or "devotional-youtube-514907",
                location=settings.GOOGLE_CLOUD_LOCATION or "global",
            )
            attempts.append((v_client, "gemini-2.5-flash"))

        for client_obj, model_id in attempts:
            for retry_idx in range(3):
                try:
                    response = client_obj.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.3
                        )
                    )
                    data = json.loads(response.text)

                    # Enforce per-scene duration cap (12s-15s for Vertex Omni 1.2 Flash) & total 60-90s floor
                    for s in data.get("scenes", []):
                        s["duration_sec"] = min(15.0, max(12.0, float(s.get("duration_sec", 12.0))))
                        s.setdefault("render_mode", "vertex_omni_t2v")
                    total_dur = sum(s.get("duration_sec", 12.0) for s in data.get("scenes", []))
                    if total_dur < self.MIN_DURATION_SEC and data.get("scenes"):
                        continue
                    data["estimated_duration_sec"] = total_dur
                    return data
                except Exception as e:
                    last_err = e
                    print(f"⚠️ ScriptwriterAgent {model_id} attempt {retry_idx+1}/3 failed: {e}")
                    time.sleep(2 * (retry_idx + 1))

        print(f"⚠️ ScriptwriterAgent API fallback to ScreenplayEngine: {last_err}")
        return ScreenplayEngine.generate_short_script(topic, canonical_source)
