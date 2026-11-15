import pytest
from pathlib import Path
from backend.app.config import settings
from backend.app.modules.visual.providers.mock_provider import MockVisualProvider
from backend.app.modules.voice.tts_engine import HindiVoiceoverEngine
from backend.app.modules.editor.ffmpeg_pipeline import VideoRenderingPipeline

@pytest.mark.asyncio
async def test_visual_and_video_generation(tmp_path):
    provider = MockVisualProvider()
    img_path = tmp_path / "test_frame.jpg"
    vid_path = tmp_path / "test_motion.mp4"

    # 1. Generate Keyframe
    img_res = await provider.generate_scene_image(
        prompt="Lord Shiva with crescent moon",
        output_path=img_path,
        aspect_ratio="9:16",
        resolution=(1080, 1920)
    )
    assert img_res["success"] is True
    assert img_path.exists()
    assert img_path.stat().st_size > 1000

    # 2. Animate Keyframe
    vid_res = await provider.animate_scene(
        image_path=img_path,
        output_video_path=vid_path,
        duration_sec=3.0,
        camera_motion="Cinematic slow push in"
    )
    assert vid_res["success"] is True
    assert vid_path.exists()
    assert vid_path.stat().st_size > 5000

@pytest.mark.asyncio
async def test_voiceover_and_rendering(tmp_path):
    voice_engine = HindiVoiceoverEngine()
    voice_path = tmp_path / "test_voice.aac"

    voice_res = await voice_engine.generate_narration_audio(
        hindi_text="देवाधिदेव महादेव ने तीनों लोकों की रक्षा के लिए हलाहल विष का पान किया।",
        output_audio_path=voice_path,
        target_duration=3.0
    )
    assert voice_res["success"] is True
    assert voice_path.exists()
    assert voice_path.stat().st_size > 1000

    # Test full rendering with video clip and voice track
    provider = MockVisualProvider()
    img_path = tmp_path / "render_frame.jpg"
    vid_path = tmp_path / "render_motion.mp4"
    await provider.generate_scene_image("Mythology test", img_path, "9:16", (1080, 1920))
    await provider.animate_scene(img_path, vid_path, duration_sec=3.0)

    scene_asset = [{
        "scene_index": 1,
        "video_path": str(vid_path),
        "duration_sec": 3.0,
        "narration_hindi": "देवाधिदेव महादेव ने हलाहल विष का पान किया।"
    }]

    render_res = VideoRenderingPipeline.render_complete_video(
        scene_assets=scene_asset,
        voiceover_files=[voice_path],
        job_id="test_render_job",
        format_type="SHORT"
    )
    assert render_res["success"] is True
    final_video = Path(render_res["video_path"])
    assert final_video.exists()
    assert final_video.stat().st_size > 10000
