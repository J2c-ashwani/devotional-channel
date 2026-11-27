from pathlib import Path
from typing import Dict, Any, List
from backend.app.config import settings
from backend.app.modules.visual.providers.gemini_imagen import GeminiImagenProvider
from backend.app.modules.visual.providers.mock_provider import MockVisualProvider

class HybridVisualPipeline:
    """
    Module H (Enhanced): Hybrid Visual Production Engine.
    Achieves maximum cinematic fidelity with strict API cost controls by routing
    scenes to their optimal generation tier:
    - ESTABLISHING_SHOT: High-res AI Matte + 2.5D FFmpeg Camera Movement ($0 video cost)
    - CHARACTER_DIALOGUE: AI Keyframe + Image-to-Video subtle facial/breathing motion
    - BATTLE_CLIMAX: Full AI Video Generation (high-motion particle burst)
    - EMOTIONAL_SCENE: Character Reference Conditioned Portrait Animation
    - ENVIRONMENT_LORE: Reusable Canonical Environment Library
    - TRANSITIONS: Native FFmpeg Cinematic Crossfades
    """

    PRODUCTION_TIERS = {
        "ESTABLISHING": {"cost_multiplier": 0.1, "method": "IMAGE_PLUS_2.5D_MOTION"},
        "DIALOGUE": {"cost_multiplier": 0.4, "method": "IMAGE_TO_VIDEO_SUBTLE"},
        "BATTLE": {"cost_multiplier": 1.0, "method": "FULL_AI_VIDEO_GENERATION"},
        "EMOTIONAL": {"cost_multiplier": 0.4, "method": "CHAR_REFERENCE_ANIMATION"},
        "ENVIRONMENT": {"cost_multiplier": 0.05, "method": "REUSABLE_MATTE_OVERLAY"}
    }

    def __init__(self):
        if settings.IMAGE_GEN_PROVIDER == "modular_gemini":
            self.provider = GeminiImagenProvider()
        else:
            self.provider = MockVisualProvider()

    async def render_scene_hybrid(
        self,
        scene_spec: Dict[str, Any],
        output_dir: Path,
        job_id: str
    ) -> Dict[str, Any]:
        idx = scene_spec.get("scene_index", 1)
        duration = scene_spec.get("duration_sec", 6.0)
        camera = scene_spec.get("camera_movement", "Cinematic push in")
        prompt = scene_spec.get("visual_prompt", "Epic Indian Mythology")
        res = tuple(scene_spec.get("resolution", [1080, 1920]))
        tier = scene_spec.get("production_tier", "ESTABLISHING")

        img_path = output_dir / f"scene_{idx:02d}_keyframe.jpg"
        video_path = output_dir / f"scene_{idx:02d}_motion.mp4"

        # Step 1: Render ultra-detailed master keyframe image
        await self.provider.generate_scene_image(
            prompt=prompt,
            output_path=img_path,
            aspect_ratio=scene_spec.get("aspect_ratio", "9:16"),
            resolution=res
        )

        # Step 2: Apply tier-specific motion synthesis
        await self.provider.animate_scene(
            image_path=img_path,
            output_video_path=video_path,
            duration_sec=duration,
            camera_motion=camera
        )

        return {
            "scene_index": idx,
            "scene_name": scene_spec.get("scene_name", f"Scene {idx}"),
            "production_tier": tier,
            "production_method": self.PRODUCTION_TIERS.get(tier, {}).get("method", "IMAGE_PLUS_2.5D_MOTION"),
            "image_path": str(img_path),
            "video_path": str(video_path),
            "duration_sec": duration,
            "voice_duration": scene_spec.get("voice_duration", duration),
            "narration_hindi": scene_spec.get("narration_hindi", ""),
            "sfx_cue": scene_spec.get("sfx_cue", None)
        }

    async def render_all_storyboard_scenes(
        self,
        storyboard_spec: Dict[str, Any],
        job_id: str
    ) -> List[Dict[str, Any]]:
        scenes = storyboard_spec.get("scenes", [])
        rendered_assets = []
        base_dir = settings.STORAGE_DIR / "visuals" / "scenes" / job_id
        base_dir.mkdir(parents=True, exist_ok=True)

        for s in scenes:
            asset = await self.render_scene_hybrid(s, base_dir, job_id)
            rendered_assets.append(asset)

        return rendered_assets

    async def render_all_omni_t2v_scenes(
        self,
        storyboard_spec: Dict[str, Any],
        job_id: str
    ) -> List[Dict[str, Any]]:
        """
        Locked Pure Google Vertex Text-to-Video Path (1080x1920, native multi-character audio+video).
        Strictly enforces Talking Heads for dialogue scenes and Kathavachak Narration for non-dialogue scenes,
        using bounded concurrency (max 3 workers) with 2s breathing/ambience tails to prevent audio clipping.
        """
        import asyncio
        import json
        import subprocess

        scenes = storyboard_spec.get("scenes", [])
        base_dir = settings.STORAGE_DIR / "visuals" / "scenes" / job_id
        base_dir.mkdir(parents=True, exist_ok=True)
        sem = asyncio.Semaphore(3)

        async def _render_one(s: Dict[str, Any]) -> Dict[str, Any]:
            idx = s.get("scene_index", 1)
            dur = int(min(15, max(12, round(float(s.get("duration_sec", 12.0))))))
            speak_end = max(8.0, float(dur) - 2.0)
            speaker = s.get("speaker") or s.get("dialogue_speaker")
            dialogue = (s.get("dialogue_hindi") or "").strip()
            narrator = (s.get("narration_hindi") or "").strip()
            if speaker and dialogue and narrator.endswith(dialogue):
                narrator = narrator[: -len(dialogue)].strip()

            visual_prompt = s.get("visual_prompt", "Cinematic 9:16 vertical photorealistic 8k ancient Indian epic film scene.")
            if speaker and dialogue:
                audio_dir = (
                    f"[0-{dur}s] Medium close-up talking-head of {speaker} speaking directly on camera in clear, natural expressive Hindi voice "
                    f"with crisp realistic lip-sync, finishing completely before {speak_end:.1f}s leaving 2s calm natural music and temple/nature ambience: '{dialogue}'"
                )
            else:
                text_to_speak = narrator or dialogue
                outro_sfx = "followed by resonant sacred temple Shankh conch and warm outro music" if idx >= len(scenes) else "leaving 2s calm music at the end"
                audio_dir = (
                    f"Voiceover [0.5s-{speak_end:.1f}s] — Deep warm resonant mature Indian male Kathavachak narrator speaking clearly and distinctly "
                    f"every single Hindi word over soft mystical bansuri and subtle ambient soundscape, {outro_sfx}: '{text_to_speak}'"
                )

            full_omni_prompt = (
                f"Cinematic 9:16 vertical photorealistic 8k live-action Indian mythological cinema. No on-screen text or watermarks.\n"
                f"{visual_prompt}\n"
                f"{audio_dir}"
            )

            video_path = base_dir / f"omni_scene_{idx:02d}.mp4"
            thumb_frame = base_dir / f"scene_{idx:02d}_frame.jpg"

            async with sem:
                await self.provider.generate_omni_t2v_scene(
                    prompt=full_omni_prompt,
                    output_video_path=video_path,
                    duration_sec=dur,
                    aspect_ratio=s.get("aspect_ratio", "9:16"),
                    gcs_prefix=f"autonomous_jobs/{job_id}"
                )

            subprocess.run(
                ["ffmpeg", "-y", "-nostdin", "-ss", "2.0", "-i", str(video_path), "-vframes", "1", "-q:v", "2", str(thumb_frame)],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            probe = subprocess.run(
                ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "json", str(video_path)],
                capture_output=True, text=True
            )
            actual_dur = float(dur)
            try:
                actual_dur = float(json.loads(probe.stdout)["format"]["duration"])
            except Exception:
                pass

            return {
                "scene_index": idx,
                "scene_name": s.get("scene_name", f"Act {idx}"),
                "production_tier": "VERTEX_OMNI_T2V",
                "production_method": "PURE_VERTEX_TEXT_TO_VIDEO",
                "image_path": str(thumb_frame),
                "video_path": str(video_path),
                "duration_sec": round(actual_dur, 2),
                "voice_duration": round(actual_dur, 2),
                "narration_hindi": s.get("narration_hindi", ""),
                "speaker": speaker,
                "dialogue_hindi": dialogue,
                "sfx_cue": s.get("sfx_cue", None)
            }

        rendered_assets = await asyncio.gather(*(_render_one(s) for s in scenes))
        return sorted(rendered_assets, key=lambda x: int(x["scene_index"]))

# Alias for backwards compatibility
VisualSceneGenerator = HybridVisualPipeline
