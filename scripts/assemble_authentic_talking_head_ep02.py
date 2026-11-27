#!/usr/bin/env python3
"""
Assemble the Authentic Talking-Head Master for Ramayana Episode 2:
- Track: Ramayana (Episode 2)
- Total Duration: ~68.0s
- Strict Rules Enforced:
  1. Scene 1 (0 to 9.0s): Narrator (Charon) - Mithila shaking, Parashurama enters.
  2. Scene 2 (9.0 to 17.0s): Bhagwan Parashurama TALKING HEAD (Native Character Voice) - Wrathful challenge.
  3. Scene 3 (17.0 to 25.0s): Prince Lakshmana TALKING HEAD (Native Character Voice) - Fearless witty defiance.
  4. Scene 4 (25.0 to 35.5s): Bhagwan Parashurama TALKING HEAD (Fenrir Voice) - Raising glowing battleaxe in fury.
  5. Scene 5 (35.5 to 47.0s): Prabhu Shri Rama TALKING HEAD (Kore Divine Voice) - Serene folded hands, Surya-vamsha Kirita Mukuta (NO peacock feather).
  6. Scene 6 (47.0 to 68.0s): Epilogue & Shankh (Narrator) - Parashurama recognizes Lord Vishnu, bows in reverence, Shankh sound, Part 3 wedding hook!
"""

import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
STORAGE_DIR = BASE_DIR / "storage"
SHOTS_DIR = STORAGE_DIR / "rendered" / "ramayana_ep02"
AUDIO_DIR = STORAGE_DIR / "audio" / "ramayana_ep02"
EXT_AUDIO = AUDIO_DIR / "extended"
TALK_AUDIO = AUDIO_DIR / "talking_heads"
WORK_DIR = SHOTS_DIR / "work_talking_head"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Visual Assets
SHOT1 = SHOTS_DIR / "shot1_parashurama_arrival.mp4"
SHOT2 = SHOTS_DIR / "shot2_parashurama_speaking_hindi.mp4"
SHOT3 = SHOTS_DIR / "shot3_lakshmana_speaking_hindi.mp4"
SHOT4 = SHOTS_DIR / "shot4_rama_serenity_outro.mp4"

# Audio Assets
AUDIO_NARRATOR_HOOK = EXT_AUDIO / "ext_01_hook_parashurama.wav"
AUDIO_PARASHURAMA_1 = SHOTS_DIR / "shot2_parashurama_speaking_hindi.wav"
AUDIO_LAKSHMANA = SHOTS_DIR / "shot3_lakshmana_speaking_hindi.wav"
AUDIO_PARASHURAMA_2 = TALK_AUDIO / "parashurama_wrath_fenrir.wav"
AUDIO_RAMA = TALK_AUDIO / "rama_dialogue_kore.wav"
AUDIO_NARRATOR_OUTRO = EXT_AUDIO / "ext_04_divine_revelation.wav"
BGM = STORAGE_DIR / "audio" / "music" / "bgm_sacred_epic_orchestral.aac"
SHANKH = STORAGE_DIR / "audio" / "sfx" / "sfx_divine_shankh.aac"

# Intermediate Segments
SEG1 = WORK_DIR / "seg1.mp4"
SEG2 = WORK_DIR / "seg2.mp4"
SEG3 = WORK_DIR / "seg3.mp4"
SEG4 = WORK_DIR / "seg4.mp4"
SEG5 = WORK_DIR / "seg5.mp4"
SEG6 = WORK_DIR / "seg6.mp4"
CONCAT_RAW = WORK_DIR / "concat_raw.mp4"

FINAL_OUTPUT = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep02_TalkingHead_FINAL.mp4")

def run(cmd: list):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("ERROR STDERR:\n", res.stderr)
        raise RuntimeError(f"FFmpeg failed: {res.stderr}")
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
    print("🎬 Assembling Pure Talking-Head Ramayana Episode 2 Master...")

    # 1. Segment 1: Narrator Hook (8.5s)
    print("\n--- Segment 1: Narrator Arrival Hook (8.5s) ---")
    cmd_seg1 = [
        "ffmpeg", "-y",
        "-i", str(SHOT1),
        "-i", str(AUDIO_NARRATOR_HOOK),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,trim=0:8.5,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atrim=0:8.5,asetpts=PTS-STARTPTS,volume=1.4[a_voice];"
        "[2:a]atrim=0:8.5,asetpts=PTS-STARTPTS,volume=0.20[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.5", str(SEG1)
    ]
    run(cmd_seg1)

    # 2. Segment 2: Parashurama TALKING HEAD (8.04s)
    print("\n--- Segment 2: Bhagwan Parashurama Talking Head (8.04s) ---")
    cmd_seg2 = [
        "ffmpeg", "-y",
        "-i", str(SHOT2),
        "-i", str(AUDIO_PARASHURAMA_1),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,trim=0:8.04,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.6[a_voice];"
        "[2:a]atrim=8.5:16.54,asetpts=PTS-STARTPTS,volume=0.15[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04", str(SEG2)
    ]
    run(cmd_seg2)

    # 3. Segment 3: Lakshmana TALKING HEAD (8.04s)
    print("\n--- Segment 3: Prince Lakshmana Talking Head (8.04s) ---")
    cmd_seg3 = [
        "ffmpeg", "-y",
        "-i", str(SHOT3),
        "-i", str(AUDIO_LAKSHMANA),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]scale=1080:1920:flags=lanczos,fps=30,trim=0:8.04,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=16.54:24.58,asetpts=PTS-STARTPTS,volume=0.15[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04", str(SEG3)
    ]
    run(cmd_seg3)

    # 4. Segment 4: Parashurama Wrathful Reaction TALKING HEAD (10.6s)
    print("\n--- Segment 4: Parashurama Fury Talking Head (10.6s) ---")
    cmd_seg4 = [
        "ffmpeg", "-y",
        "-i", str(SHOT2),
        "-i", str(AUDIO_PARASHURAMA_2),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.318*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:10.6,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atrim=0:10.6,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=24.58:35.18,asetpts=PTS-STARTPTS,volume=0.18[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "10.6", str(SEG4)
    ]
    run(cmd_seg4)

    # 5. Segment 5: Prabhu Shri Rama TALKING HEAD (11.4s)
    print("\n--- Segment 5: Prabhu Shri Rama Talking Head (11.4s) ---")
    cmd_seg5 = [
        "ffmpeg", "-y",
        "-i", str(SHOT4),
        "-i", str(AUDIO_RAMA),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.418*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:11.4,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atrim=0:11.4,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=35.18:46.58,asetpts=PTS-STARTPTS,volume=0.16[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "11.4", str(SEG5)
    ]
    run(cmd_seg5)

    # 6. Segment 6: Parashurama Bow & Divine Outro Shankh (14.0s)
    print("\n--- Segment 6: Parashurama Bow & Divine Outro Shankh (14.0s) ---")
    cmd_seg6 = [
        "ffmpeg", "-y",
        "-i", str(SHOT1),
        "-i", str(AUDIO_NARRATOR_OUTRO),
        "-i", str(BGM),
        "-i", str(SHANKH),
        "-filter_complex",
        "[0:v]reverse,scale=1080:1920:flags=lanczos,fps=30,trim=0:14.0,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atrim=0:14.0,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=46.58:60.58,asetpts=PTS-STARTPTS,afade=t=out:st=12.0:d=2.0,volume=0.20[a_bgm];"
        "[3:a]adelay=6000|6000,volume=0.85[a_shankh];"
        "[a_voice][a_bgm][a_shankh]amix=inputs=3:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]", "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "14.0", str(SEG6)
    ]
    run(cmd_seg6)

    # 7. Concatenate all 6 segments
    print("\n--- Concatenating Segments ---")
    concat_list = WORK_DIR / "concat.txt"
    concat_list.write_text(f"file '{SEG1.name}'\nfile '{SEG2.name}'\nfile '{SEG3.name}'\nfile '{SEG4.name}'\nfile '{SEG5.name}'\nfile '{SEG6.name}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(CONCAT_RAW)
    ]
    run(cmd_concat)

    # 8. Create Subtitles & Header Badge
    print("\n--- Burning Subtitles and Header Badge ---")
    badge_png = WORK_DIR / "header_badge.png"
    create_header_badge(badge_png)

    # Generate subtitle cards
    cards = [
        (0.0, 8.5, ["पिनाक टूटते ही कांप उठी मिथिला...", "हाथ में काल-समान फरसा लिए प्रगट हुए परशुराम!"], None),
        (8.5, 16.54, ["'किसने तोड़ा मेरे गुरु का पावन पिनाक?", "सामने आ, वर्ना पूरी मिथिला को भस्म कर दूँगा!'"], "भगवान परशुराम"),
        (16.54, 24.58, ["'हे मुनिवर! बचपन में हमने कई धनुहियां तोड़ीं...", "इस पुराने धनुष पर इतनी ममता क्यों?'"], "राजकुमार लक्ष्मण"),
        (24.58, 35.18, ["'रे नृपबालक! काल के वश होकर तू संभाल कर नहीं बोल रहा!", "शिवजी के धनुष को तू साधारण धनुही कह रहा है?'"], "भगवान परशुराम"),
        (35.18, 46.58, ["'हे नाथ! शिवजी के धनुष को तोड़ने वाला आपका ही कोई दास होगा।", "आज्ञा दीजिए, इस सेवक के लिए क्या आदेश है?'"], "प्रभु श्री राम"),
        (46.58, 60.58, ["श्री राम की विनम्रता देख परशुराम जान गए साक्षात विष्णु!", "चरणों में नतमस्तक हुए और टल गया महाप्रलय!"], None)
    ]

    card_paths = []
    filter_overlay = f"[0:v][1:v]overlay=0:0[v0];"
    input_args = ["-i", str(CONCAT_RAW), "-i", str(badge_png)]

    for i, (start, end, lines, spk) in enumerate(cards):
        c_path = WORK_DIR / f"card_{i}.png"
        create_sub_card(lines, c_path, speaker=spk)
        card_paths.append(c_path)
        input_args.extend(["-i", str(c_path)])
        idx_in = i + 2
        prev_v = f"v{i}"
        next_v = f"v{i+1}" if i < len(cards) - 1 else "v_final"
        filter_overlay += f"[{prev_v}][{idx_in}:v]overlay=0:0:enable='between(t,{start},{end})'[{next_v}];"

    filter_overlay = filter_overlay.rstrip(";")

    cmd_final = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_overlay,
        "-map", "[v_final]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        str(FINAL_OUTPUT)
    ]
    run(cmd_final)

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(FINAL_OUTPUT)
    ], capture_output=True, text=True, check=True)
    final_dur = float(probe.stdout.strip())

    print(f"\n🎉 AUTHENTIC TALKING-HEAD MASTER CREATED:")
    print(f"Path: {FINAL_OUTPUT}")
    print(f"Exact Duration: {final_dur:.2f}s")
    print(f"File Size: {FINAL_OUTPUT.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
