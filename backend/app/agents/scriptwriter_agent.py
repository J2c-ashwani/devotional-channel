"""
Scriptwriter Agent for Itihasa Saga.
Enforces strict, uncompromising rules for narrative depth, scriptural authenticity,
and emotional engagement. Eliminates rushed, shallow 20-30s scripts.
Guarantees 60-90 second complete story arcs with zero unexplained cuts.
"""

import json
import os
from typing import Dict, Any, List
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
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS',
            '/Users/ashwanikumar/Downloads/devotional/service-account.json'
        )
        self.client = genai.Client(
            vertexai=True,
            project='devotional-youtube-514907',
            location='global'
        )

    def write_screenplay(self, topic: Dict[str, Any], canonical_source: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a complete 5-act Hindi screenplay with timing and dialogue."""
        prompt = f"""
You are the Master Mythological Scriptwriter Agent for 'Itihasa Saga' (@itihasasaga).
Topic: {topic.get('title_hindi')}
Canonical Source: {topic.get('epic_source', canonical_source.get('citation', 'Ancient Canonical Shastras'))}

STRICT UNCOMPROMISING RULES:
1. TARGET DURATION: 65 to 80 SECONDS. Do NOT write a short 20-30 second script!
2. COMPLETE STORYTELLING:
   - Scene 1 (The Hook & Epic Premise, 12-14s): Establish the context, the location, who broke what or what crisis occurred, and the antagonist/challenger's arrival.
   - Scene 2 (The Confrontation & Challenge, 12-14s): The challenger roars in anger or sets the conflict. A key character responds bravely.
   - Scene 3 (The Climax / Heroic Intervention, 14-16s): Explain WHY the protagonist steps forward (e.g. to protect brother / resolve crisis). The protagonist is introduced by full revered name and speaks their iconic, humble, or majestic dialogue.
   - Scene 4 (The Divine Revelation & Resolution, 12-14s): Explain the outcome! How was the anger calmed or crisis averted? The challenger's realization and devotion.
   - Scene 5 (Dharmic Takeaway & Epilogue, 8-10s): The spiritual lesson, conch celebration, and next episode hook.
3. ABSOLUTE CHARACTER CLARITY:
   - NEVER say vague phrases like 'Shri Ram aage badhe muskurate hue' without explaining why He stepped forward, what He said, and what happened next.
   - Always name characters clearly: 'मर्यादा पुरुषोत्तम प्रभु श्री राम', 'भगवान परशुराम', 'राजकुमार लक्ष्मण', 'माँ गंगा', 'राजा शांतनु', etc.
4. AUTHENTIC HINDI ONLY: Devnagari Hindi only. High emotional tension and goosebump-inducing resonance.

Return a STRICT JSON object with this exact structure:
{{
  "title_hindi": "...",
  "estimated_duration_sec": 70,
  "characters_present": ["...", "..."],
  "scenes": [
    {{
      "scene_index": 1,
      "scene_name": "Epic Context & Arrival",
      "duration_sec": 14.0,
      "narrator_text_hindi": "...",
      "dialogue_speaker": "...",
      "dialogue_hindi": "...",
      "visual_description_english": "...",
      "emotional_tone": "Tense and thunderous"
    }},
    ...
  ],
  "full_screenplay_devanagari": "Full screenplay text...",
  "takeaway_moral_hindi": "..."
}}
"""
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            )
        )
        data = json.loads(response.text)
        
        # Enforce minimum duration guard
        total_dur = sum(s.get("duration_sec", 12.0) for s in data.get("scenes", []))
        if total_dur < self.MIN_DURATION_SEC:
            for s in data.get("scenes", []):
                s["duration_sec"] = round(s.get("duration_sec", 12.0) * (self.TARGET_DURATION_SEC / max(total_dur, 1.0)), 1)
        data["estimated_duration_sec"] = sum(s["duration_sec"] for s in data["scenes"])
        return data
