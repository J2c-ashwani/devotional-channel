#!/usr/bin/env python3
"""
Generate Broadcast-Grade Master Brand Logos for ITIHASA SAGA (@itihasasaga).
Renders 2048x2048 master assets using anti-aliased mathematical geometry:
1. itihasa_saga_avatar.png (Circular profile avatar for YouTube, Instagram, Facebook)
2. itihasa_saga_brandmark.png (Full emblem + Luxury Serif Typography)
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

OUTPUT_DIR = Path("/Users/ashwanikumar/Downloads")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 4096 supersampled size, downscaled to 2048 for retina vector-crisp edges
SIZE = 4096
CENTER = (SIZE // 2, SIZE // 2)
CX, CY = CENTER

# Gold Palette
GOLD_DARK = (154, 123, 56)
GOLD_MID = (212, 175, 55)
GOLD_LIGHT = (235, 203, 110)
GOLD_BRIGHT = (255, 238, 175)
GOLD_WHITE = (255, 252, 240)
BLACK_BG = (10, 12, 16)

def create_radial_background(size):
    bg = Image.new("RGBA", (size, size), BLACK_BG + (255,))
    draw = ImageDraw.Draw(bg)
    max_r = int(size * 0.7)
    
    # Subtle divine amber radial core
    for r in range(max_r, 0, -10):
        alpha = int(35 * (1.0 - (r / max_r) ** 1.5))
        color = (45, 32, 15, alpha)
        draw.ellipse([CX - r, CY - r, CX + r, CY + r], fill=color)
    return bg

def draw_celestial_emblem(draw, center_y=CY, scale=1.0):
    cx, cy = CX, center_y
    
    # 1. Outer Radiant Sun Mandala (32 Rays)
    num_rays = 32
    r_outer = int(1450 * scale)
    r_inner = int(1350 * scale)
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        x1 = cx + math.cos(angle) * r_inner
        y1 = cy + math.sin(angle) * r_inner
        x2 = cx + math.cos(angle) * r_outer
        y2 = cy + math.sin(angle) * r_outer
        
        # Ray thickness
        draw.line([(x1, y1), (x2, y2)], fill=GOLD_MID + (220,), width=int(14 * scale))
        
        # Micro sun-points
        tip_x = cx + math.cos(angle) * (r_outer + 35 * scale)
        tip_y = cy + math.sin(angle) * (r_outer + 35 * scale)
        draw.ellipse([tip_x - 10 * scale, tip_y - 10 * scale, tip_x + 10 * scale, tip_y + 10 * scale], fill=GOLD_LIGHT + (240,))

    # 2. Concentric Gold Rings
    rings = [
        (1330 * scale, 12 * scale, GOLD_MID),
        (1300 * scale, 6 * scale, GOLD_DARK),
        (1200 * scale, 16 * scale, GOLD_LIGHT),
        (1160 * scale, 8 * scale, GOLD_MID),
        (950 * scale, 10 * scale, GOLD_DARK),
    ]
    for r, w, col in rings:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col + (255,), width=int(w))

    # 3. 108 Sacred Mala Beads along Ring
    num_beads = 72
    bead_r = 1250 * scale
    for i in range(num_beads):
        angle = (2 * math.pi / num_beads) * i
        bx = cx + math.cos(angle) * bead_r
        by = cy + math.sin(angle) * bead_r
        bw = 14 * scale if i % 6 == 0 else 9 * scale
        col = GOLD_BRIGHT if i % 6 == 0 else GOLD_MID
        draw.ellipse([bx - bw, by - bw, bx + bw, by + bw], fill=col + (255,))

    # 4. Sacred 8-Pointed Lotus Petals (Ashtadal)
    petals = 8
    petal_r = 1080 * scale
    for i in range(petals):
        angle = (2 * math.pi / petals) * i
        p1 = (cx + math.cos(angle - 0.18) * (petal_r - 120 * scale), cy + math.sin(angle - 0.18) * (petal_r - 120 * scale))
        p_tip = (cx + math.cos(angle) * (petal_r + 40 * scale), cy + math.sin(angle) * (petal_r + 40 * scale))
        p2 = (cx + math.cos(angle + 0.18) * (petal_r - 120 * scale), cy + math.sin(angle + 0.18) * (petal_r - 120 * scale))
        draw.polygon([p1, p_tip, p2], fill=GOLD_MID + (180,), outline=GOLD_BRIGHT + (255,))

    # 5. The Celestial Kodanda Bow (Left and Right Recurve Arc)
    bow_h = int(880 * scale)
    bow_w = int(480 * scale)
    
    # Draw Left Bow Limb
    bow_points_left = []
    bow_points_right = []
    steps = 100
    for s in range(steps + 1):
        t = (s / steps) * 2 - 1  # -1 to 1
        # Recurve polynomial curve
        x_offset = math.sin((t + 1) * math.pi / 2) * bow_w - (t ** 4) * (bow_w * 0.3)
        y_pos = cy + t * bow_h
        bow_points_left.append((cx - x_offset, y_pos))
        bow_points_right.append((cx + x_offset, y_pos))

    # Outer Bow Spine
    draw.line(bow_points_left, fill=GOLD_LIGHT + (255,), width=int(32 * scale))
    draw.line(bow_points_right, fill=GOLD_LIGHT + (255,), width=int(32 * scale))
    # Inner Bow Highlight
    draw.line(bow_points_left, fill=GOLD_WHITE + (230,), width=int(12 * scale))
    draw.line(bow_points_right, fill=GOLD_WHITE + (230,), width=int(12 * scale))

    # Bow Tips (Nock ornaments)
    for p in [bow_points_left[0], bow_points_left[-1], bow_points_right[0], bow_points_right[-1]]:
        draw.ellipse([p[0] - 25 * scale, p[1] - 25 * scale, p[0] + 25 * scale, p[1] + 25 * scale], fill=GOLD_BRIGHT + (255,))

    # Bowstrings
    draw.line([bow_points_left[0], bow_points_left[-1]], fill=GOLD_BRIGHT + (190,), width=int(8 * scale))
    draw.line([bow_points_right[0], bow_points_right[-1]], fill=GOLD_BRIGHT + (190,), width=int(8 * scale))

    # 6. Central Divine Celestial Arrow (Pointing Straight Up to the Cosmos)
    arrow_top = cy - int(1050 * scale)
    arrow_bottom = cy + int(920 * scale)
    
    # Arrow Shaft
    draw.line([(cx, arrow_bottom), (cx, arrow_top)], fill=GOLD_LIGHT + (255,), width=int(22 * scale))
    draw.line([(cx, arrow_bottom), (cx, arrow_top)], fill=GOLD_WHITE + (255,), width=int(8 * scale))

    # Arrowhead (Razor-sharp divine arrowhead)
    ah_len = int(180 * scale)
    ah_w = int(75 * scale)
    ah_tip = (cx, arrow_top - ah_len)
    ah_left = (cx - ah_w, arrow_top)
    ah_notch = (cx, arrow_top - int(ah_len * 0.25))
    ah_right = (cx + ah_w, arrow_top)
    draw.polygon([ah_tip, ah_left, ah_notch, ah_right], fill=GOLD_BRIGHT + (255,), outline=GOLD_WHITE + (255,))

    # Fletching (Arrow Feathers at base)
    f_len = int(160 * scale)
    f_w = int(70 * scale)
    for sign in [-1, 1]:
        f1 = (cx, arrow_bottom - f_len)
        f2 = (cx + sign * f_w, arrow_bottom - int(f_len * 0.4))
        f3 = (cx + sign * f_w, arrow_bottom)
        f4 = (cx, arrow_bottom - int(f_len * 0.2))
        draw.polygon([f1, f2, f3, f4], fill=GOLD_MID + (255,), outline=GOLD_LIGHT + (255,))

    # 7. Cosmic Starburst Flare at Arrow Tip
    flare_cx, flare_cy = ah_tip
    for fl_r, fl_alpha, fl_w in [(180 * scale, 120, 8 * scale), (90 * scale, 220, 16 * scale)]:
        draw.line([(flare_cx - fl_r, flare_cy), (flare_cx + fl_r, flare_cy)], fill=GOLD_WHITE + (fl_alpha,), width=int(fl_w))
        draw.line([(flare_cx, flare_cy - fl_r), (flare_cx, flare_cy + fl_r)], fill=GOLD_WHITE + (fl_alpha,), width=int(fl_w))
        # 45 deg diagonals
        d_r = fl_r * 0.7
        draw.line([(flare_cx - d_r, flare_cy - d_r), (flare_cx + d_r, flare_cy + d_r)], fill=GOLD_WHITE + (int(fl_alpha * 0.7),), width=int(fl_w * 0.7))
        draw.line([(flare_cx - d_r, flare_cy + d_r), (flare_cx + d_r, flare_cy - d_r)], fill=GOLD_WHITE + (int(fl_alpha * 0.7),), width=int(fl_w * 0.7))
    draw.ellipse([flare_cx - 25 * scale, flare_cy - 25 * scale, flare_cx + 25 * scale, flare_cy + 25 * scale], fill=GOLD_WHITE + (255,))

def generate_avatar():
    """Generates 2048x2048 Circular Profile Icon for Instagram, YouTube, Facebook"""
    img = create_radial_background(SIZE)
    draw = ImageDraw.Draw(img)
    draw_celestial_emblem(draw, center_y=CY, scale=1.0)
    
    # Downsample with Lanczos for ultra-crisp antialiasing
    final = img.resize((2048, 2048), Image.Resampling.LANCZOS)
    out_path = OUTPUT_DIR / "itihasa_saga_avatar.png"
    final.save(out_path, format="PNG", optimize=True)
    print(f"✅ Generated Profile Avatar: {out_path}")
    return out_path

def generate_brandmark():
    """Generates 2048x2048 Full Brandmark with Luxury Serif Typography"""
    img = create_radial_background(SIZE)
    draw = ImageDraw.Draw(img)
    
    # Place emblem slightly higher to give room for luxury typography
    emblem_cy = int(SIZE * 0.40)
    draw_celestial_emblem(draw, center_y=emblem_cy, scale=0.75)
    
    # Typography using system luxury serif
    font_title_path = "/System/Library/Fonts/Supplemental/Didot.ttc"
    font_sub_path = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
    
    font_title = ImageFont.truetype(font_title_path, 200, index=0)
    font_sub = ImageFont.truetype(font_sub_path, 80, index=0)
    
    title_text = "I T I H A S A   S A G A"
    sub_text = "T I M E L E S S   E P I C S"
    
    # Calculate text positioning
    bbox_title = draw.textbbox((0, 0), title_text, font=font_title)
    w_title = bbox_title[2] - bbox_title[0]
    draw.text((CX - w_title // 2, int(SIZE * 0.78)), title_text, font=font_title, fill=GOLD_BRIGHT + (255,))
    
    # Decorative rule line
    rule_y = int(SIZE * 0.86)
    draw.line([(CX - 400, rule_y), (CX + 400, rule_y)], fill=GOLD_MID + (200,), width=6)
    draw.ellipse([CX - 15, rule_y - 15, CX + 15, rule_y + 15], fill=GOLD_LIGHT + (255,))
    
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((CX - w_sub // 2, int(SIZE * 0.89)), sub_text, font=font_sub, fill=GOLD_MID + (240,))
    
    final = img.resize((2048, 2048), Image.Resampling.LANCZOS)
    out_path = OUTPUT_DIR / "itihasa_saga_brandmark.png"
    final.save(out_path, format="PNG", optimize=True)
    print(f"✅ Generated Full Brandmark: {out_path}")
    return out_path

if __name__ == "__main__":
    generate_avatar()
    generate_brandmark()
