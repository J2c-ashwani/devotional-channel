#!/usr/bin/env python3
"""
Generate 100% SOLID OPAQUE (NO TRANSPARENCY, RGB Mode) Master Assets for Itihasa Saga:
1. Itihasa_Saga_Logo_Avatar.png & .jpg (2048x2048) - 100% Solid Black & Gold
2. Itihasa_Saga_Logo_Brandmark.png & .jpg (2048x2048) - 100% Solid Black & Gold
3. Itihasa_Saga_YouTube_Banner.png & .jpg (2560x1440) - 100% Solid Black & Gold
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("/Users/ashwanikumar/Downloads")

# Rich Solid Colors (Strict 3-tuple RGB - ZERO Alpha)
BLACK_DEEP = (6, 8, 12)       # Rich Obsidian Midnight Black
BLACK_WARM = (24, 18, 10)     # Warm Sacred Temple Hearth Core
GOLD_SHADOW = (110, 80, 25)   # Deep Bronze / Shadow Gold
GOLD_DARK = (165, 125, 45)    # Antique Gold
GOLD_MID = (225, 180, 50)     # 24k Radiant Gold
GOLD_LIGHT = (255, 215, 90)   # Bright Divine Gold
GOLD_WHITE = (255, 250, 220)  # Core Diamond Flare White

def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def create_solid_radial_canvas(width, height, cx, cy, max_r=None):
    """Creates a 100% solid RGB image with a rich sacred amber-to-obsidian vignette"""
    img = Image.new("RGB", (width, height), BLACK_DEEP)
    draw = ImageDraw.Draw(img)
    if max_r is None:
        max_r = int(math.hypot(width, height) * 0.5)
        
    for r in range(max_r, 0, -8):
        t = (1.0 - (r / max_r)) ** 1.8
        color = lerp_color(BLACK_DEEP, BLACK_WARM, t)
        draw.ellipse([cx - r * 1.3, cy - r, cx + r * 1.3, cy + r], fill=color)
    return img

def draw_bold_celestial_emblem(draw, cx, cy, scale=1.0):
    """Draws a bold, high-contrast 24K gold Kodanda bow, arrow, and 32-ray mandala"""
    
    # 1. Radiant Sunburst Rays (32 Bold Golden Spikes)
    num_rays = 32
    r_outer = int(1400 * scale)
    r_inner = int(1220 * scale)
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        x1 = cx + math.cos(angle) * r_inner
        y1 = cy + math.sin(angle) * r_inner
        x2 = cx + math.cos(angle) * r_outer
        y2 = cy + math.sin(angle) * r_outer
        
        # Primary ray beam
        draw.line([(x1, y1), (x2, y2)], fill=GOLD_LIGHT, width=max(6, int(18 * scale)))
        draw.line([(x1, y1), (x2, y2)], fill=GOLD_WHITE, width=max(2, int(6 * scale)))
        
        # Ray Diamond Ornaments
        tip_x = cx + math.cos(angle) * (r_outer + 35 * scale)
        tip_y = cy + math.sin(angle) * (r_outer + 35 * scale)
        d_sz = int(14 * scale)
        draw.polygon([
            (tip_x, tip_y - d_sz),
            (tip_x + d_sz, tip_y),
            (tip_x, tip_y + d_sz),
            (tip_x - d_sz, tip_y)
        ], fill=GOLD_WHITE, outline=GOLD_MID)

    # 2. Concentric Golden Rings (Bold, layered)
    rings = [
        (1200 * scale, int(22 * scale), GOLD_MID),
        (1160 * scale, int(10 * scale), GOLD_LIGHT),
        (1120 * scale, int(6 * scale), GOLD_DARK),
        (940 * scale, int(14 * scale), GOLD_MID),
        (880 * scale, int(8 * scale), GOLD_LIGHT),
    ]
    for r, w, col in rings:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(3, int(w)))

    # 3. 72 Sacred Mala Beads along Ring (High Contrast Pearls)
    num_beads = 48
    bead_r = 1030 * scale
    for i in range(num_beads):
        angle = (2 * math.pi / num_beads) * i
        bx = cx + math.cos(angle) * bead_r
        by = cy + math.sin(angle) * bead_r
        bw = int(18 * scale) if i % 4 == 0 else int(11 * scale)
        draw.ellipse([bx - bw, by - bw, bx + bw, by + bw], fill=GOLD_WHITE, outline=GOLD_DARK)

    # 4. Sacred 8-Pointed Lotus Petals (Ashtadal) - Solid Gold Fill
    petals = 8
    petal_r = 860 * scale
    for i in range(petals):
        angle = (2 * math.pi / petals) * i
        p1 = (cx + math.cos(angle - 0.22) * (petal_r - 140 * scale), cy + math.sin(angle - 0.22) * (petal_r - 140 * scale))
        p_tip = (cx + math.cos(angle) * (petal_r + 50 * scale), cy + math.sin(angle) * (petal_r + 50 * scale))
        p2 = (cx + math.cos(angle + 0.22) * (petal_r - 140 * scale), cy + math.sin(angle + 0.22) * (petal_r - 140 * scale))
        draw.polygon([p1, p_tip, p2], fill=GOLD_DARK, outline=GOLD_LIGHT)
        # Inner petal highlight
        p_mid = (cx + math.cos(angle) * (petal_r - 40 * scale), cy + math.sin(angle) * (petal_r - 40 * scale))
        draw.line([p1, p_mid], fill=GOLD_WHITE, width=max(2, int(4 * scale)))
        draw.line([p2, p_mid], fill=GOLD_WHITE, width=max(2, int(4 * scale)))

    # 5. The Massive Celestial Kodanda Bow (Recurve Limbs)
    bow_h = int(720 * scale)
    bow_w = int(420 * scale)
    
    bow_pts_l = []
    bow_pts_r = []
    steps = 80
    for s in range(steps + 1):
        t = (s / steps) * 2 - 1  # -1 to 1
        x_off = math.sin((t + 1) * math.pi / 2) * bow_w - (t ** 4) * (bow_w * 0.28)
        y_pos = cy + t * bow_h
        bow_pts_l.append((cx - x_off, y_pos))
        bow_pts_r.append((cx + x_off, y_pos))

    # Outer Bow Staves (Thick 3D layered lines)
    draw.line(bow_pts_l, fill=GOLD_SHADOW, width=max(6, int(46 * scale)))
    draw.line(bow_pts_r, fill=GOLD_SHADOW, width=max(6, int(46 * scale)))
    draw.line(bow_pts_l, fill=GOLD_MID, width=max(4, int(30 * scale)))
    draw.line(bow_pts_r, fill=GOLD_MID, width=max(4, int(30 * scale)))
    draw.line(bow_pts_l, fill=GOLD_WHITE, width=max(2, int(12 * scale)))
    draw.line(bow_pts_r, fill=GOLD_WHITE, width=max(2, int(12 * scale)))

    # Bow Nocks (Gold finials)
    for p in [bow_pts_l[0], bow_pts_l[-1], bow_pts_r[0], bow_pts_r[-1]]:
        r_n = int(32 * scale)
        draw.ellipse([p[0] - r_n, p[1] - r_n, p[0] + r_n, p[1] + r_n], fill=GOLD_WHITE, outline=GOLD_MID)

    # Bowstrings (Bright taut cords)
    draw.line([bow_pts_l[0], bow_pts_l[-1]], fill=GOLD_WHITE, width=max(2, int(8 * scale)))
    draw.line([bow_pts_r[0], bow_pts_r[-1]], fill=GOLD_WHITE, width=max(2, int(8 * scale)))

    # 6. Central Divine Celestial Arrow (Pointing straight up to Cosmos)
    arrow_top = cy - int(920 * scale)
    arrow_bot = cy + int(780 * scale)

    # Arrow Shaft
    draw.line([(cx, arrow_bot), (cx, arrow_top)], fill=GOLD_MID, width=max(4, int(26 * scale)))
    draw.line([(cx, arrow_bot), (cx, arrow_top)], fill=GOLD_WHITE, width=max(2, int(10 * scale)))

    # Arrowhead (Broadhead Divine Blade)
    ah_len = int(220 * scale)
    ah_w = int(100 * scale)
    ah_tip = (cx, arrow_top - ah_len)
    ah_l = (cx - ah_w, arrow_top)
    ah_notch = (cx, arrow_top - int(ah_len * 0.3))
    ah_r = (cx + ah_w, arrow_top)
    draw.polygon([ah_tip, ah_l, ah_notch, ah_r], fill=GOLD_WHITE, outline=GOLD_MID)
    draw.line([ah_tip, ah_notch], fill=GOLD_MID, width=max(2, int(6 * scale)))

    # Arrow Fletching (Sacred Feather Base)
    f_len = int(180 * scale)
    f_w = int(80 * scale)
    for sign in [-1, 1]:
        f1 = (cx, arrow_bot - f_len)
        f2 = (cx + sign * f_w, arrow_bot - int(f_len * 0.4))
        f3 = (cx + sign * f_w, arrow_bot)
        f4 = (cx, arrow_bot - int(f_len * 0.2))
        draw.polygon([f1, f2, f3, f4], fill=GOLD_LIGHT, outline=GOLD_DARK)

    # 7. Cosmic Starburst Flare at Arrow Tip
    flare_x, flare_y = ah_tip
    for fl_r, fl_w, col in [(240 * scale, 6 * scale, GOLD_LIGHT), (140 * scale, 14 * scale, GOLD_WHITE)]:
        draw.line([(flare_x - fl_r, flare_y), (flare_x + fl_r, flare_y)], fill=col, width=max(2, int(fl_w)))
        draw.line([(flare_x, flare_y - fl_r), (flare_x, flare_y + fl_r)], fill=col, width=max(2, int(fl_w)))
        d_r = fl_r * 0.7
        draw.line([(flare_x - d_r, flare_y - d_r), (flare_x + d_r, flare_y + d_r)], fill=col, width=max(1, int(fl_w * 0.7)))
        draw.line([(flare_x - d_r, flare_y + d_r), (flare_x + d_r, flare_y - d_r)], fill=col, width=max(1, int(fl_w * 0.7)))
    draw.ellipse([flare_x - 22 * scale, flare_y - 22 * scale, flare_x + 22 * scale, flare_y + 22 * scale], fill=GOLD_WHITE)

def generate_solid_avatar():
    """Generates 100% Solid RGB 2048x2048 Avatar in both PNG and JPG"""
    size = 2048
    cx, cy = size // 2, size // 2
    img = create_solid_radial_canvas(size, size, cx, cy)
    draw = ImageDraw.Draw(img)
    draw_bold_celestial_emblem(draw, cx, cy, scale=0.68)
    
    png_path = OUTPUT_DIR / "Itihasa_Saga_Logo_Avatar.png"
    jpg_path = OUTPUT_DIR / "Itihasa_Saga_Logo_Avatar.jpg"
    
    # Save as 100% solid RGB PNG (zero alpha)
    img.save(png_path, format="PNG", optimize=True)
    # Save as 100% solid high-quality JPG (impossible to have transparency)
    img.save(jpg_path, format="JPEG", quality=98)
    print(f"✅ Generated Solid Avatar: {png_path} & {jpg_path}")

def generate_solid_brandmark():
    """Generates 100% Solid RGB 2048x2048 Full Brandmark with Luxury Serif Typography"""
    size = 2048
    cx = size // 2
    emblem_cy = int(size * 0.38)
    img = create_solid_radial_canvas(size, size, cx, emblem_cy)
    draw = ImageDraw.Draw(img)
    draw_bold_celestial_emblem(draw, cx, emblem_cy, scale=0.52)
    
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 110, index=0)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 44, index=0)
    
    title_text = "I T I H A S A   S A G A"
    sub_text = "T I M E L E S S   E P I C S"
    
    bbox_title = draw.textbbox((0, 0), title_text, font=font_title)
    w_title = bbox_title[2] - bbox_title[0]
    title_y = int(size * 0.76)
    
    draw.text((cx - w_title // 2, title_y), title_text, font=font_title, fill=GOLD_WHITE)
    
    rule_y = title_y + 130
    draw.line([(cx - 300, rule_y), (cx + 300, rule_y)], fill=GOLD_MID, width=4)
    draw.ellipse([cx - 10, rule_y - 10, cx + 10, rule_y + 10], fill=GOLD_LIGHT)
    
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((cx - w_sub // 2, rule_y + 24), sub_text, font=font_sub, fill=GOLD_LIGHT)
    
    png_path = OUTPUT_DIR / "Itihasa_Saga_Logo_Brandmark.png"
    jpg_path = OUTPUT_DIR / "Itihasa_Saga_Logo_Brandmark.jpg"
    img.save(png_path, format="PNG", optimize=True)
    img.save(jpg_path, format="JPEG", quality=98)
    print(f"✅ Generated Solid Brandmark: {png_path} & {jpg_path}")

def generate_solid_banner():
    """Generates 100% Solid RGB 2560x1440 YouTube Banner in both PNG and JPG"""
    width = 2560
    height = 1440
    cx = width // 2
    cy = height // 2
    
    img = create_solid_radial_canvas(width, height, cx, cy, max_r=1100)
    draw = ImageDraw.Draw(img)
    
    # 48 Radiant Sunburst Beams across banner
    for i in range(48):
        angle = (2 * math.pi / 48) * i
        length = 1400
        x2 = cx + math.cos(angle) * length
        y2 = cy + math.sin(angle) * length
        col = (45, 34, 18) if i % 2 == 0 else (28, 20, 10)
        draw.line([(cx, cy), (x2, y2)], fill=col, width=3 if i % 2 == 0 else 1)
        
    # Concentric rings
    for r in [220, 360, 520, 720, 950, 1200]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 30, 15), width=2)
        
    # Stardust particles
    random.seed(108)
    for _ in range(250):
        px = random.randint(50, width - 50)
        py = random.randint(50, height - 50)
        sz = random.uniform(1.2, 3.2)
        col = GOLD_LIGHT if random.random() > 0.4 else GOLD_DARK
        draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col)

    # Safe Zone Central Positioning
    emblem_y = cy - 60
    draw_bold_celestial_emblem(draw, cx, emblem_y, scale=0.20)
    
    # Typography
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 82, index=0)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 28, index=0)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 22, index=0)

    title = "I T I H A S A   S A G A"
    bbox_title = draw.textbbox((0, 0), title, font=font_title)
    w_title = bbox_title[2] - bbox_title[0]
    title_y = emblem_y + 115

    # Shadow + Text
    draw.text((cx - w_title // 2 + 2, title_y + 2), title, font=font_title, fill=(0, 0, 0))
    draw.text((cx - w_title // 2, title_y), title, font=font_title, fill=GOLD_WHITE)

    rule_y = title_y + 98
    draw.line([(cx - 360, rule_y), (cx - 40, rule_y)], fill=GOLD_MID, width=2)
    draw.line([(cx + 40, rule_y), (cx + 360, rule_y)], fill=GOLD_MID, width=2)
    draw.ellipse([cx - 8, rule_y - 8, cx + 8, rule_y + 8], fill=GOLD_LIGHT)

    subtitle = "RAMAYANA  •  MAHABHARATA  •  PURANIC CHRONICLES"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((cx - w_sub // 2, rule_y + 18), subtitle, font=font_sub, fill=GOLD_LIGHT)

    badge = "NEW EPISODES DAILY AT 7:00 AM IST  |  @ITIHASASAGA"
    bbox_badge = draw.textbbox((0, 0), badge, font=font_badge)
    w_badge = bbox_badge[2] - bbox_badge[0]
    draw.text((cx - w_badge // 2, rule_y + 56), badge, font=font_badge, fill=GOLD_DARK)

    png_path = OUTPUT_DIR / "Itihasa_Saga_YouTube_Banner.png"
    jpg_path = OUTPUT_DIR / "Itihasa_Saga_YouTube_Banner.jpg"
    img.save(png_path, format="PNG", optimize=True)
    img.save(jpg_path, format="JPEG", quality=98)
    print(f"✅ Generated Solid Banner: {png_path} & {jpg_path}")

if __name__ == "__main__":
    generate_solid_avatar()
    generate_solid_brandmark()
    generate_solid_banner()
