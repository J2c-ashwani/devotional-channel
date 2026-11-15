import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any
from backend.app.config import settings
from backend.app.modules.editor.subtitle_generator import SubtitleGenerator
from backend.app.modules.editor.audio_mixer import AudioMixer

class VideoRenderingPipeline:
    """
    Module K: Automatic Video Editor & Rendering Engine using FFmpeg.
    Assembles video clips, synchronized voiceover, ducked music, subtitles,
    and applies color grading and loudness normalization.
    """

    @classmethod
    def render_complete_video(
        cls,
        scene_assets: List[Dict[str, Any]],
        voiceover_files: List[Path],
        job_id: str,
        format_type: str = "SHORT"
    ) -> Dict[str, Any]:
        render_dir = settings.STORAGE_DIR / "rendered" / job_id
        render_dir.mkdir(parents=True, exist_ok=True)

        target_res = (1080, 1920) if format_type == "SHORT" else (1920, 1080)
        output_video_path = render_dir / f"final_{format_type.lower()}_{job_id}.mp4"
        output_srt_path = render_dir / f"subtitles_{job_id}.srt"
        mixed_audio_path = render_dir / f"master_soundtrack_{job_id}.aac"

        # 1. Generate Subtitles
        SubtitleGenerator.generate_srt(scene_assets, output_srt_path)

        # 2. Mix Audio
        durations = [s.get("duration_sec", 6.0) for s in scene_assets]
        AudioMixer.mix_soundtrack(voiceover_files, durations, mixed_audio_path)

        # 3. Concatenate Scene Video Clips
        video_concat_txt = render_dir / "video_concat.txt"
        with open(video_concat_txt, "w") as f:
            for s in scene_assets:
                vpath = Path(s["video_path"]).resolve()
                f.write(f"file '{vpath}'\n")

        # Color grading filter: slight warm saturation (+10%) and subtle contrast (+5%) for mythological richness
        color_filter = "eq=contrast=1.05:brightness=0.01:saturation=1.12"

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(video_concat_txt),
            "-i", str(mixed_audio_path),
            "-vf", color_filter,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video_path)
        ]

        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 4. Technical Validation of Rendered File
        validation = cls.validate_rendered_video(output_video_path, target_res)
        if not validation["valid"]:
            raise RuntimeError(f"Video rendering failed technical validation: {validation['error']}")

        return {
            "success": True,
            "video_path": str(output_video_path),
            "subtitles_path": str(output_srt_path),
            "resolution": target_res,
            "duration_sec": validation["duration"],
            "file_size_bytes": output_video_path.stat().st_size
        }

    @classmethod
    def validate_rendered_video(cls, video_path: Path, expected_resolution: tuple) -> Dict[str, Any]:
        if not video_path.exists() or video_path.stat().st_size == 0:
            return {"valid": False, "error": "Video file is missing or 0 bytes."}

        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_streams", "-show_format",
            str(video_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            return {"valid": False, "error": "ffprobe failed to read video file."}

        try:
            data = json.loads(res.stdout)
            format_info = data.get("format", {})
            duration = float(format_info.get("duration", 0.0))
            streams = data.get("streams", [])
            has_video = any(s.get("codec_type") == "video" for s in streams)
            has_audio = any(s.get("codec_type") == "audio" for s in streams)
        except Exception as e:
            return {"valid": False, "error": f"Error parsing video streams: {str(e)}"}

        if not has_video:
            return {"valid": False, "error": "Rendered video has no video stream."}
        if not has_audio:
            return {"valid": False, "error": "Rendered video has no audio stream."}
        if duration <= 2.0:
            return {"valid": False, "error": f"Video duration ({duration}s) too short."}

        return {
            "valid": True,
            "duration": round(duration, 2),
            "streams": len(streams),
            "error": None
        }
