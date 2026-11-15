import pytest
from backend.app.modules.director.production_director import AutomatedProductionDirector
from backend.app.modules.psychology.audience_psychology import AudiencePsychologyEngine
from backend.app.modules.recovery.recovery_engine import AutonomousRecoveryEngine
from backend.app.modules.mythology.source_library import SourceLibrary
from backend.app.modules.mythology.fact_checker import MythologyFactChecker
from backend.app.modules.scriptwriting.originality_guard import OriginalityGuard

def test_production_director_review():
    mock_scenes = [
        {"scene_index": 1, "duration_sec": 6.0, "camera_movement": "Wide slow push in", "visual_prompt": "Wide ancient Mithila palace"},
        {"scene_index": 2, "duration_sec": 8.0, "camera_movement": "Medium shot", "visual_prompt": "Lord Rama standing serenely"},
        {"scene_index": 3, "duration_sec": 10.0, "camera_movement": "Dynamic rotational orbit", "visual_prompt": "Divine Pinaka bow breaking with cosmic radiant power"},
        {"scene_index": 4, "duration_sec": 6.0, "camera_movement": "Slow wide pullback", "visual_prompt": "Mithila celebration"}
    ]
    review = AutomatedProductionDirector.review_storyboard_direction(mock_scenes)
    assert review["approved"] is True
    assert review["director_score"] >= 80.0
    assert review["director_signoff"] == "PASSED"

def test_audience_psychology_hook_evaluation():
    # Strong hook
    strong_hook = "राजा जनक की भरी सभा में जब पांच हजार बलिष्ठ पुरुष भी जिस शिव धनुष को हिला न सके—तब महर्षि विश्वामित्र ने श्री राम की ओर देखा!"
    eval_strong = AudiencePsychologyEngine.evaluate_hook_psychology(strong_hook)
    assert eval_strong["effective_hook"] is True
    assert eval_strong["psychology_score"] >= 15.0

    # Weak hook with drop-off filler
    weak_hook = "नमस्ते दोस्तों, आज के इस वीडियो में हम बात करेंगे कि राम जी ने धनुष कैसे तोड़ा।"
    eval_weak = AudiencePsychologyEngine.evaluate_hook_psychology(weak_hook)
    assert eval_weak["effective_hook"] is False
    assert len(eval_weak["detected_fillers"]) > 0

def test_autonomous_recovery_checkpoints(tmp_path):
    job_id = "test_recovery_job_99"
    payload = {"step": "research_complete", "topic": "Dhanurbhanga"}
    
    # Save checkpoint
    saved_path = AutonomousRecoveryEngine.save_checkpoint(job_id, "01_RESEARCH", payload)
    assert saved_path.exists()

    # Load checkpoint
    loaded = AutonomousRecoveryEngine.load_last_checkpoint(job_id)
    assert loaded is not None
    assert loaded["payload"]["topic"] == "Dhanurbhanga"

    # Clean up
    AutonomousRecoveryEngine.clear_job_checkpoints(job_id)

def test_ramayana_pilot_scriptural_grounding():
    topic = "श्री राम का धनुर्भंग: जब मिथिला में शिव का पिनाक धनुष टूटा"
    source = SourceLibrary.get_canonical_source(topic)
    assert source is not None
    assert "Valmiki Ramayana" in source["epic_name"]
    assert "Bala Kanda" in source["kanda_or_parva"]
    assert "Sarga 66" in source["sarga_or_adhyaya"]

    script_text = (
        "राजा जनक की सभा में जब विश्वामित्र ने आज्ञा दी, तो श्री राम ने उस पिनाक धनुष को "
        "क्षण मात्र में उठा लिया। प्रत्यंचा चढ़ाते ही धनुष मध्य से टूट गया।"
    )
    fact_audit = MythologyFactChecker.validate_script(script_text, topic)
    assert fact_audit["passed"] is True
    assert fact_audit["hard_blocker"] is False
    assert len(fact_audit["verified_assertions"]) > 0

def test_enhanced_originality_guard_with_history():
    new_script = "समुद्र लंघन के समय हनुमान जी ने मैनाक पर्वत को विश्राम का विनम्र अस्वीकार किया।"
    new_hook = "जब सौ योजन विशाल महासागर के ऊपर पवनपुत्र हनुमान ने छलांग लगाई—तो पाताल से मैनाक पर्वत उठ खड़ा हुआ!"
    
    audit = OriginalityGuard.audit_script_originality(new_script, new_hook)
    assert audit["passed"] is True
    assert audit["originality_score"] >= 15.0
