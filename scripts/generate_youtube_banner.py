#!/usr/bin/env python3
"""
Generate Broadcast-Grade Master YouTube Channel Banner for ITIHASA SAGA (@itihasasaga).
Official YouTube specifications:
- Full Canvas: 2560 x 1440 pixels (16:9 for TV display)
- Safe Area (Mobile & Desktop guaranteed visibility): 1546 x 423 pixels (Centered)
  - X: 507 to 2053
  - Y: 508 to 931
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_PATH = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_YouTube_Banner.png")

# Native banner dimensions
WIDTH = 2560
HEIGHT = 1440
CX = WIDTH // 2
CY = HEIGHT // 2

# Colors
BG_DARK = (8, 10, 14)
BG_CORE = (28, 20, 10)
GOLD_DARK = (154, 123, 56)
GOLD_MID = (212, 175, 55)
GOLD_LIGHT = (238, 207, 115)
GOLD_BRIGHT = (255, 240, 185)
GOLD_WHITE = (255, 252, 242)

def create_banner():
    # 1. Base Dark Canvas
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_DARK + (255,))
    draw = ImageDraw.Draw(img)

    # 2. Celestial Warm Core Glow (Centered)
    for r in range(900, 0, -15):
        alpha = int(45 * (1.0 - (r / 900) ** 1.3))
        draw.ellipse([CX - r * 1.6, CY - r, CX + r * 1.6, CY + r], fill=(55, 38, 16, alpha))

    # 3. Outer Divine Solar Rays (48 Rays across canvas)
    num_rays = 48
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        length = 1300
        x2 = CX + math.cos(angle) * length
        y2 = CY + math.sin(angle) * length
        alpha = 25 if i % 2 == 0 else 12
        w = 3 if i % 2 == 0 else 1
        draw.line([(CX, CY), (x2, y2)], fill=GOLD_MID + (alpha,), width=w)

    # 4. Concentric Sacred Geometry Rings (Subtle in background)
    ring_radii = [180, 240, 320, 420, 560, 720, 900, 1150]
    for r in ring_radii:
        alpha = 35 if r < 500 else 18
        draw.ellipse([CX - r, CY - r, CX + r, CY + r], outline=GOLD_MID + (alpha,), width=2)

    # 5. Golden Stardust / Celestial Embers Particles
    random.seed(108)  # Sacred seed for reproducible beauty
    for _ in range(250):
        px = random.randint(100, WIDTH - 100)
        py = random.randint(100, HEIGHT - 100)
        p_dist = math.hypot(px - CX, py - CY)
        if p_dist < 1200:
            sz = random.uniform(1.0, 3.5)
            alpha = random.randint(40, 160)
            col = GOLD_BRIGHT if random.random() > 0.4 else GOLD_MID
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col + (alpha,))

    # 6. Central Sacred Emblem (Kodanda Bow & Starburst) positioned slightly above center
    emblem_y = CY - 55
    scale = 0.32  # Compact scale to fit safely within the 423px vertical safe zone
    
    # Lotus petals behind emblem
    petals = 12
    for i in range(petals):
        angle = (2 * math.pi / petals) * i
        p_len = 160 * scale
        p_tip = (CX + math.cos(angle) * (180 + p_len), emblem_y + math.sin(angle) * (180 + p_len))
        p1 = (CX + math.cos(angle - 0.15) * 170, emblem_y + math.sin(angle - 0.15) * 170)
        p2 = (CX + math.cos(angle + 0.15) * 170, emblem_y + math.sin(angle + 0.15) * 170)
        draw.polygon([p1, p_tip, p2], fill=GOLD_MID + (70,), outline=GOLD_LIGHT + (120,))

    # Circular emblem frame
    draw.ellipse([CX - 130, emblem_y - 130, CX + 130, emblem_y + 130], outline=GOLD_LIGHT + (220,), width=3)
    draw.ellipse([CX - 120, emblem_y - 120, CX + 120, emblem_y + 120], outline=GOLD_DARK + (180,), width=1)

    # Bow curves
    bow_h = int(105)
    bow_w = int(65)
    bow_pts_l = []
    bow_pts_r = []
    for s in range(51):
        t = (s / 50) * 2 - 1
        x_off = math.sin((t + 1) * math.pi / 2) * bow_w - (t ** 4) * (bow_w * 0.25)
        y_pos = emblem_y + t * bow_h
        bow_pts_l.append((CX - x_off, y_pos))
        bow_pts_r.append((CX + x_off, y_pos))

    draw.line(bow_pts_l, fill=GOLD_BRIGHT + (255,), width=4)
    draw.line(bow_pts_r, fill=GOLD_BRIGHT + (255,), width=4)
    draw.line([bow_pts_l[0], bow_pts_l[-1]], fill=GOLD_WHITE + (180,), width=1)
    draw.line([bow_pts_r[0], bow_pts_r[-1]], fill=GOLD_WHITE + (180,), width=1)

    # Arrow
    arrow_top = emblem_y - 115
    arrow_bot = emblem_y + 105
    draw.line([(CX, arrow_bot), (CX, arrow_top)], fill=GOLD_WHITE + (255,), width=3)
    # Arrowhead
    draw.polygon([(CX, arrow_top - 20), (CX - 12, arrow_top), (CX, arrow_top - 4), (CX + 12, arrow_top)], fill=GOLD_WHITE + (255,))
    # Starburst flare at arrow tip
    tip_y = arrow_top - 20
    for fl_r in [35, 18]:
        draw.line([(CX - fl_r, tip_y), (CX + fl_r, tip_y)], fill=GOLD_WHITE + (220,), width=2)
        draw.line([(CX, tip_y - fl_r), (CX, tip_y + fl_r)], fill=GOLD_WHITE + (220,), width=2)

    # 7. Safe Zone Typography (Ensuring complete visibility on Mobile & TV)
    # Fonts
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 76, index=0)
    font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 26, index=0)
    font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Baskerville.ttc", 20, index=0)

    # Main Title
    title = "I T I H A S A   S A G A"
    bbox_title = draw.textbbox((0, 0), title, font=font_title)
    w_title = bbox_title[2] - bbox_title[0]
    title_y = emblem_y + 115
    
    # Subtle drop shadow
    draw.text((CX - w_title // 2 + 2, title_y + 2), title, font=font_title, fill=(0, 0, 0, 220))
    draw.text((CX - w_title // 2, title_y), title, font=font_title, fill=GOLD_WHITE + (255,))

    # Horizontal Luxury Accents (Flanking Lines with Jewels)
    rule_y = title_y + 92
    draw.line([(CX - 320, rule_y), (CX - 40, rule_y)], fill=GOLD_MID + (180,), width=2)
    draw.line([(CX + 40, rule_y), (CX + 320, rule_y)], fill=GOLD_MID + (180,), width=2)
    draw.ellipse([CX - 8, rule_y - 8, CX + 8, rule_y + 8], fill=GOLD_LIGHT + (255,))

    # Subtitle / Epic Pillars
    subtitle = "RAMAYANA  •  MAHABHARATA  •  PURANIC CHRONICLES"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    draw.text((CX - w_sub // 2, rule_y + 18), subtitle, font=font_sub, fill=GOLD_LIGHT + (240,))

    # Schedule & Handle Badge
    badge = "NEW EPISODES DAILY AT 7:00 AM IST  |  @ITIHASASAGA"
    bbox_badge = draw.textbbox((0, 0), badge, font=font_badge)
    w_badge = bbox_badge[2] - bbox_badge[0]
    draw.text((CX - w_badge // 2, rule_y + 55), badge, font=font_badge, fill=GOLD_DARK + (220,))

    # Save to Downloads
    img.save(OUTPUT_PATH, format="PNG", optimize=True)
    print(f"✅ Generated YouTube Channel Banner: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_banner()
