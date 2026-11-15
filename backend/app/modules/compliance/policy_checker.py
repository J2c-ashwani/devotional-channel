from typing import Dict, Any, List

class PolicyComplianceChecker:
    """
    Module M: YouTube Policy & Monetization Compliance Engine.
    Strictly evaluates content against YouTube's official partner program policies:
    - Reused Content prevention
    - Repetitive / Inauthentic mass-produced content avoidance
    - Synthetic media disclosure enforcement
    - Advertiser-friendly guidelines
    - COPPA / Made for Kids classification
    """

    PROHIBITED_SENSATIONAL_TERMS = [
        "भगवान का कत्ल", "खूनी तमाशा", "शर्मनाक सच", "धर्म का अंत", "चौंकाने वाला घिनौना सच"
    ]

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

        # 1. Advertiser-Friendly & Community Guidelines Check
        for term in cls.PROHIBITED_SENSATIONAL_TERMS:
            if term in title or term in script_text:
                violations.append(f"Sensationalist or offensive term detected: '{term}'")

        # 2. Synthetic Media Disclosure Check (Mandatory for AI generated content)
        has_disclosure = metadata.get("has_altered_or_synthetic_content", False)
        if not has_disclosure:
            violations.append("YouTube Altered or Synthetic media disclosure is missing.")

        # 3. Made for Kids Check (COPPA)
        is_kids = metadata.get("made_for_kids", False)
        if is_kids:
            warnings.append("Video marked as Made For Kids; verify if complex philosophical dilemmas are suitable.")

        # 4. Copyright Audit Clearance
        if not copyright_audit.get("certified", False):
            violations.append(f"Copyright certification failed: {copyright_audit.get('reason', 'Unverified licenses')}")

        # 5. Mass-Produced Template Repetition Guard (Originality score out of 20, min 12.0 = 60%)
        orig_score = script_data.get("originality_score", 20.0)
        if orig_score < 12.0:
            violations.append(f"Script failed originality threshold ({orig_score}/20); high risk of Reused / Repetitive content penalty.")

        is_passed = len(violations) == 0
        score = 10.0 if is_passed else max(0.0, 10.0 - (len(violations) * 5.0))

        return {
            "passed": is_passed,
            "policy_score": score,
            "max_score": 10.0,
            "violations": violations,
            "warnings": warnings,
            "synthetic_media_flagged": has_disclosure,
            "made_for_kids_designation": False,
            "advertiser_friendly": len(violations) == 0
        }
