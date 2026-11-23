import pytest
from backend.app.modules.qc.qc_engine import QualityControlEngine
from backend.app.modules.qc.hard_rules import HardRuleEnforcer
from backend.app.modules.mythology.episodic_ledger import EpisodicLedger

def test_single_shot_duration_hard_blocker():
    """Ensure clips under 60 seconds are blocked from publishing."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000, "duration_sec": 34.0},  # 34s is rushed!
        is_duplicate=False,
        format_type="SHORT"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "below mandatory 60.0s minimum" in qc["hard_blocker_reason"]

def test_single_shot_iconography_hard_blocker():
    """Ensure peacock feather on Prabhu Shri Rama triggers hard blocker."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000, "duration_sec": 65.0},
        is_duplicate=False,
        format_type="SHORT",
        script_data={"full_screenplay_devanagari": "श्री राम के मुकुट पर मयूर पंख चमक रहा था"},
        topic_title="श्री राम का धनुर्भंग"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "peacock feather is strictly prohibited" in qc["hard_blocker_reason"]

def test_single_shot_duplicate_suppression():
    """Ensure previously published episodes are blocked from duplicate re-uploading."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000, "duration_sec": 65.0},
        is_duplicate=True,  # Duplicate!
        format_type="SHORT"
    )
    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert "Duplicate Content Failure" in qc["hard_blocker_reason"]

def test_single_shot_perfect_pass():
    """Ensure complete 65s authentic video passes single-shot QC cleanly."""
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 50000000, "duration_sec": 65.0},
        is_duplicate=False,
        format_type="SHORT",
        director_review={"director_signoff": True, "director_score": 98.0},
        script_data={"full_screenplay_devanagari": "प्रभु श्री राम ने शिवजी के पिनाक धनुष को उठाया"},
        topic_title="श्री राम का धनुर्भंग"
    )
    assert qc["is_passed"] is True
    assert qc["hard_blocker_triggered"] is False
    assert qc["overall_score"] >= 90.0
