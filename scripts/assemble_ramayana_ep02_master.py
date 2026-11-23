#!/usr/bin/env python3
"""
Assemble Ramayana Episode 2 Definitive Broadcast Master:
- Track: Ramayana (Morning Track A)
- Episode 2: "भगवान परशुराम का मिथिला में आगमन: पिनाक टूटने पर भीषण क्रोध और लक्ष्मण संवाद"
- Narrative Structure (4 Scenes, ~36.6s):
  1. Scene 1: Arrival of Bhagwan Parashurama with glowing Parashu axe in shaking Mithila durbar (10.52s)
     - Audio: Google Charon Voiceover + Sacred BGM (Video audio completely muted)
  2. Scene 2: Bhagwan Parashurama wrathful dialogue in Hindi (8.04s)
     - Audio: Native character lip-sync dialogue + subtle background score
  3. Scene 3: Prince Lakshmana fearless dialogue in Hindi (8.04s)
     - Audio: Native character lip-sync dialogue + subtle background score
  4. Scene 4: Maryada Purushottam Shri Rama stepping forward with folded hands & serene aura (10.00s)
     - Audio: Google Charon Voiceover + Sacred Shankh SFX + Divine Outro BGM (Video audio completely muted)
- Format: 1080x1920 9:16 Vertical Master
- Header Badge: 'रामायण • भाग 2'
- Full Hindi Subtitles Burned-In
"""

import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
STORAGE_DIR = BASE_DIR / "storage"
SHOTS_DIR = STORAGE_DIR / "rendered" / "ramayana_ep02"
WORK_DIR = SHOTS_DIR / "work"
WORK_DIR.mkdir(parents=True, exist_ok=True)

# Visual Assets (Pure Gemini Omni 1.2 Flash)
SHOT1 = SHOTS_DIR / "shot1_parashurama_arrival.mp4"
SHOT2 = SHOTS_DIR / "shot2_parashurama_speaking_hindi.mp4"
SHOT3 = SHOTS_DIR / "shot3_lakshmana_speaking_hindi.mp4"
SHOT4 = SHOTS_DIR / "shot4_rama_serenity_outro.mp4"

# Audio Assets
VOICE_HOOK = STORAGE_DIR / "audio" / "ramayana_ep02" / "scene_01_hook_charon.wav"
VOICE_OUTRO = STORAGE_DIR / "audio" / "ramayana_ep02" / "scene_04_outro_charon.wav"
BGM = STORAGE_DIR / "audio" / "music" / "bgm_sacred_epic_orchestral.aac"
SHANKH = STORAGE_DIR / "audio" / "sfx" / "sfx_divine_shankh.aac"

# Intermediate Rendered Segments
SEG1 = WORK_DIR / "seg1_parashurama_arrival.mp4"
SEG2 = WORK_DIR / "seg2_parashurama_dialogue.mp4"
SEG3 = WORK_DIR / "seg3_lakshmana_dialogue.mp4"
SEG4 = WORK_DIR / "seg4_rama_outro.mp4"
CONCAT_VIDEO = WORK_DIR / "concat_raw.mp4"

# Final Master Outputs
FINAL_STORAGE_OUTPUT = SHOTS_DIR / "Itihasa_Saga_Ramayana_Ep02_Hindi_FINAL.mp4"
FINAL_DOWNLOADS_OUTPUT = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep02_Hindi_FINAL.mp4")

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
    font_main = ImageFont.truetype(font_path, 36)
    font_speaker = ImageFont.truetype(font_path, 32)
    
    total_text_h = sum(draw.textbbox((0, 0), l, font=font_main)[3] - draw.textbbox((0, 0), l, font=font_main)[1] for l in lines) + (len(lines) - 1) * 14
    if speaker:
        total_text_h += 44
        
    pad_y = 20
    pad_x = 38
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
        outline=(218, 165, 32, 235) if is_dialogue else (255, 255, 255, 150),
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
    print(f"✅ Subtitle card saved: {output_path}")

def main():
    print("=" * 60)
    print("🎬 Assembling Ramayana Ep 02 Definitive Broadcast Master")
    print("   Featuring Google Charon Voice & Mithila Confrontation Visuals")
    print("=" * 60)

    # 1. Segment 1: Bhagwan Parashurama Arrival (10.52s)
    # ZERO VIDEO AUDIO (Mute [0:a] to ensure 100% clean Google Charon voiceover!)
    print("\n--- 1. Rendering Segment 1: Parashurama Arrival (10.52s) ---")
    cmd_seg1 = [
        "ffmpeg", "-y",
        "-i", str(SHOT1),
        "-i", str(VOICE_HOOK),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]setpts=1.3087*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:10.52,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.20,atrim=0:10.52,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=0:10.52,asetpts=PTS-STARTPTS,afade=t=in:ss=0:d=1.0,volume=0.20[a_bgm];"
        "[a_voice][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "10.52",
        str(SEG1)
    ]
    run(cmd_seg1)

    # 2. Segment 2: Bhagwan Parashurama Speaking Hindi Dialogue (8.04s)
    # Keeps video's authentic lip-sync dialogue audio + mixes subtle BGM
    print("\n--- 2. Rendering Segment 2: Parashurama Dialogue (8.04s) ---")
    cmd_seg2 = [
        "ffmpeg", "-y",
        "-i", str(SHOT2),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]trim=0:8.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v_out];"
        "[0:a]atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.5[a_diag];"
        "[1:a]atrim=10.52:18.56,asetpts=PTS-STARTPTS,volume=0.15[a_bgm];"
        "[a_diag][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04",
        str(SEG2)
    ]
    run(cmd_seg2)

    # 3. Segment 3: Prince Lakshmana Dialogue (8.04s)
    # Keeps video's authentic lip-sync dialogue audio + mixes subtle BGM
    print("\n--- 3. Rendering Segment 3: Lakshmana Dialogue (8.04s) ---")
    cmd_seg3 = [
        "ffmpeg", "-y",
        "-i", str(SHOT3),
        "-i", str(BGM),
        "-filter_complex",
        "[0:v]trim=0:8.04,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30[v_out];"
        "[0:a]atrim=0:8.04,asetpts=PTS-STARTPTS,volume=1.5[a_diag];"
        "[1:a]atrim=18.56:26.60,asetpts=PTS-STARTPTS,volume=0.15[a_bgm];"
        "[a_diag][a_bgm]amix=inputs=2:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "8.04",
        str(SEG3)
    ]
    run(cmd_seg3)

    # 4. Segment 4: Maryada Purushottam Shri Rama Outro (10.00s)
    # ZERO VIDEO AUDIO (Clean Google Charon Outro + BGM + Divine Shankh)
    print("\n--- 4. Rendering Segment 4: Rama Serenity & Outro (10.00s) ---")
    cmd_seg4 = [
        "ffmpeg", "-y",
        "-i", str(SHOT4),
        "-i", str(VOICE_OUTRO),
        "-i", str(BGM),
        "-i", str(SHANKH),
        "-filter_complex",
        "[0:v]setpts=1.2434*PTS,scale=1080:1920:flags=lanczos,fps=30,trim=0:10.00,setpts=PTS-STARTPTS[v_out];"
        "[1:a]atempo=1.22,atrim=0:10.00,asetpts=PTS-STARTPTS,volume=1.5[a_voice];"
        "[2:a]atrim=26.60:36.60,asetpts=PTS-STARTPTS,afade=t=out:st=8.5:d=1.5,volume=0.20[a_bgm];"
        "[3:a]adelay=4000|4000,volume=1.1,afade=t=out:st=8.5:d=1.5[a_shankh];"
        "[a_voice][a_bgm][a_shankh]amix=inputs=3:duration=first:dropout_transition=2,loudnorm=I=-14:LRA=7:TP=-1.5[a_out]",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
        "-t", "10.00",
        str(SEG4)
    ]
    run(cmd_seg4)

    # 5. Concatenate Segments
    print("\n--- 5. Concatenating All 4 Segments into Unified Stream ---")
    concat_list = WORK_DIR / "concat_list.txt"
    concat_list.write_text(f"file '{SEG1}'\nfile '{SEG2}'\nfile '{SEG3}'\nfile '{SEG4}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(CONCAT_VIDEO)
    ]
    run(cmd_concat)

    # 6. Generate Header and Subtitle Overlay Cards
    print("\n--- 6. Creating UI Overlays (Header Badge & Subtitle Cards) ---")
    header_badge = WORK_DIR / "overlay_header_badge.png"
    create_header_badge("रामायण • भाग 2", header_badge)

    sub_card1 = WORK_DIR / "overlay_sub1.png"
    create_subtitle_card([
        "पिनाक धनुष के टूटते ही कांप उठी मिथिला...",
        "जब हाथ में काल-समान फरसा लिए प्रगट हुए भगवान परशुराम!"
    ], sub_card1)

    sub_card2 = WORK_DIR / "overlay_sub2.png"
    create_subtitle_card([
        "किसने तोड़ा मेरे गुरु महादेव का यह पावन पिनाक?",
        "सामने आ, वर्ना आज पूरी मिथिला को भस्म कर दूँगा!"
    ], sub_card2, is_dialogue=True, speaker="भगवान परशुराम")

    sub_card3 = WORK_DIR / "overlay_sub3.png"
    create_subtitle_card([
        "हे मुनिवर! बचपन में हमने कई धनुहियां तोड़ीं...",
        "तब कभी ऐसा क्रोध नहीं किया!",
        "इस पुराने धनुष पर इतनी ममता क्यों?"
    ], sub_card3, is_dialogue=True, speaker="लक्ष्मण")

    sub_card4 = WORK_DIR / "overlay_sub4.png"
    create_subtitle_card([
        "और तब आगे बढ़े प्रभु श्री राम...",
        "मर्यादा और सौम्यता का वह पावन संवाद",
        "जिसने परशुराम के क्रोध को शांत किया! भाग 3 के लिए फॉलो करें!"
    ], sub_card4)

    # 7. Burn Overlays into Final Master
    print("\n--- 7. Burning UI Overlays & Rendering Final Master ---")
    cmd_burn = [
        "ffmpeg", "-y",
        "-i", str(CONCAT_VIDEO),
        "-i", str(header_badge),
        "-i", str(sub_card1),
        "-i", str(sub_card2),
        "-i", str(sub_card3),
        "-i", str(sub_card4),
        "-filter_complex",
        "[0:v][1:v]overlay=0:0[v1];"
        "[v1][2:v]overlay=0:0:enable='between(t,0,10.52)'[v2];"
        "[v2][3:v]overlay=0:0:enable='between(t,10.52,18.56)'[v3];"
        "[v3][4:v]overlay=0:0:enable='between(t,18.56,26.60)'[v4];"
        "[v4][5:v]overlay=0:0:enable='between(t,26.60,36.60)'[v_final]",
        "-map", "[v_final]",
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(FINAL_STORAGE_OUTPUT)
    ]
    run(cmd_burn)

    # Copy to user's Downloads folder
    shutil.copy2(FINAL_STORAGE_OUTPUT, FINAL_DOWNLOADS_OUTPUT)
    print(f"\n✨ SUCCESS! Broadcast Master delivered to:")
    print(f"👉 {FINAL_DOWNLOADS_OUTPUT} ({FINAL_DOWNLOADS_OUTPUT.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
