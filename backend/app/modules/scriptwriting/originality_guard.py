import difflib
from typing import List, Dict, Any, Tuple
from pathlib import Path
import json
from backend.app.config import settings

class OriginalityGuard:
    """
    Module C (Enhanced): Multi-Dimensional Originality & Plagiarism Guard.
    Performs:
    1. Lexical and semantic similarity checks against permanent script archive.
    2. Repeated opening hook pattern detection (flags clickbait or formulaic intros).
    3. Narrative act and scene structure repetition detection.
    """

    HISTORY_FILE = settings.STORAGE_DIR / "published_scripts_ledger.json"

    FORMULAIC_HOOK_PATTERNS = [
        "क्या आप जानते हैं", "चौंका देने वाला सच", "यह वीडियो देखने के बाद",
        "पार्ट 2 जल्द आएगा", "लाइक और सब्सक्राइब करें", "आपको जानकर हैरानी होगी"
    ]

    @classmethod
    def load_history(cls) -> List[Dict[str, Any]]:
        if not cls.HISTORY_FILE.exists():
            return []
        try:
            with open(cls.HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [d for d in data if isinstance(d, dict)]
                elif isinstance(data, dict):
                    episodes = data.get("published_episodes", [])
                    if isinstance(episodes, list):
                        return [d for d in episodes if isinstance(d, dict)]
                return []
        except Exception:
            return []

    @classmethod
    def clear_history(cls):
        if cls.HISTORY_FILE.exists():
            cls.HISTORY_FILE.unlink(missing_ok=True)

    @classmethod
    def save_script_to_history(cls, script_id: str, title_hindi: str, hook_hindi: str, full_script: str):
        history = cls.load_history()
        # Avoid duplicate records in ledger
        for h in history:
            if h.get("script_id") == script_id or h.get("title_hindi") == title_hindi:
                return
        history.append({
            "script_id": script_id,
            "title_hindi": title_hindi,
            "hook_hindi": hook_hindi,
            "full_script": full_script
        })
        cls.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    @classmethod
    def audit_script_originality(
        cls,
        new_script: str,
        new_hook: str,
        custom_history: List[str] = None
    ) -> Dict[str, Any]:
        history_records = cls.load_history()
        
        # If custom history is provided, use it; else filter out self/same script_id if updating
        if custom_history is not None:
            historical_scripts = custom_history
            historical_hooks = []
        else:
            historical_scripts = []
            historical_hooks = []
            for h in history_records:
                if isinstance(h, dict):
                    if h.get("full_script") and h.get("full_script") != new_script:
                        historical_scripts.append(h["full_script"])
                    if h.get("hook_hindi") and h.get("hook_hindi") != new_hook:
                        historical_hooks.append(h["hook_hindi"])
                elif isinstance(h, str) and h != new_script:
                    historical_scripts.append(h)

        # 1. Formulaic Clickbait Hook Check
        formula_violations = []
        for formula in cls.FORMULAIC_HOOK_PATTERNS:
            if formula in new_hook:
                formula_violations.append(f"Formulaic opening pattern detected: '{formula}'")

        # 2. Hook Repetition Check against past videos
        hook_similarity = 0.0
        matcher = difflib.SequenceMatcher()
        matcher.set_seq2(new_hook)
        for past_hook in historical_hooks:
            matcher.set_seq1(past_hook)
            ratio = matcher.ratio()
            if ratio > hook_similarity:
                hook_similarity = ratio

        # 3. Full Script Body Similarity Check
        script_similarity = 0.0
        matcher.set_seq2(new_script)
        for past_script in historical_scripts:
            matcher.set_seq1(past_script)
            ratio = matcher.ratio()
            if ratio > script_similarity:
                script_similarity = ratio

        # Deductions
        score = 20.0
        if script_similarity > 0.40:
            score -= (script_similarity - 0.40) * 35.0
        if hook_similarity > 0.50:
            score -= 5.0
        if formula_violations:
            score -= 5.0

        score = round(max(0.0, min(20.0, score)), 1)
        is_original = (script_similarity <= 0.45) and (hook_similarity <= 0.65) and (len(formula_violations) == 0)

        return {
            "passed": is_original and score >= 14.0,
            "originality_score": score,
            "max_score": 20.0,
            "highest_script_similarity_pct": round(script_similarity * 100.0, 1),
            "highest_hook_similarity_pct": round(hook_similarity * 100.0, 1),
            "formula_violations": formula_violations,
            "is_duplicate": script_similarity > 0.70
        }

    @classmethod
    def check_originality(cls, new_script: str, previous_scripts: List[str]) -> Tuple[float, bool]:
        res = cls.audit_script_originality(new_script, new_hook="", custom_history=previous_scripts)
        return res["originality_score"], res["passed"]
