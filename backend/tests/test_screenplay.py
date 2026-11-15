import pytest
from backend.app.modules.scriptwriting.screenplay_engine import ScreenplayEngine
from backend.app.modules.scriptwriting.originality_guard import OriginalityGuard
from backend.app.modules.mythology.source_library import SourceLibrary

def test_screenplay_generation_shorts():
    topic = {"title_hindi": "भगवान शिव का नीलकंठ अवतार: जब हलाहल विष ने सृष्टि को हिला दिया"}
    source = SourceLibrary.get_canonical_source(topic["title_hindi"])
    script = ScreenplayEngine.generate_short_script(topic, source)

    assert script["format"] == "SHORT"
    assert len(script["opening_hook_hindi"]) > 20
    assert len(script["climax_hindi"]) > 20
    assert len(script["conclusion_hindi"]) > 20
    assert 30 <= script["estimated_duration_sec"] <= 60
    assert "नीलकंठ" in script["full_screenplay_devanagari"]

def test_screenplay_generation_longform():
    topic = {"title_hindi": "कुरुक्षेत्र का १८वां दिन: भीष्म की शरशैया और धर्मराज युधिष्ठिर का संवाद"}
    source = SourceLibrary.get_canonical_source(topic["title_hindi"])
    script = ScreenplayEngine.generate_longform_script(topic, source)

    assert script["format"] == "LONG_FORM"
    assert script["estimated_duration_sec"] >= 480
    assert "भीष्म" in script["full_screenplay_devanagari"]
    assert len(script["dialogue_excerpts"]) > 0

def test_originality_guard():
    script1 = "जब क्षीरसागर के मंथन से अमृत नहीं, बल्कि कालकूट विष निकला तो देवता कांप उठे।"
    script2 = "कुरुक्षेत्र की 14वीं रात जब घटोत्कच ने अपनी माया से हाहाकार मचाया।"
    score, is_orig = OriginalityGuard.check_originality(script2, [script1])
    assert is_orig is True
    assert score >= 15.0

    # Test exact duplicate
    score_dup, is_orig_dup = OriginalityGuard.check_originality(script1, [script1])
    assert is_orig_dup is False
    assert score_dup == 0.0
