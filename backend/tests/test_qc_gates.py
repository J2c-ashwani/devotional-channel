import pytest
from backend.app.modules.qc.qc_engine import QualityControlEngine

def test_qc_pass_clean_production():
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": True, "score": 20.0, "hard_blocker": False},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000},
        is_duplicate=False
    )

    assert qc["is_passed"] is True
    assert qc["overall_score"] >= 90.0
    assert qc["hard_blocker_triggered"] is False
    assert qc["status"] == "APPROVED"

def test_qc_fail_closed_on_hard_blocker():
    # Hallucination or factual contradiction triggers hard blocker
    qc = QualityControlEngine.audit_production(
        research_score=19.0,
        factual_result={"passed": False, "score": 0.0, "hard_blocker": True, "blocker_reason": "Invented scriptural conversation"},
        script_originality=20.0,
        visual_result={"success": True},
        audio_result={"success": True},
        copyright_result={"certified": True, "score": 10.0},
        policy_result={"passed": True, "policy_score": 10.0},
        render_result={"success": True, "file_size_bytes": 500000},
        is_duplicate=False
    )

    assert qc["is_passed"] is False
    assert qc["hard_blocker_triggered"] is True
    assert qc["status"] == "QUARANTINED"
    assert "Invented scriptural conversation" in qc["hard_blocker_reason"]
