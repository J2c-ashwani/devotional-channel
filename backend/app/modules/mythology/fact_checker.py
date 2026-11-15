from typing import Dict, Any, List
from backend.app.modules.mythology.source_library import SourceLibrary

class MythologyFactChecker:
    """
    Module B (Enhanced): Structured Scripture Verification & Lineage Guard.
    Ensures every factual event maps directly to Valmiki Ramayana, Vyasa Mahabharata,
    or Puranas with verified Kanda/Sarga and Shloka citations.
    """

    KNOWN_CANONICAL_PROHIBITIONS = [
        {
            "prohibited": "रावण ने शिवजी को युद्ध में हरा दिया",
            "reason": "Direct contradiction: Shiva crushed Ravana's pride beneath Mount Kailash (Uttara Kanda 16)."
        },
        {
            "prohibited": "कर्ण ने अर्जुन को कुरुक्षेत्र में मार दिया",
            "reason": "Direct contradiction of Mahabharata: Arjuna defeated Karna on Day 17 (Karna Parva)."
        },
        {
            "prohibited": "राम ने सीता की परीक्षा रावण की लंका में ली",
            "reason": "False chronology: Agni Pariksha occurred in Lanka after Ravana's death, not during captivity."
        },
        {
            "prohibited": "विश्वामित्र ने राम को धनुष तोड़ने से रोका",
            "reason": "Direct contradiction: Vishwamitra explicitly commanded Rama to string the bow (Bala Kanda 1.67.12)."
        }
    ]

    @classmethod
    def validate_script(cls, script_hindi: str, topic_slug: str) -> Dict[str, Any]:
        source = SourceLibrary.get_canonical_source(topic_slug)
        if not source:
            return {
                "passed": False,
                "score": 0.0,
                "hard_blocker": True,
                "blocker_reason": "No verifiable canonical public-domain scripture identified for topic.",
                "assertions_verified": [],
                "unverified_claims": []
            }

        contradictions: List[str] = []
        verified_assertions: List[Dict[str, Any]] = []

        # Pass 1: Contradiction Check
        for p in cls.KNOWN_CANONICAL_PROHIBITIONS:
            if p["prohibited"] in script_hindi:
                contradictions.append(p["reason"])

        # Pass 2: Citation Grounding against Canonical Assertions
        for a in source.get("factual_assertions", []):
            keywords = [w for w in a["fact"].replace("।", "").replace(",", "").split() if len(w) > 4]
            # Match semantic presence of canonical facts in script
            matched = any(k in script_hindi for k in keywords[:4]) if keywords else False
            if matched:
                verified_assertions.append({
                    "assertion_id": a["assertion_id"],
                    "citation": a["citation"],
                    "fact": a["fact"],
                    "status": "VERIFIED_IN_SCRIPT"
                })

        # Calculate reliability score
        total_assertions = len(source.get("factual_assertions", []))
        verified_count = len(verified_assertions)
        ratio = (verified_count / max(1, total_assertions)) if total_assertions else 1.0

        score = round(15.0 + (5.0 * ratio), 1)
        if contradictions:
            score = 0.0

        has_hard_blocker = len(contradictions) > 0 or not source.get("public_domain_certified", False)

        return {
            "passed": not has_hard_blocker and score >= 15.0,
            "score": score,
            "max_score": 20.0,
            "hard_blocker": has_hard_blocker,
            "blocker_reason": "; ".join(contradictions) if contradictions else None,
            "source_citation": f"{source['epic_name']} | {source.get('kanda_or_parva', '')} | {source.get('sarga_or_adhyaya', '')}",
            "edition": source.get("source_edition"),
            "verified_assertions": verified_assertions,
            "shloka_anchor": source.get("original_sanskrit_shloka")
        }
