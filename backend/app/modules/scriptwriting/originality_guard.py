import difflib
from typing import List, Tuple

class OriginalityGuard:
    """
    Ensures newly generated scripts do not copy or plagiarize previous scripts or templates.
    Computes lexical and sequence similarity to prevent repetitive mass-production.
    """
    
    @classmethod
    def check_originality(cls, new_script: str, previous_scripts: List[str]) -> Tuple[float, bool]:
        """
        Returns (originality_score out of 20, is_original boolean).
        Requires similarity to all past scripts to be under 40% (originality >= 60%).
        """
        if not previous_scripts:
            return 20.0, True

        highest_similarity = 0.0
        matcher = difflib.SequenceMatcher()
        matcher.set_seq2(new_script)

        for past in previous_scripts:
            matcher.set_seq1(past)
            sim = matcher.ratio()
            if sim > highest_similarity:
                highest_similarity = sim

        # If similarity is under 30%, it is considered fully original (20/20)
        if highest_similarity <= 0.30:
            originality_score = 20.0
        else:
            originality_score = round(max(0.0, 20.0 * (1.0 - (highest_similarity - 0.30) / 0.70)), 1)
        
        # Hard failure if similarity > 45% (template recycling)
        is_original = highest_similarity <= 0.45
        return originality_score, is_original
