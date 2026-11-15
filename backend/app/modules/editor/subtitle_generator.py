from pathlib import Path
from typing import List, Dict, Any

class SubtitleGenerator:
    """
    Generates SRT and ASS format synchronized Hindi subtitles for YouTube videos.
    """

    @classmethod
    def format_time_srt(cls, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    @classmethod
    def generate_srt(cls, scenes: List[Dict[str, Any]], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        current_time = 0.0
        lines = []
        
        for i, scene in enumerate(scenes, 1):
            dur = scene.get("duration_sec", 6.0)
            text = scene.get("narration_hindi", "").strip()
            if not text:
                current_time += dur
                continue
                
            start_str = cls.format_time_srt(current_time)
            end_str = cls.format_time_srt(current_time + dur)
            
            lines.append(f"{i}")
            lines.append(f"{start_str} --> {end_str}")
            lines.append(text)
            lines.append("")
            
            current_time += dur
            
        output_path.write_text("\n".join(lines), encoding="utf-8")
        return output_path
