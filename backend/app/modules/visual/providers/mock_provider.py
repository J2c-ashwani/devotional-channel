import os
import subprocess
from pathlib import Path
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageFont
from backend.app.modules.visual.providers.base import VisualGenerationProvider

class MockVisualProvider(VisualGenerationProvider):
    """
    Generates high-definition aesthetic keyframes and smooth animated video clips using Pillow & FFmpeg.
    Employs pan/zoom cinematic camera motion (Ken Burns effect).
    Zero API cost, fully reproducible for testing, development, and fallback.
    """

    async def generate_scene_image(
        self,
        prompt: str,
        output_path: Path,
        aspect_ratio: str = "9:16",
        resolution: tuple = (1080, 1920)
    ) -> Dict[str, Any]:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        width, height = resolution
        
        # Create rich gradient background (cosmic divine gold/blue/indigo)
        img = Image.new("RGB", (width, height), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)
        
        # Draw dramatic atmospheric cosmic aura
        center_x, center_y = width // 2, height // 2
        for r in range(min(width, height) // 2, 0, -20):
            alpha_color = (
                int(20 + (255 - 20) * (1 - r / (min(width, height) / 2))),
                int(40 + (180 - 40) * (1 - r / (min(width, height) / 2))),
                int(80 + (240 - 80) * (1 - r / (min(width, height) / 2)))
            )
            draw.ellipse(
                [center_x - r, center_y - r, center_x + r, center_y + r],
                fill=alpha_color
            )
            
        # Draw sacred geometric mandala / aura lines
        draw.ellipse([center_x - 220, center_y - 220, center_x + 220, center_y + 220], outline=(255, 215, 0), width=4)
        draw.ellipse([center_x - 180, center_y - 180, center_x + 180, center_y + 180], outline=(255, 165, 0), width=2)
        
        # Add cinematic title overlay
        draw.text(
            (width // 2, height - 200),
            "PAURANIK GATHA CINEMATIC STUDIOS",
            fill=(255, 255, 255),
            anchor="ms"
        )
        draw.text(
            (width // 2, height - 160),
            "Sacred Indian Mythology Visual Sequence",
            fill=(255, 215, 0),
            anchor="ms"
        )
        
        img.save(output_path, "JPEG", quality=95)
        return {
            "success": True,
            "provider": "mock_visual_hd",
            "file_path": str(output_path),
            "width": width,
            "height": height
        }

    async def animate_scene(
        self,
        image_path: Path,
        output_video_path: Path,
        duration_sec: float,
        camera_motion: str = "Cinematic slow push in"
    ) -> Dict[str, Any]:
        output_video_path.parent.mkdir(parents=True, exist_ok=True)
        fps = 30
        frames = int(duration_sec * fps)
        
        # Use FFmpeg zoompan filter to generate cinematic animated motion
        # Slow zoom in: zoom starts at 1.0 and increases smoothly
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-vf", f"zoompan=z='min(zoom+0.0015,1.25)':d={frames}:s=1080x1920:fps={fps}",
            "-t", str(duration_sec),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            str(output_video_path)
        ]
        
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            # Fallback to direct static frame encoding if zoompan encounters dimension quirks
            fallback_cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(image_path),
                "-t", str(duration_sec),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                str(output_video_path)
            ]
            subprocess.run(fallback_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        return {
            "success": True,
            "provider": "mock_motion_engine",
            "video_path": str(output_video_path),
            "duration": duration_sec,
            "camera_motion": camera_motion
        }
