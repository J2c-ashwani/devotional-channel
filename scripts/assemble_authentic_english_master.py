#!/usr/bin/env python3
"""
Assemble Authentic English Master Video with Character Lip-Sync & Indian Accent:
1. Scene 1 (The Iron Vault & Warriors): 
   - No character speaking on camera.
   - Authentic Indian English narrator voiceover (en-IN-PrabhatNeural).
   - Video: shot1_pinaka_vault_t2v.mp4 extended to 13.39s.

2. Scene 2A (King Janaka on Throne):
   - King Janaka speaks with grief upon his throne.
   - 100% ORIGINAL NATIVE AUDIO & LIP-SYNC from king_janaka_omni_clip.mp4.
   - Zero external voiceover dubbing over him.
   - Authentic Indian accent, real person talking.

3. Scene 2B (Sage Vishvamitra Commanding Rama):
   - Sage Vishvamitra commanding Prince Rama in Mithila court.
   - NATIVE AUDIO from vishvamitra_omni_clip.mp4.

4. Scene 3 (Shri Rama Lifting & Snapping Bow):
   - Action kinetic climax: Rama hoists bow, pulls string, bow snaps in half.
   - NATIVE ACTION AUDIO from rama_breaks_bow_action_omni.mp4 + thunder crack.

5. Scene 4 (Celebration & Follow CTA):
   - Palace sunrise, divine flowers shower.
   - Authentic Indian English narrator voiceover + Shankh conch.
"""

import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
OUTPUT_DIR = STORAGE_DIR / "rendered" / "authentic_english"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Visual Assets (Gemini Omni 1.2 Flash Pure Text-to-Video)
CLIP1 = STORAGE_DIR / "rendered" / "shot1_pinaka_vault_t2v.mp4"
CLIP2A = STORAGE_DIR / "rendered" / "king_janaka_omni_clip.mp4"
CLIP2B = STORAGE_DIR / "rendered" / "vishvamitra_omni_clip.mp4"
CLIP3 = STORAGE_DIR / "rendered" / "rama_breaks_bow_action_omni.mp4"
CLIP4 = STORAGE_DIR / "rendered" / "shot4_rama_sita_celebration_omni.mp4"

# Audio Narration Assets (Authentic Indian English)
VOICE_SC1 = STORAGE_DIR / "audio" / "english_narration_indian" / "scene_01_indian.mp3"
VOICE_SC4 = STORAGE_DIR / "audio" / "english_narration_indian" / "scene_04_indian.mp3"

# SFX & BGM
BGM = STORAGE_DIR / "audio" / "music" / "bgm_sacred_epic_orchestral.aac"
THUNDER = STORAGE_DIR / "audio" / "sfx" / "sfx_thunder_rumble.aac"
SHANKH = STORAGE_DIR / "audio" / "sfx" / "sfx_divine_shankh.aac"

# Intermediate Rendered Segments
SEG1 = OUTPUT_DIR / "seg1_vault.mp4"
SEG2A = OUTPUT_DIR / "seg2a_janaka.mp4"
SEG2B = OUTPUT_DIR / "seg2b_vishvamitra.mp4"
SEG3 = OUTPUT_DIR / "seg3_action.mp4"
SEG4 = OUTPUT_DIR / "seg4_celebration.mp4"

FINAL_OUTPUT = STORAGE_DIR / "rendered" / "ramayana_part1_english_pure_t2v.mp4"
DOWNLOADS_OUTPUT = Path("/Users/ashwanikumar/Downloads/ramayana_part1_english_pure_t2v.mp4")

def run(cmd: list):
    print("Executing:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("ERROR STDERR:\n", res.stderr)
        raise RuntimeError(f"FFmpeg command failed: {res.stderr}")
    return res

def generate_header_badge(text: str, output_path: Path):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 44)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad_x = 44
    pad_y = 16
    badge_w = text_w + pad_x * 2
    badge_h = text_h + pad_y * 2
    badge_x = (1080 - badge_w) // 2
    badge_y = 140
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=24,
        fill=(15, 12, 10, 190),
        outline=(212, 175, 55, 240),
        width=3
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), text, font=font, fill=(255, 255, 255, 255))
    img.save(output_path)
    print(f"Header badge saved to {output_path}")

def main():
    print("=== Rendering Authentic English Master with Character Lip-Sync ===")

    # -------------------------------------------------------------
    # 1. Segment 1: The Pinaka Vault & Warriors (Duration: 13.39s)
    # Ping-pong / extend video to 13.39s, mix Indian voiceover + ambient BGM + subtle native sound
    # -------------------------------------------------------------
    print("\n--- Segment 1: Iron Vault (Indian Narrator Voiceover) ---")
    cmd_seg1 = [
        "ffmpeg", "-y",
        "-i", str(CLIP1),
        "-i", str(VOICE_SC1),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30[base];"
        "[base]split=3[v1][v2_in][v3];"
        "[v2_in]reverse[v2];"
        "[v1][v2][v3]concat=n=3:v=1:a=0,trim=0:13.39,setpts=PTS-STARTPTS[v_out];"
        "[0:a]volume=0.3[a_native];"
        "[1:a]volume=1.0[a_voice];"
        "[2:a]volume=0.15,atrim=0:13.39,afade=t=in:ss=0:d=1.0[a_bgm];"
        "[a_voice][a_native][a_bgm]amix=inputs=3:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "13.39",
        str(SEG1)
    ]
    run(cmd_seg1)

    # -------------------------------------------------------------
    # 2. Segment 2A: King Janaka on Throne (Duration: 8.04s)
    # 100% NATIVE OMNI VIDEO + NATIVE OMNI AUDIO & LIP-SYNC!
    # King Janaka speaks in his authentic Indian accent with sorrow.
    # -------------------------------------------------------------
    print("\n--- Segment 2A: King Janaka (Original Native Lip-Sync & Voice) ---")
    cmd_seg2a = [
        "ffmpeg", "-y",
        "-i", str(CLIP2A),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,setpts=PTS-STARTPTS[v_out];"
        "[0:a]volume=1.8,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "8.04",
        str(SEG2A)
    ]
    run(cmd_seg2a)

    # -------------------------------------------------------------
    # 3. Segment 2B: Sage Vishvamitra (Duration: 8.04s)
    # NATIVE OMNI VIDEO + NATIVE OMNI AUDIO
    # -------------------------------------------------------------
    print("\n--- Segment 2B: Sage Vishvamitra (Original Native Video & Audio) ---")
    cmd_seg2b = [
        "ffmpeg", "-y",
        "-i", str(CLIP2B),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,setpts=PTS-STARTPTS[v_out];"
        "[0:a]volume=1.4,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "8.04",
        str(SEG2B)
    ]
    run(cmd_seg2b)

    # -------------------------------------------------------------
    # 4. Segment 3: Shri Rama Action (Duration: 8.04s)
    # Rama hoists the bow, pulls the string, bow snaps in half!
    # NATIVE OMNI VIDEO + NATIVE AUDIO + THUNDER IMPACT
    # -------------------------------------------------------------
    print("\n--- Segment 3: Rama Action (Lifting & Snapping Bow) ---")
    cmd_seg3 = [
        "ffmpeg", "-y",
        "-i", str(CLIP3),
        "-i", str(THUNDER),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,setpts=PTS-STARTPTS[v_out];"
        "[0:a]volume=1.2[a_native];"
        "[1:a]adelay=4000|4000,volume=0.9[a_sfx];"
        "[a_native][a_sfx]amix=inputs=2:duration=first:dropout_transition=1,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "8.04",
        str(SEG3)
    ]
    run(cmd_seg3)

    # -------------------------------------------------------------
    # 5. Segment 4: Celebration & Follow CTA (Duration: 12.12s)
    # Celestial flowers shower + Indian English narrator CTA + Shankh
    # -------------------------------------------------------------
    print("\n--- Segment 4: Celebration (Clean Studio Voiceover & Shankh Finale) ---")
    cmd_seg4 = [
        "ffmpeg", "-y",
        "-i", str(CLIP4),
        "-i", str(VOICE_SC4),
        "-i", str(SHANKH),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30[base];"
        "[base]split=3[v1][v2_in][v3];"
        "[v2_in]reverse[v2];"
        "[v1][v2][v3]concat=n=3:v=1:a=0,trim=0:12.12,setpts=PTS-STARTPTS[v_out];"
        "[1:a]volume=1.0[a_voice];"
        "[2:a]adelay=6000|6000,volume=0.85[a_shankh];"
        "[3:a]volume=0.15,atrim=0:12.12,afade=t=out:st=10.5:d=1.5[a_bgm];"
        "[a_voice][a_shankh][a_bgm]amix=inputs=3:duration=first:dropout_transition=2,afade=t=out:st=10.5:d=1.5,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", "12.12",
        str(SEG4)
    ]
    run(cmd_seg4)

    # -------------------------------------------------------------
    # 6. Final Concatenation with Episode Header Badge
    # -------------------------------------------------------------
    print("\n--- Final Concatenation of All 5 Segments with Header Badge ---")
    badge_path = OUTPUT_DIR / "badge_overlay.png"
    generate_header_badge("RAMAYANA  •  PART 1", badge_path)

    concat_list = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for s in [SEG1, SEG2A, SEG2B, SEG3, SEG4]:
            f.write(f"file '{s.resolve()}'\n")

    cmd_final = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-i", str(badge_path),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0,eq=contrast=1.04:brightness=0.01:saturation=1.12[v_out]",
        "-map", "[v_out]",
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        str(FINAL_OUTPUT)
    ]
    run(cmd_final)
    print(f"\n Master Authentic English Video created: {FINAL_OUTPUT}!")

if __name__ == "__main__":
    main()
