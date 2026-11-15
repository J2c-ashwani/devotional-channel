import pytest
from backend.app.modules.mythology.source_library import SourceLibrary
from backend.app.modules.mythology.fact_checker import MythologyFactChecker
from backend.app.modules.mythology.pronunciation import PronunciationManager

def test_canonical_source_lookup():
    source = SourceLibrary.get_canonical_source("भगवान शिव का नीलकंठ अवतार")
    assert source is not None
    assert "Shiva Purana" in source["epic_name"]
    assert source["public_domain_certified"] is True

def test_fact_check_valid_script():
    valid_script = (
        "समुद्र मंथन के समय जब महाविनाशक कालकूट हलाहल विष प्रकट हुआ, "
        "तो भगवान शिव ने तीनों लोकों की रक्षा हेतु विष का पान किया और नीलकंठ कहलाए।"
    )
    result = MythologyFactChecker.validate_script(valid_script, "भगवान शिव का नीलकंठ अवतार")
    assert result["passed"] is True
    assert result["hard_blocker"] is False
    assert result["score"] >= 15.0

def test_fact_check_hallucination_detection():
    # Intentionally insert a prohibited historical hallucination
    corrupted_script = (
        "कुरुक्षेत्र के युद्ध में कर्ण ने अर्जुन को कुरुक्षेत्र में मार दिया और विजय पाई।"
    )
    result = MythologyFactChecker.validate_script(corrupted_script, "घटोत्कच")
    assert result["passed"] is False
    assert result["hard_blocker"] is True
    assert "contradiction" in result["blocker_reason"].lower()

def test_pronunciation_manager():
    mgr = PronunciationManager()
    processed = mgr.apply_pronunciation_rules("दशरथ और कौशल्या ने विश्वामित्र का स्वागत किया।")
    assert "दशरथ" in processed
    assert "कौशल्या" in processed
