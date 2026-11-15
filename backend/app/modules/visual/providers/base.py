from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path

class VisualGenerationProvider(ABC):
    """
    Abstract Base Class for Image and Animation Generation Providers.
    Allows hot-swapping providers (Gemini Imagen, Flux, Midjourney API, Runway, Pika, or Mock)
    without rewriting the production pipeline.
    """

    @abstractmethod
    async def generate_scene_image(
        self,
        prompt: str,
        output_path: Path,
        aspect_ratio: str = "9:16",
        resolution: tuple = (1080, 1920)
    ) -> Dict[str, Any]:
        """Generates a keyframe image for a scene."""
        pass

    @abstractmethod
    async def animate_scene(
        self,
        image_path: Path,
        output_video_path: Path,
        duration_sec: float,
        camera_motion: str = "Cinematic slow push in"
    ) -> Dict[str, Any]:
        """Animates a keyframe image into a dynamic video clip."""
        pass
