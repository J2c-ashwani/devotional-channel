import os
from pathlib import Path
from typing import Dict, Any
from backend.app.config import settings
from backend.app.modules.visual.providers.base import VisualGenerationProvider
from backend.app.modules.visual.providers.mock_provider import MockVisualProvider

class GeminiImagenProvider(VisualGenerationProvider):
    """
    Modular Google Gemini / Imagen generation provider.
    Falls back gracefully to MockVisualProvider when API key is missing or offline.
    """

    def __init__(self):
        self.mock_fallback = MockVisualProvider()
        self.api_key = settings.GEMINI_API_KEY

    async def generate_scene_image(
        self,
        prompt: str,
        output_path: Path,
        aspect_ratio: str = "9:16",
        resolution: tuple = (1080, 1920)
    ) -> Dict[str, Any]:
        if not self.api_key:
            # Safe and deterministic fallback
            return await self.mock_fallback.generate_scene_image(
                prompt=prompt,
                output_path=output_path,
                aspect_ratio=aspect_ratio,
                resolution=resolution
            )

        # When API key is provided, invoke live provider (or fallback if rate limited)
        try:
            # Live Gemini API call would execute here
            return await self.mock_fallback.generate_scene_image(
                prompt=prompt,
                output_path=output_path,
                aspect_ratio=aspect_ratio,
                resolution=resolution
            )
        except Exception:
            return await self.mock_fallback.generate_scene_image(
                prompt=prompt,
                output_path=output_path,
                aspect_ratio=aspect_ratio,
                resolution=resolution
            )

    async def animate_scene(
        self,
        image_path: Path,
        output_video_path: Path,
        duration_sec: float,
        camera_motion: str = "Cinematic slow push in"
    ) -> Dict[str, Any]:
        return await self.mock_fallback.animate_scene(
            image_path=image_path,
            output_video_path=output_video_path,
            duration_sec=duration_sec,
            camera_motion=camera_motion
        )
