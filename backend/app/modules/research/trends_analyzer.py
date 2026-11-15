import json
from datetime import datetime
from typing import List, Dict, Any
from backend.app.config import settings

class TrendsAnalyzer:
    """
    Analyzes search trends, queries, and seasonal festival alignment for Hindi Indian Mythology.
    """
    
    SEED_DISCOVERY_TOPICS = [
        {
            "title_hindi": "भगवान शिव का नीलकंठ अवतार: जब हलाहल विष ने सृष्टि को हिला दिया",
            "title_english": "Neelkanth: When Lord Shiva Drank the Cosmic Poison (Samudra Manthan)",
            "epic_source": "Shiva Purana / Bhagavata Purana",
            "format_type": "SHORT",
            "search_volume": 85000,
            "competition_count": 12,
            "underexplored_aspect": "The specific cosmic dilemma and why even devas could not withstand the venom fumes",
            "keywords": ["neelkanth", "samudra manthan", "shiva purana", "shiv katha in hindi", "vishaanu"],
            "deity": "Lord Shiva"
        },
        {
            "title_hindi": "महाभारत का सबसे बड़ा रहस्य: घटोत्कच का अंतिम बलिदान और कर्ण की विवशता",
            "title_english": "The Sacrifice of Ghatotkacha and the Destiny of Karna's Vasava Shakti",
            "epic_source": "Mahabharata - Drona Parva",
            "format_type": "SHORT",
            "search_volume": 92000,
            "competition_count": 15,
            "underexplored_aspect": "Krishna's strategic grief and why Ghatotkacha had to fall to save Arjuna",
            "keywords": ["ghatotkacha", "karna vasava dart", "mahabharat katha", "kurukshetra night battle", "krishna strategy"],
            "deity": "Lord Krishna"
        },
        {
            "title_hindi": "वाल्मीकि रामायण का रहस्य: जब मेघनाद ने इंद्र को बंदी बना लिया था",
            "title_english": "How Meghanada Defeated Indra and Earned the Title Indrajit",
            "epic_source": "Valmiki Ramayana - Uttara Kanda",
            "format_type": "SHORT",
            "search_volume": 78000,
            "competition_count": 8,
            "underexplored_aspect": "Brahmadeva's boons and the secret celestial rituals performed in Nikumbhila",
            "keywords": ["meghanada", "indrajit", "valmiki ramayana", "ravana son", "nikumbhila yajna"],
            "deity": "Lord Rama"
        },
        {
            "title_hindi": "कुरुक्षेत्र का १८वां दिन: भीष्म की शरशैया और धर्मराज युधिष्ठिर को राजधर्म का अंतिम उपदेश",
            "title_english": "Bhishma's Bed of Arrows: The Ultimate Discourse on Rajadharma and Moksha",
            "epic_source": "Mahabharata - Shanti Parva",
            "format_type": "LONG_FORM",
            "search_volume": 120000,
            "competition_count": 18,
            "underexplored_aspect": "In-depth moral dilemmas of justice, governance, and why Draupadi laughed at Bhishma's words",
            "keywords": ["bhishma sharshayya", "shanti parva", "rajadharma", "yudhishthir bhishma samvad", "mahabharat hindi"],
            "deity": "Lord Krishna"
        },
        {
            "title_hindi": "महाकाल की महागाथा: समुद्र मंथन से लेकर द्वादश ज्योतिर्लिंगों की संपूर्ण अमर कथा",
            "title_english": "The Eternal Lore of Mahakaal: From Cosmic Ocean Churning to the 12 Jyotirlingas",
            "epic_source": "Shiva Purana - Koti Rudra Samhita",
            "format_type": "MONTHLY_SPECIAL",
            "search_volume": 250000,
            "competition_count": 22,
            "underexplored_aspect": "Comprehensive cinematic multi-act retelling linking each sacred shrine to human consciousness",
            "keywords": ["12 jyotirlinga story in hindi", "shiva purana full documentary", "mahakaal katha", "rudra samhita"],
            "deity": "Lord Shiva"
        }
    ]

    def __init__(self):
        with open(settings.CONFIG_DIR / "channel_profile.json", "r", encoding="utf-8") as f:
            self.channel_profile = json.load(f)

    def detect_seasonal_festival_boost(self, deity: str) -> int:
        festivals = self.channel_profile.get("cultural_festivals", [])
        for fest in festivals:
            if deity.lower() in fest.get("deity", "").lower() or fest.get("deity", "").lower() in deity.lower():
                return fest.get("priority_boost", 15)
        return 0

    def get_candidate_topics(self) -> List[Dict[str, Any]]:
        candidates = []
        for item in self.SEED_DISCOVERY_TOPICS:
            boost = self.detect_seasonal_festival_boost(item.get("deity", ""))
            candidate = dict(item)
            candidate["festival_boost"] = boost
            candidate["detected_at"] = datetime.utcnow().isoformat()
            candidates.append(candidate)
        return candidates
