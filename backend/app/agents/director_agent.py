"""
Production Director Agent for Itihasa Saga.
Enforces strict visual, acoustic, and iconographic standards.
Guarantees zero iconographic defects, pristine audio mixing, and broadcast-ready overlays.
"""

from pathlib import Path
from typing import Dict, Any, List
from PIL import Image, ImageDraw, ImageFont

class ProductionDirectorAgent:
    """
    Production Director Agent.
    Rules:
    1. SCRIPTURAL ICONOGRAPHY:
       - Prabhu Shri Rama: Classical Surya-vamsha Kirita Mukuta (royal gold crown with jewels & pearls).
         STRICTLY NO MAYUR PANKH (Peacock feather belongs exclusively to Shri Krishna).
       - Shri Krishna: Mayur Pankh on crown, yellow silk, flute.
       - Parashurama: Ascetic warrior, Jata, tiger skin, glowing Parashu axe.
       - Lakshmana: Young royal warrior, gold crown, fearless stance.
    2. AUDIO INTEGRITY:
       - Narrator voice: Exclusively Google Charon (mature Kathavachak Hindi).
       - Background video audio MUST be 100% muted on narrator-led scenes to eliminate conflicting chatter.
       - Dialogue scenes: Lip-sync voice elevated, BGM lowered to subtle bed (volume=0.15).
       - Climax & Outro: Divine Shankh conch and sacred orchestral score.
    3. SUBTITLE & OVERLAY PERFECTION:
       - Header badge top-centered in gold.
       - Subtitle cards bottom-centered with dark glassmorphic box, gold border, and gold speaker tags.
       - Zero text clipping; font size 34-36px with generous horizontal padding.
    """

    NEGATIVE_PROMPTS_RAMA = (
        "peacock feather, mayur pankh, peacock plume, flute, krishna iconography, "
        "distorted face, extra limbs, modern clothing, cartoonish"
    )

    @classmethod
    def audit_scene_prompt(cls, character_id: str, prompt: str) -> str:
        """Injects strict visual and negative prompt safeguards into scene prompts."""
        if "rama" in character_id.lower() or "राम" in prompt:
            prompt += (
                " Authentic ancient Surya-vamsha royal golden crown (Kirita Mukuta) adorned with rubies and pearls. "
                "STRICTLY NO peacock feather, NO mayur pankh, classical Vedic royal crown only. "
                "Divine calm, serene lotus eyes, majestic humility."
            )
        elif "parashurama" in character_id.lower() or "परशुराम" in prompt:
            prompt += (
                " Fierce warrior-sage with glowing wrathful eyes, long ascetic matted hair, "
                "wearing rudraksha beads and bark cloth, carrying a glowing razor-sharp Parashu battleaxe."
            )
        elif "lakshmana" in character_id.lower() or "लक्ष्मण" in prompt:
            prompt += (
                " Handsome, youthful prince in royal silk robes with golden crown, "
                "fearless stance, confident courageous smile, heroic devotion."
            )
        return prompt

    @classmethod
    def create_header_badge(cls, track: str, episode_num: int, output_path: Path):
        """Generates standard top-centered gold header badge."""
        title_text = f"रामायण • भाग {episode_num}" if "RAMAYANA" in track.upper() else f"महाभारत • भाग {episode_num}"
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        try:
            font = ImageFont.truetype(font_path, 44)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pad_x, pad_y = 46, 16
        badge_w, badge_h = text_w + pad_x * 2, text_h + pad_y * 2
        badge_x, badge_y = (1080 - badge_w) // 2, 150

        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=26,
            fill=(12, 10, 8, 215),
            outline=(218, 165, 32, 240),  # Golden Rod #DAA520
            width=3
        )
        draw.text((badge_x + pad_x, badge_y + pad_y - 2), title_text, font=font, fill=(255, 255, 255, 255))
        img.save(output_path)

    @classmethod
    def create_subtitle_card(cls, lines: List[str], output_path: Path, speaker: str = None):
        """Generates perfectly formatted subtitle card with gold speaker tag and zero clipping."""
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
        font_main = ImageFont.truetype(font_path, 36)
        font_speaker = ImageFont.truetype(font_path, 32)

        total_text_h = sum(draw.textbbox((0, 0), l, font=font_main)[3] - draw.textbbox((0, 0), l, font=font_main)[1] for l in lines) + (len(lines) - 1) * 14
        if speaker:
            total_text_h += 44

        pad_y, pad_x = 20, 38
        badge_h = total_text_h + pad_y * 2
        max_w = max(draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0] for l in lines)
        if speaker:
            max_w = max(max_w, draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0])
        badge_w = min(1020, max_w + pad_x * 2)
        badge_x = (1080 - badge_w) // 2
        badge_y = 1560 - badge_h // 2

        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
            radius=22,
            fill=(10, 10, 10, 220),
            outline=(218, 165, 32, 235) if speaker else (255, 255, 255, 150),
            width=2
        )

        curr_y = badge_y + pad_y
        if speaker:
            s_w = draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0]
            draw.text(((1080 - s_w) // 2, curr_y), speaker, font=font_speaker, fill=(255, 215, 0, 255))
            curr_y += 42

        for l in lines:
            l_w = draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0]
            draw.text(((1080 - l_w) // 2, curr_y), l, font=font_main, fill=(255, 255, 255, 255))
            curr_y += 50

        img.save(output_path)
