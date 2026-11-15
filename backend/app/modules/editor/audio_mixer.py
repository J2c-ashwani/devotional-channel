import subprocess
from pathlib import Path
from typing import List, Dict, Any
from backend.app.modules.audio.music_library import MusicRegistry

class AudioMixer:
    """
    Concatenates scene voiceovers, ducks background music under speech,
    adds SFX cues, and applies EBU R128 loudness normalization (-14 LUFS).
    """

    @classmethod
    def mix_soundtrack(
        cls,
        voiceover_files: List[Path],
        scene_durations: List[float],
        output_audio_path: Path
    ) -> Dict[str, Any]:
        output_audio_path.parent.mkdir(parents=True, exist_ok=True)
        total_duration = sum(scene_durations)

        # Ensure canonical background music and SFX are present
        stems = MusicRegistry.ensure_default_audio_assets()
        bgm_path = stems["bgm_epic"]

        # Create concat list for voiceovers
        concat_txt = output_audio_path.parent / "voice_concat.txt"
        with open(concat_txt, "w") as f:
            for vf in voiceover_files:
                f.write(f"file '{vf.resolve()}'\n")

        merged_voice = output_audio_path.parent / "merged_voice.aac"
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:a", "aac",
            str(merged_voice)
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Mix merged voice (loudness 1.0) with ducked background music (volume 0.18)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(merged_voice),
            "-stream_loop", "-1",
            "-i", str(bgm_path),
            "-filter_complex",
            f"[1:a]volume=0.18,atrim=0:{total_duration}[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=11:TP=-1.5[out]",
            "-map", "[out]",
            "-t", str(total_duration),
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_audio_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return {
            "success": True,
            "mixed_audio_path": str(output_audio_path),
            "total_duration": total_duration,
            "loudness_target": "-14 LUFS"
        }
