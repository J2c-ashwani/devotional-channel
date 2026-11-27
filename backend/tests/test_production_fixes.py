import json
import subprocess
from pathlib import Path
from unittest.mock import patch
import pytest

from backend.app.config import settings
from backend.app.modules.cost.budget_guard import BudgetGuard
from backend.app.modules.cost.tracker import CostTracker
from backend.app.modules.editor.ffmpeg_pipeline import VideoRenderingPipeline
from backend.app.modules.formats.longform_planner import LongformPlanner
from backend.app.modules.mythology.source_library import SourceLibrary
from backend.app.modules.scriptwriting.originality_guard import OriginalityGuard
from backend.app.modules.scriptwriting.screenplay_engine import ScreenplayEngine
from backend.app.modules.youtube.uploader import YouTubeUploader
from backend.app.pipeline.orchestrator import ProductionPipelineOrchestrator


@pytest.mark.asyncio
async def test_live_upload_fails_closed_without_credentials(tmp_path):
    """Issue 1: Live upload (simulate_upload=False) must NEVER fake success when unconfigured."""
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"fake_mp4_bytes")
    srt = tmp_path / "sample.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:02,000\nनमस्ते\n", encoding="utf-8")

    uploader = YouTubeUploader()
    uploader.client_id = "mock_client_id"
    uploader.client_secret = "mock_client_secret"
    uploader.refresh_token = "mock_refresh_token"

    res = await uploader.upload_and_schedule_video(
        video_path=video,
        thumbnail_path=None,
        metadata={"title_hindi": "Test", "description_hindi": "Desc", "tags": ["test"]},
        subtitles_path=srt,
        simulate_upload=False,
    )
    assert res["success"] is False
    assert res["simulated"] is False
    assert "youtube_video_id" not in res
    assert res["has_subtitles"] is True


@pytest.mark.asyncio
async def test_live_upload_fails_closed_on_api_error(tmp_path):
    """Issue 1: Live upload API exception must NOT fall back to a simulated yt_ ID."""
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"fake_mp4_bytes")

    uploader = YouTubeUploader()
    uploader.client_id = "real_client_id"
    uploader.client_secret = "real_client_secret"
    uploader.refresh_token = "1//0gRealLookingRefreshToken1234567890"

    with patch.object(uploader, "_execute_live_upload_sync", side_effect=RuntimeError("quotaExceeded")):
        res = await uploader.upload_and_schedule_video(
            video_path=video,
            thumbnail_path=None,
            metadata={"title_hindi": "Test", "description_hindi": "Desc", "tags": ["test"]},
            simulate_upload=False,
        )
    assert res["success"] is False
    assert res["simulated"] is False
    assert "quotaExceeded" in res["error"]


@pytest.mark.asyncio
async def test_live_upload_executes_and_uploads_subtitles(tmp_path):
    """Issue 1 & 5: Live upload succeeds only when _execute_live_upload_sync succeeds and passes subtitles."""
    video = tmp_path / "sample.mp4"
    video.write_bytes(b"fake_mp4_bytes")
    srt = tmp_path / "sample.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:02,000\nजय श्री राम\n", encoding="utf-8")

    uploader = YouTubeUploader()
    uploader.client_id = "real_client_id"
    uploader.client_secret = "real_client_secret"
    uploader.refresh_token = "1//0gRealLookingRefreshToken1234567890"

    fake_live = {
        "video_id": "dQw4w9WgXcQ",
        "thumbnail_uploaded": True,
        "thumbnail_error": None,
        "subtitles_uploaded": True,
        "subtitles_error": None,
    }
    with patch.object(uploader, "_execute_live_upload_sync", return_value=fake_live) as mock_live:
        res = await uploader.upload_and_schedule_video(
            video_path=video,
            thumbnail_path=None,
            metadata={"title_hindi": "Test", "description_hindi": "Desc", "tags": ["test"]},
            subtitles_path=srt,
            simulate_upload=False,
        )
    mock_live.assert_called_once()
    assert mock_live.call_args[0][2] == srt
    assert res["success"] is True
    assert res["simulated"] is False
    assert res["youtube_video_id"] == "dQw4w9WgXcQ"
    assert res["subtitles_uploaded"] is True


@pytest.mark.asyncio
async def test_fact_checker_catches_contradiction_in_generated_script(tmp_path, monkeypatch):
    """Issue 2: Fact check must run AFTER screenplay generation and quarantine scripts with prohibited claims."""
    monkeypatch.setattr(settings, "STORAGE_DIR", tmp_path)
    OriginalityGuard.clear_history()

    bad_script = {
        "id": "script_bad_01",
        "format": "SHORT",
        "opening_hook_hindi": "विश्वामित्र ने राम को धनुष तोड़ने से रोका और सभा में सन्नाटा छा गया।",
        "narrative_body_hindi": "सभा के राजा स्तब्ध थे।",
        "climax_hindi": "श्री राम ने धनुष उठाया।",
        "conclusion_hindi": "मर्यादा की विजय हुई।",
        "dialogue_excerpts": [],
        "full_screenplay_devanagari": "विश्वामित्र ने राम को धनुष तोड़ने से रोका।",
        "estimated_duration_sec": 45,
    }

    orchestrator = ProductionPipelineOrchestrator()
    orchestrator.scriptwriter = None
    with patch.object(ScreenplayEngine, "generate_short_script", return_value=bad_script):
        res = await orchestrator.execute_production_run(format_type="SHORT", simulate_upload=True)

    assert res["success"] is False
    assert res["status"] == "QUARANTINED"
    assert "Fact-Checking Failure" in (res.get("hard_blocker") or "")
    OriginalityGuard.clear_history()


def test_budget_guard_persists_and_enforces_monthly_spend(tmp_path, monkeypatch):
    """Issue 3: CostTracker persists job spend and BudgetGuard blocks once ceiling is exceeded."""
    monkeypatch.setattr(settings, "STORAGE_DIR", tmp_path)
    monkeypatch.setattr(settings, "MONTHLY_BUDGET_USD", 10.0)

    assert CostTracker.get_monthly_spend() == 0.0
    assert BudgetGuard.check_budget_availability(estimated_new_job_cost=0.50)["allowed"] is True

    CostTracker.record_job_cost("job_1", "LONG_FORM", {"total_cost_usd": 6.50, "breakdown": {}}, "SCHEDULED")
    CostTracker.record_job_cost("job_2", "LONG_FORM", {"total_cost_usd": 3.20, "breakdown": {}}, "SCHEDULED")

    assert CostTracker.get_monthly_spend() == pytest.approx(9.70, abs=1e-4)
    blocked = BudgetGuard.check_budget_availability(estimated_new_job_cost=0.50)
    assert blocked["allowed"] is False
    assert blocked["current_spend_usd"] == pytest.approx(9.70, abs=1e-4)


def test_longform_script_and_planner_do_not_truncate_and_hit_target_duration():
    """Issue 4: Longform planner preserves full narration (no [:150] slice) and meets 8-15 min target."""
    for topic in [
        {"title_hindi": "कुरुक्षेत्र का १८वां दिन: भीष्म की शरशैया और धर्मराज युधिष्ठिर का संवाद"},
        {"title_hindi": "श्री राम का धनुर्भंग: जब मिथिला में शिव का पिनाक धनुष टूटा"},
    ]:
        source = SourceLibrary.get_canonical_source(topic["title_hindi"])
        script = ScreenplayEngine.generate_longform_script(topic, source)
        storyboard = LongformPlanner.create_storyboard_spec(script, {})

        assert storyboard["total_scenes"] >= 8
        assert 480.0 <= storyboard["estimated_duration_sec"] <= 900.0
        assert script["estimated_duration_sec"] >= 480.0
        combined_narration = " ".join(s["narration_hindi"] for s in storyboard["scenes"])
        assert len(combined_narration) > 4000
        # Ensure body wasn't truncated to 150 chars
        assert script["narrative_body_hindi"][-40:] in combined_narration


def test_ffmpeg_embeds_subtitle_stream_in_final_mp4(tmp_path, monkeypatch):
    """Issue 5: Final MP4 must contain embedded Hindi subtitles (and burned-in if libass is available)."""
    monkeypatch.setattr(settings, "STORAGE_DIR", tmp_path)

    # Create a real 3-second test video and 3-second WAV voiceover via FFmpeg
    clip_path = tmp_path / "scene_01.mp4"
    voice_path = tmp_path / "voice_01.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=3",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip_path)
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "3",
        "-c:a", "pcm_s16le", str(voice_path)
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    render_res = VideoRenderingPipeline.render_complete_video(
        scene_assets=[{
            "scene_index": 1,
            "video_path": str(clip_path),
            "duration_sec": 3.0,
            "voice_duration": 2.5,
            "narration_hindi": "प्रभु श्री राम ने सहजता से पिनाक धनुष उठा लिया।",
        }],
        voiceover_files=[voice_path],
        job_id="test_subs_job",
        format_type="SHORT",
    )

    assert render_res["success"] is True
    assert render_res["subtitles_embedded"] is True
    assert Path(render_res["subtitles_path"]).exists()

    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", render_res["video_path"]],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    streams = json.loads(probe.stdout)["streams"]
    sub_streams = [s for s in streams if s.get("codec_type") == "subtitle"]
    assert len(sub_streams) == 1
    assert sub_streams[0].get("codec_name") == "mov_text"
