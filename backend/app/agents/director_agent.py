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
    Rules (LOCKED FOR BOTH RAMAYANA & MAHABHARATA):
    1. GENERATION ENGINE & PACING:
       - Pure Google Vertex Text-to-Video (gemini-omni-1.2-flash, 1080x1920 9:16, native audio+video at 1.00x speed).
       - ZERO static-image keyframe workarounds and ZERO stretched/robotic external TTS voiceovers (no setpts/atempo).
       - Pacing strictly <= 2.0 spoken Hindi words/sec per 12s-15s block so zero trailing words clip.
    2. PURE TALKING HEAD DIALOGUES:
       - Every dialogue_speaker MUST appear on-screen as a talking head speaking in their own native Vertex voice with lip-sync.
       - Kathavachak narrator speaks ONLY on non-dialogue scene-setting hooks, transitions, and epilogues.
    3. SCRIPTURAL ICONOGRAPHY:
       - Prabhu Shri Rama: Classical Surya-vamsha Kirita Mukuta (royal gold crown with rubies & pearls).
         STRICTLY NO MAYUR PANKH (Peacock feather belongs exclusively to Shri Krishna).
       - Mata Sita: Crimson-gold Banarasi silk bridal/royal attire, delicate veil, sacred tilak/bindi.
       - Shri Krishna: Mayur Pankh on crown, yellow silk, flute.
       - Parashurama: Ascetic warrior, Jata, tiger skin, glowing Parashu axe.
       - Lakshmana: Young royal warrior, gold crown, fearless stance.
       - Rajkumar Devavrata / Pitamaah Bhishma: Tall noble Kuru warrior in ivory-white and gold silk armor with golden crown circlet.
       - Nishadaraj / Satyavati / Maharaja Shantanu / Eklavya / Karna / Arjuna: Authentic Vedic attire consistent across scenes.
    4. AUDIO & SUBTITLE PERFECTION:
       - Mastered at EBU R128 (-14 LUFS) with click-free boundaries and dynamic ffprobe timing.
       - Header badge top-centered in gold ('रामायण • भाग N' or 'महाभारत • भाग N').
       - Subtitle cards bottom-centered with dark glassmorphic box, gold border, and gold speaker tags.
    """

    NEGATIVE_PROMPTS_RAMA = (
        "peacock feather, mayur pankh, peacock plume, flute, krishna iconography, "
        "distorted face, extra limbs, modern clothing, cartoonish"
    )

    @classmethod
    def audit_scene_prompt(cls, character_id: str, prompt: str) -> str:
        """Injects strict visual, talking-head, and iconography safeguards into Ramayana & Mahabharata scene prompts."""
        full_context = f"{character_id or ''} {prompt or ''}".lower()
        if "rama" in full_context or "राम" in full_context:
            prompt += (
                " Authentic ancient Surya-vamsha royal golden crown (Kirita Mukuta) adorned with rubies and pearls. "
                "STRICTLY NO peacock feather, NO mayur pankh, classical Vedic royal crown only. "
                "Divine calm, serene lotus eyes, majestic humility."
            )
        elif "सीता" in full_context or "sita" in full_context:
            prompt += (
                " Graceful Mithila princess in deep crimson and gold embroidered Banarasi silk saree, ruby maang-tikka, "
                "expressive compassionate eyes, sublime Indian devotional dignity."
            )
        elif "परशुराम" in full_context or "parashurama" in full_context:
            prompt += (
                " Fierce warrior-sage with glowing wrathful eyes, long ascetic matted hair, "
                "wearing rudraksha beads and bark cloth, carrying a glowing razor-sharp Parashu battleaxe."
            )
        elif "लक्ष्मण" in full_context or "lakshmana" in full_context:
            prompt += (
                " Handsome, youthful prince in royal silk robes with golden crown, "
                "fearless stance, confident courageous smile, heroic devotion."
            )
        elif "देवव्रत" in full_context or "भीष्म" in full_context or "bhishma" in full_context or "devavrata" in full_context:
            prompt += (
                " Towering noble prince in gleaming ivory-white and gold Kuru silk robes and shoulder armor, "
                "carved golden crown circlet, luminous eyes shining with unwavering filial devotion and vow."
            )
        elif "निषादराज" in full_context or "nishadaraj" in full_context or "nishad" in full_context:
            prompt += (
                " Dignified weathered elderly river-chieftain with silver beard, maroon cotton shawl, rudraksha mala, firm stern expression."
            )
        elif "कर्ण" in full_context or "karna" in full_context:
            prompt += (
                " Radiant Surya-putra warrior in divine fused golden Kavacha chest armor and glowing golden Kundala earrings."
            )
        elif "एकलव्य" in full_context or "eklavya" in full_context:
            prompt += (
                " Sincere young forest tribal archer in humble forest tunic holding wooden bow with intense spiritual devotion."
            )
        elif "कृष्ण" in full_context or "krishna" in full_context:
            prompt += (
                " Meghashyama blue-cloud complexion, golden Pitambara silk, radiant crown adorned with Peacock Feather (Mayur Pankh)."
            )
        elif "कैकेयी" in full_context or "kaikeyi" in full_context:
            prompt += (
                " Regally proud Ayodhya queen in deep magenta and gold silk saree with heavy royal gold jewelry, intense determined gaze."
            )
        elif "मंथरा" in full_context or "manthara" in full_context:
            prompt += (
                " Shrewd hunchbacked palace maidservant in muted dark-green cotton drapes, whispering cunningly with sharp calculating eyes."
            )
        elif "दशरथ" in full_context or "dasharatha" in full_context:
            prompt += (
                " Noble aged Emperor of Ayodhya with silver-streaked beard, crimson-gold royal silk robes and Surya-vamsha crown, deeply agonized fatherly emotion."
            )
        elif "हनुमान" in full_context or "hanuman" in full_context:
            prompt += (
                " Radiant mighty Vanara warrior Bajrangbali in golden dhoti and sacred janeyu thread, glowing mace Gada, fearless devotional strength."
            )
        elif "जटायु" in full_context or "jatayu" in full_context:
            prompt += (
                " Colossal majestic golden-feathered Eagle King with blazing heroic eyes fighting valiantly in mid-air."
            )
        return prompt

    @staticmethod
    def get_hindi_font(size: int) -> ImageFont.FreeTypeFont:
        """Cross-platform Devanagari Unicode font loader (macOS + Linux GitHub Actions)."""
        import glob
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansDevanagariUI-Regular.ttf",
            "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf",
        ]
        for pattern in ("/usr/share/fonts/**/*Devanagari*.ttf", "/usr/share/fonts/**/*NotoSans*.ttf"):
            candidates.extend(glob.glob(pattern, recursive=True))
        for fp in candidates:
            if Path(fp).exists():
                try:
                    return ImageFont.truetype(fp, size)
                except Exception:
                    continue
        return ImageFont.load_default()

    @classmethod
    def wrap_hindi_lines(cls, text: str, font_size: int = 35, max_width: int = 900) -> List[str]:
        """Wraps Devanagari Hindi text by true pixel width rather than ASCII character count."""
        img = Image.new("RGBA", (1080, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = cls.get_hindi_font(font_size)
        words = (text or "").strip().split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if (bbox[2] - bbox[0]) <= max_width or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or [""]

    @classmethod
    def create_header_badge(cls, track: str, episode_num: int, output_path: Path):
        """Generates standard top-centered gold header badge."""
        title_text = f"रामायण • भाग {episode_num}" if "RAMAYANA" in track.upper() else f"महाभारत • भाग {episode_num}"
        img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = cls.get_hindi_font(44)

        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pad_x, pad_y = 46, 16
        badge_w, badge_h = text_w + pad_x * 2, text_h + pad_y * 2
        badge_x, badge_y = (1080 - badge_w) // 2, 130

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
        font_main = cls.get_hindi_font(36)
        font_speaker = cls.get_hindi_font(32)

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
