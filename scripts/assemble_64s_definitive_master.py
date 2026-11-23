#!/usr/bin/env python3
"""
Assemble the 64-Second Definitive Broadcast Master for Ramayana Episode 2:
- Track: Ramayana (Morning Track A)
- Episode: "भगवान परशुराम का मिथिला में आगमन: पिनाक टूटने पर भीषण क्रोध और लक्ष्मण-राम संवाद"
- Duration: ~63.0s (Full, Complete, Satisfying Narrative Arc)
- Structure:
  1. Scene 1 (0 to 13.0s): Context, Mithila shaking, Parashurama enters roaring in wrath
  2. Scene 2 (13.0 to 23.0s): Fearless Lakshmana smiling and taunting; Parashurama raises his axe
  3. Scene 3 (23.0 to 38.0s): Shri Rama steps between them with folded hands ("नाथ संभुधनु भंजनिहारा...")
  4. Scene 4 (38.0 to 51.0s): Divine revelation; Parashurama realizes Rama is Bhagwan Vishnu & surrenders
  5. Scene 5 (51.0 to 63.0s): Sacred aftermath, Shankh conch, epilogue, and Part 3 wedding hook!
- Zero rushed cuts, zero unexplained characters, 100% authentic Surya-vamsha Kirita Mukuta!
"""

import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
STORAGE_DIR = BASE_DIR / "storage"
SHOTS_DIR = STORAGE_DIR / "rendered" / "ramayana_ep02"
AUDIO_DIR = STORAGE_DIR / "audio" / "ramayana_ep02" / "extended"
WORK_DIR = SHOTS_DIR / "work_64s"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Visual Stems
SHOT1 = SHOTS_DIR / "shot1_parashurama_arrival.mp4"
SHOT2 = SHOTS_DIR / "shot2_parashurama_speaking_hindi.mp4"
SHOT3 = SHOTS_DIR / "shot3_lakshmana_speaking_hindi.mp4"
SHOT4 = SHOTS_DIR / "shot4_rama_serenity_outro.mp4"

# Audio Stems (Authentic Google Charon)
AUDIO1 = AUDIO_DIR / "ext_01_hook_parashurama.wav"
AUDIO2 = AUDIO_DIR / "ext_02_lakshmana_bridge.wav"
AUDIO3 = AUDIO_DIR / "ext_03_rama_entry_and_dialogue.wav"
AUDIO4 = AUDIO_DIR / "ext_04_divine_revelation.wav"
AUDIO5 = AUDIO_DIR / "ext_05_outro.wav"
BGM = STORAGE_DIR / "audio" / "music" / "bgm_sacred_epic_orchestral.aac"
SHANKH = STORAGE_DIR / "audio" / "sfx" / "sfx_divine_shankh.aac"

# Intermediate Segments
SEG1 = WORK_DIR / "seg1.mp4"
SEG2 = WORK_DIR / "seg2.mp4"
SEG3 = WORK_DIR / "seg3.mp4"
SEG4 = WORK_DIR / "seg4.mp4"
SEG5 = WORK_DIR / "seg5.mp4"
CONCAT_VIDEO = WORK_DIR / "concat_raw.mp4"

FINAL_OUTPUT = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep02_Hindi_FINAL.mp4")
STORAGE_FINAL = SHOTS_DIR / "Itihasa_Saga_Ramayana_Ep02_Hindi_64s_FINAL.mp4"

def run(cmd: list):
    print("\nExecuting:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("ERROR STDERR:\n", res.stderr)
        raise RuntimeError(f"FFmpeg command failed: {res.stderr}")
    return res

def create_header_badge(output_path: Path):
    text = "रामायण • भाग 2"
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    try:
        font = ImageFont.truetype(font_path, 44)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 46, 16
    badge_w, badge_h = text_w + pad_x * 2, text_h + pad_y * 2
    badge_x, badge_y = (1080 - badge_w) // 2, 140

    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=26,
        fill=(12, 10, 8, 220),
        outline=(218, 165, 32, 245),
        width=3
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), text, font=font, fill=(255, 255, 255, 255))
    img.save(output_path)

def create_sub_card(lines: list, output_path: Path, speaker: str = None):
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    font_main = ImageFont.truetype(font_path, 34)
    font_speaker = ImageFont.truetype(font_path, 30)

    total_text_h = sum(draw.textbbox((0, 0), l, font=font_main)[3] - draw.textbbox((0, 0), l, font=font_main)[1] for l in lines) + (len(lines) - 1) * 12
    if speaker:
        total_text_h += 42

    pad_y, pad_x = 18, 36
    badge_h = total_text_h + pad_y * 2
    max_w = max(draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0] for l in lines)
    if speaker:
        max_w = max(max_w, draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0])
    badge_w = min(1000, max_w + pad_x * 2)
    badge_x = (1080 - badge_w) // 2
    badge_y = 1570 - badge_h // 2

    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=20,
        fill=(8, 8, 8, 225),
        outline=(218, 165, 32, 235) if speaker else (255, 255, 255, 140),
        width=2
    )

    curr_y = badge_y + pad_y
    if speaker:
        s_w = draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0]
        draw.text(((1080 - s_w) // 2, curr_y), speaker, font=font_speaker, fill=(255, 215, 0, 255))
        curr_y += 38

    for l in lines:
        l_w = draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0]
        draw.text(((1080 - l_w) // 2, curr_y), l, font=font_main, fill=(255, 255, 255, 255))
        curr_y += 46

    img.save(output_path)

def main():
    print("🎬 Assembling Definitive 63-Second Ramayana Ep 2 Master...")

    # 1. Segment 1: Parashurama Arrival & Roar (13.0s)
    # Video slowed down smoothly to match 13s, video audio muted, Charon audio active
    print("\n--- Segment 1: Parashurama Arrival (13.0s) ---")
    cmd_seg1 = [
        "ffmpeg", "-y",
        "-i", str(SHOT1),
        "-i", str(AUDIO1),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.616*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:13.0,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.12,atrim=0:13.0,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=0:13.0,asetpts=PTS-STARTPTS,afade=t=in:ss=0:d=1.0,volume=0.20[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "13.0",
        str(SEG1)
    ]
    run(cmd_seg1)

    # 2. Segment 2: Lakshmana Fearless Smile & Defiance (10.0s)
    print("\n--- Segment 2: Lakshmana Defiance (10.0s) ---")
    cmd_seg2 = [
        "ffmpeg", "-y",
        "-i", str(SHOT3),
        "-i", str(AUDIO2),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.243*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:10.0,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.11,atrim=0:10.0,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=13.0:23.0,asetpts=PTS-STARTPTS,volume=0.18[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "10.0",
        str(SEG2)
    ]
    run(cmd_seg2)

    # 3. Segment 3: Prabhu Shri Rama Steps In & Humble Words (15.0s)
    print("\n--- Segment 3: Shri Rama's Protection & Dialogue (15.0s) ---")
    cmd_seg3 = [
        "ffmpeg", "-y",
        "-i", str(SHOT4),
        "-i", str(AUDIO3),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.865*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:15.0,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.15,atrim=0:15.0,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=23.0:38.0,asetpts=PTS-STARTPTS,volume=0.20[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "15.0",
        str(SEG3)
    ]
    run(cmd_seg3)

    # 4. Segment 4: Divine Revelation & Parashurama Surrenders (13.0s)
    print("\n--- Segment 4: Parashurama Realization (13.0s) ---")
    cmd_seg4 = [
        "ffmpeg", "-y",
        "-i", str(SHOT2),
        "-i", str(AUDIO4),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.616*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:13.0,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.12,atrim=0:13.0,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=38.0:51.0,asetpts=PTS-STARTPTS,volume=0.20[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "13.0",
        str(SEG4)
    ]
    run(cmd_seg4)

    # 5. Segment 5: Sacred Epilogue, Shankh & Part 3 Hook (12.0s)
    print("\n--- Segment 5: Sacred Shankh & Outro (12.0s) ---")
    cmd_seg5 = [
        "ffmpeg", "-y",
        "-i", str(SHOT4),
        "-i", str(AUDIO5),
        "-i", str(BGM),
        "-i", str(SHANKH),
        "-filter_complex",
        "[0:v]setpts=1.492*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:12.0,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.18,atrim=0:12.0,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=51.0:63.0,asetpts=PTS-STARTPTS,afade=t=out:st=10.0:d=2.0,volume=0.20[a_bgm];"
        "[3:a]adelay=4500|4500,volume=1.2,afade=t=out:st=10.0:d=2.0[a_shankh];"
        "[a_voice][a_bgm][a_shankh]amix=inputs=3:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "12.0",
        str(SEG5)
    ]
    run(cmd_seg5)

    # Concatenate all 5 segments
    print("\n--- Concatenating 5 Segments into 63s Stream ---")
    concat_list = WORK_DIR / "concat_list.txt"
    concat_list.write_text(f"file '{SEG1}'\nfile '{SEG2}'\nfile '{SEG3}'\nfile '{SEG4}'\nfile '{SEG5}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(CONCAT_VIDEO)])

    # Generate UI Overlays
    header_badge = WORK_DIR / "badge.png"
    create_header_badge(header_badge)

    sub1 = WORK_DIR / "sub1.png"
    create_sub_card([
        "शिवजी का पिनाक धनुष टूटते ही तीनों लोक कांप उठे!",
        "हाथ में काल-समान फरसा लिए प्रगट हुए भगवान परशुराम!",
        "'किसने तोड़ा महादेव का पिनाक? वर्ना मिथिला भस्म कर दूँगा!'"
    ], sub1, speaker="भगवान परशुराम")

    sub2 = WORK_DIR / "sub2.png"
    create_sub_card([
        "भयभीत सभा में निर्भीक छोटे भाई लक्ष्मण मुस्कुराकर बोले...",
        "'बचपन में कई धनुहियां तोड़ीं, इस पुराने धनुष पर ममता क्यों?'",
        "क्रोधित परशुराम ने लक्ष्मण पर फरसा तान लिया!"
    ], sub2, speaker="लक्ष्मण")

    sub3 = WORK_DIR / "sub3.png"
    create_sub_card([
        "लक्ष्मण की रक्षा हेतु आगे बढ़े मर्यादा पुरुषोत्तम प्रभु श्री राम!",
        "दोनों हाथ जोड़कर अत्यंत विनम्रता से बोले—",
        "'हे नाथ! शिवजी के धनुष को तोड़ने वाला आपका ही कोई दास होगा!'"
    ], sub3, speaker="मर्यादा पुरुषोत्तम प्रभु श्री राम")

    sub4 = WORK_DIR / "sub4.png"
    create_sub_card([
        "श्री राम की असीम विनम्रता और दिव्य तेज को देखकर",
        "परशुराम समझ गए कि सामने साक्षात भगवान विष्णु हैं!",
        "उनका सारा क्रोध पिघल गया और वे नतमस्तक हो गए!"
    ], sub4)

    sub5 = WORK_DIR / "sub5.png"
    create_sub_card([
        "प्रभु श्री राम ने अपनी मर्यादा से महाप्रलय को टाल दिया!",
        "अगला भाग 3: श्री राम और सीता जी का दिव्य विवाह!",
        "इतिहास सागा (@itihasasaga) को अभी फॉलो करें!"
    ], sub5)

    # Burn Overlays into Final Master
    print("\n--- Burning Overlays into Final Broadcast Master ---")
    cmd_burn = [
        "ffmpeg", "-y",
        "-i", str(CONCAT_VIDEO),
        "-i", str(header_badge),
        "-i", str(sub1),
        "-i", str(sub2),
        "-i", str(sub3),
        "-i", str(sub4),
        "-i", str(sub5),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0[v1];"
        "[v1][2:v]overlay=0:0:enable='between(t,0,13.0)'[v2];"
        "[v2][3:v]overlay=0:0:enable='between(t,13.0,23.0)'[v3];"
        "[v3][4:v]overlay=0:0:enable='between(t,23.0,38.0)'[v4];"
        "[v4][5:v]overlay=0:0:enable='between(t,38.0,51.0)'[v5];"
        "[v5][6:v]overlay=0:0:enable='between(t,51.0,63.0)'[v_final]",
        "-map", "[v_final]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart",
        str(STORAGE_FINAL)
    ]
    run(cmd_burn)

    shutil.copy2(STORAGE_FINAL, FINAL_OUTPUT)
    print(f"\n✨ SUCCESS! 63-Second Master Video Delivered to:")
    print(f"👉 {FINAL_OUTPUT} ({FINAL_OUTPUT.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
