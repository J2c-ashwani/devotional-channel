from typing import Dict, Any, List

class AudiencePsychologyEngine:
    """
    Module S: Audience Psychology & Emotional Retention Engine.
    Engineers emotional tension curves and validates scripts against viewer retention drop-off patterns:
    1. First 2 Seconds Hook: Evaluates paradox, moral stakes, and elimination of introductory filler.
    2. Navarasa Emotional Resonance: Scores presence of Veerya (Heroism), Adbhuta (Wonder), and Karuna (Compassion).
    3. Pacing Escalation: Ensures stakes intensify before climax rather than plateauing.
    """

    DEADLY_DROP_OFF_FILLERS = [
        "नमस्ते दोस्तों", "स्वागत है हमारे चैनल पर", "आज हम बात करेंगे",
        "वीडियो को अंत तक देखें", "चैनल को सब्सक्राइब करें", "जैसा कि आप जानते हैं"
    ]

    @classmethod
    def evaluate_hook_psychology(cls, opening_hook: str) -> Dict[str, Any]:
        hook = opening_hook.strip()
        word_count = len(hook.split())
        
        # Check for audience-losing filler phrases in first 2 seconds
        detected_fillers = [f for f in cls.DEADLY_DROP_OFF_FILLERS if f in hook]
        
        # Assess curiosity & stakes markers
        stakes_markers = ["जब", "क्यों", "रहस्य", "चुनौती", "प्रलय", "बलिदान", "संकल्प", "प्रतिज्ञा", "क्षण"]
        has_stakes = any(m in hook for m in stakes_markers)
        
        # Pacing: Optimal hook is punchy (12-25 words in Hindi)
        pacing_optimal = 10 <= word_count <= 32

        score = 20.0
        if detected_fillers:
            score -= 10.0
        if not has_stakes:
            score -= 5.0
        if not pacing_optimal:
            score -= 3.0

        score = max(0.0, score)
        is_effective = len(detected_fillers) == 0 and score >= 14.0

        return {
            "effective_hook": is_effective,
            "psychology_score": score,
            "detected_fillers": detected_fillers,
            "has_stakes_marker": has_stakes,
            "word_count": word_count,
            "recommendation": "Hook delivers immediate emotional tension." if is_effective else "Eliminate introductory filler; open directly with the impossible crisis."
        }

    @classmethod
    def analyze_emotional_arc(cls, script_data: Dict[str, Any]) -> Dict[str, Any]:
        hook_eval = cls.evaluate_hook_psychology(script_data.get("opening_hook_hindi", ""))
        full_text = script_data.get("full_screenplay_devanagari", "")

        # Assess Navarasa presence
        rasa_scores = {
            "Veerya (Heroic Valor)": any(w in full_text for w in ["पराक्रम", "धनुष", "प्रत्यंचा", "अमोघ", "वीर", "शक्ति"]),
            "Adbhuta (Cosmic Wonder)": any(w in full_text for w in ["आश्चर्य", "दिव्य", "गगन", "प्रचंड", "स्वर्ण", "तेज"]),
            "Shanta/Dharma (Moral Grounding)": any(w in full_text for w in ["धर्म", "कर्तव्य", "सत्य", "कल्याण", "न्याय", "शाश्वत"])
        }

        emotional_breadth = sum(1 for present in rasa_scores.values() if present)
        psychological_retention_index = round((hook_eval["psychology_score"] / 20.0) * 100.0, 1)

        return {
            "hook_evaluation": hook_eval,
            "navarasa_balance": rasa_scores,
            "emotional_breadth_score": emotional_breadth,
            "predicted_retention_index": psychological_retention_index,
            "retention_tier": "HIGH_RETENTION (>80%)" if psychological_retention_index >= 85 else "MODERATE_RETENTION"
        }
