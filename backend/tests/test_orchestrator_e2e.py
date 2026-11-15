import pytest
from pathlib import Path
from backend.app.pipeline.orchestrator import ProductionPipelineOrchestrator
from backend.app.pipeline.emergency import EmergencyKillSwitch
from backend.app.modules.scriptwriting.originality_guard import OriginalityGuard

@pytest.fixture(autouse=True)
def clean_test_ledger():
    OriginalityGuard.clear_history()
    yield
    OriginalityGuard.clear_history()

@pytest.mark.asyncio
async def test_end_to_end_shorts_pipeline():
    orchestrator = ProductionPipelineOrchestrator()
    result = await orchestrator.execute_production_run(
        format_type="SHORT",
        simulate_upload=True
    )

    assert result["success"] is True
    assert result["status"] == "SCHEDULED"
    assert result["qc_score"] >= 90.0
    assert "video_path" in result
    assert Path(result["video_path"]).exists()
    assert Path(result["thumbnail_path"]).exists()
    assert result["youtube"]["success"] is True
    assert "yt_" in result["youtube"]["youtube_video_id"]
    assert "13:30:00Z" in result["youtube"]["scheduled_publish_at_utc"] # 19:00 IST

@pytest.mark.asyncio
async def test_end_to_end_longform_pipeline():
    orchestrator = ProductionPipelineOrchestrator()
    result = await orchestrator.execute_production_run(
        format_type="LONG_FORM",
        forced_topic={
            "id": "topic_bhishma",
            "title_hindi": "कुरुक्षेत्र का १८वां दिन: भीष्म की शरशैया और धर्मराज युधिष्ठिर को राजधर्म का अंतिम उपदेश",
            "title_english": "Bhishma's Bed of Arrows: The Ultimate Discourse on Rajadharma",
            "epic_source": "Mahabharata",
            "format_type": "LONG_FORM"
        },
        simulate_upload=True,
        scene_duration_override=3.0
    )

    assert result["success"] is True
    assert result["status"] == "SCHEDULED"
    assert result["qc_score"] >= 90.0
    assert Path(result["video_path"]).exists()

@pytest.mark.asyncio
async def test_emergency_kill_switch_blocks_production():
    EmergencyKillSwitch.activate("Testing safety freeze")
    orchestrator = ProductionPipelineOrchestrator()
    result = await orchestrator.execute_production_run(format_type="SHORT")
    assert result["success"] is False
    assert result["status"] == "HALTED"
    EmergencyKillSwitch.deactivate()
