from pathlib import Path
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageFont
from backend.app.config import settings

class ThumbnailGenerator:
    """
    Module L: Thumbnail Generation Engine.
    Creates high-CTR mobile-optimized thumbnails with high contrast,
    clean subject focal points, and punchy Hindi typography.
    """

    @classmethod
    def create_thumbnail(
        cls,
        topic_title_hindi: str,
        output_path: Path,
        aspect_ratio: str = "16:9", # Thumbnails are 16:9 for YouTube (1280x720)
        source_keyframe: Path = None
    ) -> Dict[str, Any]:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        width, height = (1280, 720)

        if source_keyframe and source_keyframe.exists():
            img = Image.open(source_keyframe).convert("RGB")
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        else:
            img = Image.new("RGB", (width, height), color=(15, 23, 42))
            draw = ImageDraw.Draw(img)
            # Radiant golden/crimson sunburst gradient
            for r in range(450, 0, -25):
                color = (
                    int(180 * (1 - r / 450) + 30),
                    int(50 * (1 - r / 450) + 15),
                    int(20 * (1 - r / 450) + 15)
                )
                draw.ellipse([640 - r, 360 - r, 640 + r, 360 + r], fill=color)

        draw = ImageDraw.Draw(img)

        # Draw dark bottom banner for high-contrast legible Hindi text
        draw.rectangle([0, height - 180, width, height], fill=(0, 0, 0, 200))
        draw.rectangle([0, height - 185, width, height - 180], fill=(255, 215, 0)) # Golden accent line

        # Add punchy concise headline
        headline = topic_title_hindi[:45] + ("..." if len(topic_title_hindi) > 45 else "")
        draw.text(
            (width // 2, height - 110),
            headline,
            fill=(255, 255, 255),
            anchor="mm"
        )
        
        # Sub-badge
        draw.text(
            (width // 2, height - 50),
            "॥ पौराणिक गाथा - सत्य ऐतिहासिक रहस्य ॥",
            fill=(255, 215, 0),
            anchor="mm"
        )

        img.save(output_path, "JPEG", quality=95)
        return {
            "success": True,
            "thumbnail_path": str(output_path),
            "resolution": (width, height)
        }
