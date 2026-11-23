#!/usr/bin/env python3
"""
Assemble Mahabharata Episode 1 Definitive Broadcast Master (V2 - Google Charon Voice & Flowing Cradle):
- Track: Mahabharata (Track B)
- Episode 1: "माँ गंगा का त्याग और देवव्रत का जन्म: जब राजा शांतनु ने तोड़ा अपना वचन"
- Updates based on user feedback:
  1. Voice: Google Charon (the authentic mature Kathavachak voice from Ramayana Part 1)
  2. Scene 1 Visual: Goddess Ganga gently placing the sacred cradle into the flowing river Ganga
  3. Audio Purity: 100% MUTE original video audio in Scene 1 & 4 — zero conflicting background chatter!
  4. Scene 2 & 3: Original native character Hindi lip-sync dialogue from King Shantanu and Goddess Ganga
Total duration: ~29.1s (Broadcast Gold Retention Zone)
"""

import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
STORAGE_DIR = BASE_DIR / "storage"
SHOTS_DIR = STORAGE_DIR / "rendered" / "mahabharata_ep01"
WORK_DIR = SHOTS_DIR / "work_v2"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Visual Assets (Pure Gemini Omni 1.2 Flash)
SHOT1 = SHOTS_DIR / "shot1_ganga_cradle_flowing.mp4"  # NEW: Ganga flowing baby cradle in river
SHOT2 = SHOTS_DIR / "shot2_shantanu_speaking_hindi.mp4"
SHOT3 = SHOTS_DIR / "shot3_ganga_speaking_hindi.mp4"
SHOT4 = SHOTS_DIR / "shot4_ganga_departure.mp4"

# Audio Assets (AUTHENTIC GOOGLE CHARON - SAME AS RAMAYANA PART 1!)
VOICE_HOOK = STORAGE_DIR / "audio" / "mahabharata_ep01" / "scene_01_hook_charon.wav"
VOICE_OUTRO = STORAGE_DIR / "audio" / "mahabharata_ep01" / "scene_04_outro_charon.wav"
BGM = STORAGE_DIR / "audio" / "music" / "bgm_sacred_epic_orchestral.aac"
SHANKH = STORAGE_DIR / "audio" / "sfx" / "sfx_divine_shankh.aac"

# Intermediate Rendered Segments
SEG1 = WORK_DIR / "seg1_cradle_hook.mp4"
SEG2 = WORK_DIR / "seg2_shantanu.mp4"
SEG3 = WORK_DIR / "seg3_ganga.mp4"
SEG4 = WORK_DIR / "seg4_outro.mp4"
CONCAT_VIDEO = WORK_DIR / "concat_raw.mp4"

# Final Master Outputs
FINAL_STORAGE_OUTPUT = SHOTS_DIR / "Itihasa_Saga_Mahabharata_Ep01_Hindi_FINAL.mp4"
FINAL_DOWNLOADS_OUTPUT = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Mahabharata_Ep01_Hindi_FINAL.mp4")

def run(cmd: list):
    print("\nExecuting:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("ERROR STDERR:\n", res.stderr)
        raise RuntimeError(f"FFmpeg command failed: {res.stderr}")
    return res

def create_header_badge(text: str, output_path: Path):
    """Creates top-centered header badge with gold outline and semi-transparent background."""
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    try:
        font = ImageFont.truetype(font_path, 44)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad_x = 46
    pad_y = 16
    badge_w = text_w + pad_x * 2
    badge_h = text_h + pad_y * 2
    badge_x = (1080 - badge_w) // 2
    badge_y = 150

    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=26,
        fill=(12, 10, 8, 210),
        outline=(218, 165, 32, 240),  # Golden Rod #DAA520
        width=3
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), text, font=font, fill=(255, 255, 255, 255))
    img.save(output_path)
    print(f"✅ Header badge created at: {output_path}")

def create_subtitle_card(lines: list, output_path: Path, is_dialogue: bool = False, speaker: str = None):
    """Creates bottom-positioned subtitle card with gold accents."""
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    font_main = ImageFont.truetype(font_path, 42)
    font_speaker = ImageFont.truetype(font_path, 34)
    
    total_text_h = sum(draw.textbbox((0, 0), l, font=font_main)[3] - draw.textbbox((0, 0), l, font=font_main)[1] for l in lines) + (len(lines) - 1) * 16
    if speaker:
        total_text_h += 48
        
    pad_y = 22
    pad_x = 42
    badge_h = total_text_h + pad_y * 2
    max_w = max(draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0] for l in lines)
    if speaker:
        max_w = max(max_w, draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0])
    badge_w = min(1000, max_w + pad_x * 2)
    badge_x = (1080 - badge_w) // 2
    badge_y = 1560 - badge_h // 2
    
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=22,
        fill=(10, 10, 10, 215),
        outline=(218, 165, 32, 235) if is_dialogue else (255, 255, 255, 140),
        width=2
    )
    
    curr_y = badge_y + pad_y
    if speaker:
        s_w = draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0]
        draw.text(((1080 - s_w) // 2, curr_y), speaker, font=font_speaker, fill=(255, 215, 0, 255))
        curr_y += 46
        
    for l in lines:
        l_w = draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0]
        draw.text(((1080 - l_w) // 2, curr_y), l, font=font_main, fill=(255, 255, 255, 255))
        curr_y += 56
        
    img.save(output_path)
    print(f"✅ Subtitle card saved: {output_path}")

def main():
    print("=" * 60)
    print("🎬 Assembling Mahabharata Ep 01 Definitive Master (V2)")
    print("   Featuring Google Charon Voice & Flowing Cradle Visual")
    print("=" * 60)

    # 1. Segment 1: Opening Hook with Flowing Cradle (8.04s)
    # ZERO VIDEO AUDIO (Completely Mute [0:a] to eliminate background chatter)
    # ONLY Google Charon voice + Sacred BGM
    print("\n--- 1. Rendering Segment 1: Ganga Flowing Cradle (8.04s) ---")
    cmd_seg1 = [
        "ffmpeg", "-y",
        "-i", str(SHOT1),
        "-i", str(VOICE_HOOK),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]trim=0:8.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v_out];"
        "[1:a]atempo=1.08,atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=0:8.04,asetpts=PTS-STARTPTS,afade=t=in:ss=0:d=1.0,volume=0.18[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04",
        str(SEG1)
    ]
    run(cmd_seg1)

    # 2. Segment 2: King Shantanu Anguish (5.03s)
    # NATIVE LIP-SYNC CHARACTER AUDIO from King Shantanu + subtle BGM
    print("\n--- 2. Rendering Segment 2: Shantanu Native Lip-Sync (5.03s) ---")
    cmd_seg2 = [
        "ffmpeg", "-y",
        "-i", str(SHOT2),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]trim=0:5.03,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v_out];"
        "[0:a]atrim=0:5.03,asetpts=PTS-STARTPTS,volume=1.8[a_speech];"
        "[1:a]atrim=8.04:13.07,asetpts=PTS-STARTPTS,volume=0.12[a_bgm];"
        "[a_speech][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "5.03",
        str(SEG2)
    ]
    run(cmd_seg2)

    # 3. Segment 3: Goddess Ganga Revelation & Farewell (8.04s)
    # NATIVE LIP-SYNC CHARACTER AUDIO from Goddess Ganga + subtle BGM
    print("\n--- 3. Rendering Segment 3: Goddess Ganga Native Lip-Sync (8.04s) ---")
    cmd_seg3 = [
        "ffmpeg", "-y",
        "-i", str(SHOT3),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]trim=0:8.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v_out];"
        "[0:a]atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.8[a_speech];"
        "[1:a]atrim=13.07:21.11,asetpts=PTS-STARTPTS,volume=0.12[a_bgm];"
        "[a_speech][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04",
        str(SEG3)
    ]
    run(cmd_seg3)

    # 4. Segment 4: Celestial Departure & Outro (8.04s)
    # ZERO VIDEO AUDIO (Clean Google Charon Outro + BGM + Divine Shankh)
    print("\n--- 4. Rendering Segment 4: Charon Outro & Shankh (8.04s) ---")
    cmd_seg4 = [
        "ffmpeg", "-y",
        "-i", str(SHOT4),
        "-i", str(VOICE_OUTRO),
        "-i", str(BGM),
        "-i", str(SHANKH),
        "-filter_complex",
        "[0:v]trim=0:8.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v_out];"
        "[1:a]atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=21.11:29.15,asetpts=PTS-STARTPTS,afade=t=out:st=6.5:d=1.5,volume=0.18[a_bgm];"
        "[3:a]adelay=4200|4200,volume=0.65[a_shankh];"
        "[a_voice][a_bgm][a_shankh]amix=inputs=3:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04",
        str(SEG4)
    ]
    run(cmd_seg4)

    # 5. Concatenate Segments
    print("\n--- 5. Concatenating 4 Segments into Unified Stream ---")
    concat_list = WORK_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        f.write(f"file '{SEG1.resolve()}'\n")
        f.write(f"file '{SEG2.resolve()}'\n")
        f.write(f"file '{SEG3.resolve()}'\n")
        f.write(f"file '{SEG4.resolve()}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        str(CONCAT_VIDEO)
    ]
    run(cmd_concat)

    # 6. Generate Badges & Subtitle Cards
    print("\n--- 6. Creating Header Badge & Subtitle Overlays ---")
    badge_png = WORK_DIR / "badge_header.png"
    create_header_badge("महाभारत • भाग 1", badge_png)

    sub1_png = WORK_DIR / "sub_01_hook.png"
    create_subtitle_card(["महाराज शांतनु और देवी गंगा का वह वचन,", "जिसने महाभारत की नींव रखी!"], sub1_png)

    sub2_png = WORK_DIR / "sub_02_shantanu.png"
    create_subtitle_card(["हे गंगे! रुक जाओ!", "यह मेरा आठवाँ पुत्र है, इसे मत बहाओ!"], sub2_png, is_dialogue=True, speaker="राजा शांतनु")

    sub3a_png = WORK_DIR / "sub_03a_ganga.png"
    create_subtitle_card(["हे राजन्! तुमने अपना वचन तोड़ दिया!", "अब मैं तुम्हारे साथ नहीं रह सकती!"], sub3a_png, is_dialogue=True, speaker="देवी गंगा")

    sub3b_png = WORK_DIR / "sub_03b_ganga.png"
    create_subtitle_card(["पर देवव्रत अवश्य जीवित रहेगा!", "मैं इसे सर्वश्रेष्ठ योद्धा बनाकर लौटाऊँगी!"], sub3b_png, is_dialogue=True, speaker="देवी गंगा")

    sub4_png = WORK_DIR / "sub_04_outro.png"
    create_subtitle_card(["और इस प्रकार जन्मा वह महायोद्धा 'भीष्म'!", "महाभारत • भाग 2 के लिए अभी फॉलो करें!"], sub4_png, is_dialogue=False)

    # 7. Burn Overlays onto Master Video
    # Timing:
    # Seg 1: 0.0 to 8.04
    # Seg 2: 8.04 to 13.07
    # Seg 3: 13.07 to 21.11
    # Seg 4: 21.11 to 29.15
    print("\n--- 7. Burning All Overlays onto Final Broadcast Master ---")
    filter_complex = (
        "[0:v][1:v]overlay=0:0[v0];"
        "[v0][2:v]overlay=0:0:enable='between(t,0.5,7.8)'[v1];"
        "[v1][3:v]overlay=0:0:enable='between(t,8.2,12.8)'[v2];"
        "[v2][4:v]overlay=0:0:enable='between(t,13.2,17.2)'[v3];"
        "[v3][5:v]overlay=0:0:enable='between(t,17.2,21.0)'[v4];"
        "[v4][6:v]overlay=0:0:enable='between(t,21.5,28.8)'[v_out]"
    )

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(CONCAT_VIDEO),
        "-i", str(badge_png),
        "-i", str(sub1_png),
        "-i", str(sub2_png),
        "-i", str(sub3a_png),
        "-i", str(sub3b_png),
        "-i", str(sub4_png),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        str(FINAL_STORAGE_OUTPUT)
    ]
    run(cmd_final)

    # Deliver to Downloads
    shutil.copyfile(FINAL_STORAGE_OUTPUT, FINAL_DOWNLOADS_OUTPUT)
    print(f"\n🎉 DEFINITIVE BROADCAST MASTER V2 COMPLETE & DELIVERED!")
    print(f"📁 Storage: {FINAL_STORAGE_OUTPUT} ({FINAL_STORAGE_OUTPUT.stat().st_size} bytes)")
    print(f"📁 Downloads: {FINAL_DOWNLOADS_OUTPUT} ({FINAL_DOWNLOADS_OUTPUT.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
