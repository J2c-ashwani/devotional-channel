from pathlib import Path
from typing import Dict, Any, List
from backend.app.config import settings
from backend.app.modules.visual.providers.gemini_imagen import GeminiImagenProvider
from backend.app.modules.visual.providers.mock_provider import MockVisualProvider

class VisualSceneGenerator:
    """
    Module H: Cinematic Visual & Animation Generation Engine.
    Converts storyboard scenes into rendered image keyframes and video clips.
    """

    def __init__(self):
        if settings.IMAGE_GEN_PROVIDER == "modular_gemini":
            self.provider = GeminiImagenProvider()
        else:
            self.provider = MockVisualProvider()

    async def render_all_storyboard_scenes(
        self,
        storyboard_spec: Dict[str, Any],
        job_id: str
    ) -> List[Dict[str, Any]]:
        scenes = storyboard_spec.get("scenes", [])
        rendered_assets = []
        base_dir = settings.STORAGE_DIR / "visuals" / "scenes" / job_id
        base_dir.mkdir(parents=True, exist_ok=True)

        for scene in scenes:
            idx = scene.get("scene_index", 1)
            duration = scene.get("duration_sec", 6.0)
            camera = scene.get("camera_movement", "Cinematic push in")
            prompt = scene.get("visual_prompt", "Epic Indian Mythology")
            res = tuple(scene.get("resolution", [1080, 1920]))

            img_path = base_dir / f"scene_{idx:02d}_keyframe.jpg"
            video_path = base_dir / f"scene_{idx:02d}_motion.mp4"

            # 1. Generate keyframe image
            img_result = await self.provider.generate_scene_image(
                prompt=prompt,
                output_path=img_path,
                aspect_ratio=scene.get("aspect_ratio", "9:16"),
                resolution=res
            )

            # 2. Animate keyframe image into video
            video_result = await self.provider.animate_scene(
                image_path=img_path,
                output_video_path=video_path,
                duration_sec=duration,
                camera_motion=camera
            )

            rendered_assets.append({
                "scene_index": idx,
                "scene_name": scene.get("scene_name", f"Scene {idx}"),
                "image_path": str(img_path),
                "video_path": str(video_path),
                "duration_sec": duration,
                "narration_hindi": scene.get("narration_hindi", ""),
                "sfx_cue": scene.get("sfx_cue", None)
            })

        return rendered_assets
