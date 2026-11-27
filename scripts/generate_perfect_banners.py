#!/usr/bin/env python3
"""
Generate Mathematically Guaranteed YouTube Banners for ITIHASA SAGA.
Strict YouTube Safe Zone Boundaries:
- Canvas: 2560 x 1440
- All-Device Safe Area: 1546 x 423
  - X: 507 to 2053
  - Y: 509 to 931
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("/Users/ashwanikumar/Downloads")

WIDTH = 2560
HEIGHT = 1440
CX = WIDTH // 2
CY = HEIGHT // 2

SAFE_X1, SAFE_X2 = 507, 2053
SAFE_Y1, SAFE_Y2 = 509, 931
SAFE_H = SAFE_Y2 - SAFE_Y1  # 422 px

# Colors (100% Solid RGB)
BLACK_DEEP = (6, 8, 12)
BLACK_WARM = (22, 16, 10)
GOLD_SHADOW = (110, 80, 25)
GOLD_DARK = (165, 125, 45)
GOLD_MID = (225, 180, 50)
GOLD_LIGHT = (255, 215, 90)
GOLD_WHITE = (255, 250, 220)

def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def create_base_canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), BLACK_DEEP)
    draw = ImageDraw.Draw(img)
    
    # Celestial amber core
    for r in range(950, 0, -8):
        t = (1.0 - (r / 950)) ** 1.8
        color = lerp_color(BLACK_DEEP, BLACK_WARM, t)
        draw.ellipse([CX - r * 1.5, CY - r, CX + r * 1.5, CY + r], fill=color)

    # 48 Radiant Sunburst Beams
    for i in range(48):
        angle = (2 * math.pi / 48) * i
        length = 1400
        x2 = CX + math.cos(angle) * length
        y2 = CY + math.sin(angle) * length
        col = (40, 30, 16) if i % 2 == 0 else (24, 18, 10)
        draw.line([(CX, CY), (x2, y2)], fill=col, width=3 if i % 2 == 0 else 1)

    # Concentric rings
    for r in [220, 360, 520, 720, 950, 1200]:
        draw.ellipse([CX - r, CY - r, CX + r, CY + r], outline=(38, 28, 14), width=2)

    # Stardust
    random.seed(108)
    for _ in range(220):
        px = random.randint(50, WIDTH - 50)
        py = random.randint(50, HEIGHT - 50)
        sz = random.uniform(1.2, 3.0)
        col = GOLD_LIGHT if random.random() > 0.4 else GOLD_DARK
        draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col)
        
    return img

def draw_emblem(draw, cx, cy, radius):
    """Draws a clean, high-contrast Kodanda bow & arrow emblem inside radius"""
    scale = radius / 400.0
    
    # Outer ring
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=GOLD_MID, width=max(2, int(4 * scale)))
    draw.ellipse([cx - radius + 8, cy - radius + 8, cx + radius - 8, cy + radius - 8], outline=GOLD_DARK, width=1)
    
    # 24 Sun points
    for i in range(24):
        angle = (2 * math.pi / 24) * i
        x1 = cx + math.cos(angle) * (radius - 12)
        y1 = cy + math.sin(angle) * (radius - 12)
        x2 = cx + math.cos(angle) * (radius + 15)
        y2 = cy + math.sin(angle) * (radius + 15)
        draw.line([(x1, y1), (x2, y2)], fill=GOLD_LIGHT, width=max(2, int(3 * scale)))

    # Bow limbs
    bow_h = int(radius * 0.75)
    bow_w = int(radius * 0.42)
    bow_pts_l, bow_pts_r = [], []
    for s in range(41):
        t = (s / 40) * 2 - 1
        x_off = math.sin((t + 1) * math.pi / 2) * bow_w - (t ** 4) * (bow_w * 0.25)
        y_pos = cy + t * bow_h
        bow_pts_l.append((cx - x_off, y_pos))
        bow_pts_r.append((cx + x_off, y_pos))
        
    draw.line(bow_pts_l, fill=GOLD_MID, width=max(3, int(10 * scale)))
    draw.line(bow_pts_r, fill=GOLD_MID, width=max(3, int(10 * scale)))
    draw.line(bow_pts_l, fill=GOLD_WHITE, width=max(1, int(4 * scale)))
    draw.line(bow_pts_r, fill=GOLD_WHITE, width=max(1, int(4 * scale)))
    
    # Bowstrings
    draw.line([bow_pts_l[0], bow_pts_l[-1]], fill=GOLD_WHITE, width=max(1, int(2 * scale)))
    draw.line([bow_pts_r[0], bow_pts_r[-1]], fill=GOLD_WHITE, width=max(1, int(2 * scale)))

    # Arrow
    arrow_top = cy - int(radius * 0.82)
    arrow_bot = cy + int(radius * 0.72)
    draw.line([(cx, arrow_bot), (cx, arrow_top)], fill=GOLD_WHITE, width=max(2, int(5 * scale)))
    
    # Arrowhead
    ah_len = int(radius * 0.22)
    ah_w = int(radius * 0.12)
    draw.polygon([
        (cx, arrow_top - ah_len),
        (cx - ah_w, arrow_top),
        (cx, arrow_top - int(ah_len * 0.25)),
        (cx + ah_w, arrow_top)
    ], fill=GOLD_WHITE, outline=GOLD_MID)
    
    # Tip flare
    flare_y = arrow_top - ah_len
    for fl_r in [int(radius * 0.2), int(radius * 0.1)]:
        draw.line([(cx - fl_r, flare_y), (cx + fl_r, flare_y)], fill=GOLD_WHITE, width=2)
        draw.line([(cx, flare_y - fl_r), (cx, flare_y + fl_r)], fill=GOLD_WHITE, width=2)

def generate_perfect_horizontal_banner():
    """
    Layout 1 (Horizontal Executive Studio Lockup):
    Left: Majestic Golden Emblem (Radius: 135px, Height: 270px)
    Right: Bold Title + Subtitles
    Total Height: ~270px (Centered vertically in the 422px safe zone -> 76px safety margin on top and bottom!)
    """
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)

    # Safe Zone Y is 509 to 931. CY = 720.
    # Total Lockup Width: ~1250 px (centered at CX = 1280)
    # Left edge ~650, Right edge ~1910 (Well inside 507 to 2053!)
    
    emblem_cx = CX - 380
    emblem_cy = CY
    draw_emblem(draw, emblem_cx, emblem_cy, radius=130)

    # Typography on the Right
    text_x = CX - 180
    font_pre = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 26, index=0)
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 92, index=0)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 30, index=0)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 22, index=0)

    # 1. Pre-title
    pre_y = CY - 105
    draw.text((text_x, pre_y), "S A N A T A N   D H A R M A   E P I C S", font=font_pre, fill=GOLD_DARK)

    # 2. Main Title (Big & Bold)
    title_y = pre_y + 34
    draw.text((text_x + 2, title_y + 2), "ITIHASA SAGA", font=font_title, fill=(0, 0, 0))
    draw.text((text_x, title_y), "ITIHASA SAGA", font=font_title, fill=GOLD_WHITE)

    # 3. Decorative Gold Accent Line
    rule_y = title_y + 102
    draw.line([(text_x, rule_y), (text_x + 650, rule_y)], fill=GOLD_MID, width=2)
    draw.ellipse([text_x - 4, rule_y - 4, text_x + 4, rule_y + 4], fill=GOLD_LIGHT)
    draw.ellipse([text_x + 650 - 4, rule_y - 4, text_x + 650 + 4, rule_y + 4], fill=GOLD_LIGHT)

    # 4. Subtitle
    sub_y = rule_y + 14
    draw.text((text_x, sub_y), "RAMAYANA  •  MAHABHARATA  •  PURANAS", font=font_sub, fill=GOLD_LIGHT)

    # 5. Schedule Badge
    badge_y = sub_y + 42
    draw.text((text_x, badge_y), "NEW EPISODES DAILY AT 7:00 AM IST  |  @ITIHASASAGA", font=font_badge, fill=GOLD_MID)

    # Save both PNG & JPG
    p_png = OUTPUT_DIR / "Itihasa_Saga_YouTube_Banner.png"
    p_jpg = OUTPUT_DIR / "Itihasa_Saga_YouTube_Banner.jpg"
    img.save(p_png, format="PNG", optimize=True)
    img.save(p_jpg, format="JPEG", quality=98)
    print("✅ Generated Perfect Horizontal Banner:", p_png, p_jpg)

def generate_perfect_compact_center_banner():
    """
    Layout 2 (Compact Centered Stack):
    Everything stacked vertically, but strictly scaled to fit within 300px total height!
    """
    img = create_base_canvas()
    draw = ImageDraw.Draw(img)

    # Emblem at top: radius = 55px (Height 110px)
    emblem_cy = CY - 85
    draw_emblem(draw, CX, emblem_cy, radius=55)

    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 62, index=0)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 22, index=0)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 17, index=0)

    # Main Title
    title = "I T I H A S A   S A G A"
    bbox_t = draw.textbbox((0, 0), title, font=font_title)
    w_t = bbox_t[2] - bbox_t[0]
    title_y = emblem_cy + 65
    draw.text((CX - w_t // 2 + 2, title_y + 2), title, font=font_title, fill=(0, 0, 0))
    draw.text((CX - w_t // 2, title_y), title, font=font_title, fill=GOLD_WHITE)

    # Accent line
    rule_y = title_y + 76
    draw.line([(CX - 250, rule_y), (CX + 250, rule_y)], fill=GOLD_MID, width=2)
    draw.ellipse([CX - 5, rule_y - 5, CX + 5, rule_y + 5], fill=GOLD_LIGHT)

    # Subtitle
    sub = "RAMAYANA  •  MAHABHARATA  •  PURANIC CHRONICLES"
    bbox_s = draw.textbbox((0, 0), sub, font=font_sub)
    w_s = bbox_s[2] - bbox_s[0]
    draw.text((CX - w_s // 2, rule_y + 12), sub, font=font_sub, fill=GOLD_LIGHT)

    # Badge
    badge = "NEW EPISODES DAILY AT 7:00 AM IST  |  @ITIHASASAGA"
    bbox_b = draw.textbbox((0, 0), badge, font=font_badge)
    w_b = bbox_b[2] - bbox_b[0]
    draw.text((CX - w_b // 2, rule_y + 42), badge, font=font_badge, fill=GOLD_MID)

    p_center_jpg = OUTPUT_DIR / "Itihasa_Saga_YouTube_Banner_Centered.jpg"
    p_center_png = OUTPUT_DIR / "Itihasa_Saga_YouTube_Banner_Centered.png"
    img.save(p_center_png, format="PNG", optimize=True)
    img.save(p_center_jpg, format="JPEG", quality=98)
    print("✅ Generated Compact Centered Banner:", p_center_jpg)

if __name__ == "__main__":
    generate_perfect_horizontal_banner()
    generate_perfect_compact_center_banner()
