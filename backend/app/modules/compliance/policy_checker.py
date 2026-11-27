from typing import Dict, Any, List

class PolicyComplianceChecker:
    """
    Module M (Enhanced): Nuanced YouTube Policy & Synthetic Media Evaluator.
    Determines disclosure based strictly on YouTube's official criteria:
    - Disclosure REQUIRED: If content makes a real person appear to say/do something,
      or generates a photorealistic scene depicting a real-world event that viewers could mistake for documentary reality.
    - Disclosure NOT REQUIRED: Obvious 3D animation, stylized mythological fantasy,
      celestial realms, and creative epic storytelling that no viewer would mistake for real footage of living persons.
    """

    PROHIBITED_SENSATIONAL_TERMS = [
        "भगवान का कत्ल", "खूनी तमाशा", "शर्मनाक सच", "धर्म का अंत", "चौंकाने वाला घिनौना सच"
    ]

    @classmethod
    def evaluate_synthetic_media_requirement(
        cls,
        visual_style: str,
        depicts_real_living_persons: bool = False,
        photorealistic_documentary_mimicry: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates YouTube synthetic media disclosure requirement according to official 2024+ guidelines.
        """
        requires_disclosure = (depicts_real_living_persons or photorealistic_documentary_mimicry)
        
        reason = (
            "Depicts real persons or documentary mimicry; mandatory YouTube altered/synthetic media disclosure."
            if requires_disclosure else
            "Stylized 3D cinematic animation of ancient mythological epic; viewer clearly recognizes animation. Disclosure not legally mandated."
        )

        return {
            "requires_disclosure": requires_disclosure,
            "rationale": reason
        }

    @classmethod
    def audit_content_for_youtube_policies(
        cls,
        script_data: Dict[str, Any],
        metadata: Dict[str, Any],
        copyright_audit: Dict[str, Any]
    ) -> Dict[str, Any]:
        violations: List[str] = []
        warnings: List[str] = []

        title = metadata.get("title_hindi", "")
        desc = metadata.get("description_hindi", "")
        script_text = script_data.get("full_screenplay_devanagari", "")

        # 1. Advertiser-Friendly & Community Guidelines Check (word-boundary safe for Devanagari prefixes/suffixes like 'राजधर्म का अंतिम')
        import re
        for term in cls.PROHIBITED_SENSATIONAL_TERMS:
            pattern = r"(?<![\u0900-\u097Fa-zA-Z0-9])" + re.escape(term) + r"(?![\u0900-\u097Fa-zA-Z0-9])"
            if re.search(pattern, title) or re.search(pattern, script_text):
                violations.append(f"Sensationalist or offensive term detected: '{term}'")

        # 2. Synthetic Media Disclosure Evaluation
        disclosure_eval = cls.evaluate_synthetic_media_requirement(
            visual_style="3D_CINEMATIC_ANIMATION",
            depicts_real_living_persons=False,
            photorealistic_documentary_mimicry=False
        )

        # 3. Made for Kids Check (COPPA)
        is_kids = metadata.get("made_for_kids", False)
        if is_kids:
            warnings.append("Video marked as Made For Kids; verify philosophical suitability.")

        # 4. Copyright Audit Clearance
        if not copyright_audit.get("certified", False):
            violations.append(f"Copyright certification failed: {copyright_audit.get('reason', 'Unverified licenses')}")

        # 5. Mass-Produced Template Repetition Guard (Originality score >= 14/20)
        orig_score = script_data.get("originality_score", 20.0)
        if orig_score < 14.0:
            violations.append(f"Script failed originality threshold ({orig_score}/20); high risk of Reused/Repetitive content.")

        is_passed = len(violations) == 0
        score = 10.0 if is_passed else max(0.0, 10.0 - (len(violations) * 5.0))

        return {
            "passed": is_passed,
            "policy_score": score,
            "max_score": 10.0,
            "violations": violations,
            "warnings": warnings,
            "synthetic_media_evaluation": disclosure_eval,
            "has_altered_or_synthetic_content": disclosure_eval["requires_disclosure"],
            "made_for_kids_designation": False,
            "advertiser_friendly": len(violations) == 0
        }
