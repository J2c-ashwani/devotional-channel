#!/usr/bin/env python3
"""
Assemble the Final Broadcast Master for Ramayana Episode 3:
- Source: 100% Pure Google Vertex Text-to-Video (gemini-omni-1.2-flash, native 1080x1920)
- Native 1.00x speed & native Vertex multi-character voices + lip-sync (NO atempo/setpts stretching)
- Dynamic ffprobe-exact timing for clean Hindi subtitle cards & gold header badge ('रामायण • भाग 3')
- Audio broadcast mastering (EBU R128 loudnorm I=-14 LUFS + click-free transitions)
- Outputs:
    /Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep03_Hindi_REVIEW.mp4
    storage/rendered/ramayana_ep03/Itihasa_Saga_Ramayana_Ep03_Hindi_REVIEW.mp4
"""

import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
SCENES_DIR = BASE_DIR / "storage" / "rendered" / "ramayana_ep03" / "v2_clean"
WORK_DIR = SCENES_DIR / "work_master"
WORK_DIR.mkdir(parents=True, exist_ok=True)

SCENE_IDS = [
    "scene_01_baraat_arrival",
    "scene_02_janaka_welcome",
    "scene_03_vishvamitra_varmala",
    "scene_04_rama_sita_vows",
    "scene_05_janaka_bidai",
    "scene_06_ayodhya_diwali_hook",
]

FINAL_STORAGE = BASE_DIR / "storage" / "rendered" / "ramayana_ep03" / "Itihasa_Saga_Ramayana_Ep03_Hindi_REVIEW.mp4"
FINAL_DOWNLOADS = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Ramayana_Ep03_Hindi_REVIEW.mp4")


def run(cmd: list):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg command failed:\n{' '.join(cmd)}\nSTDERR:\n{res.stderr}")
    return res


def probe_duration(path: Path) -> float:
    res = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ])
    return float(res.stdout.strip())


def wrap_hindi_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int = 880) -> list:
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def create_header_badge(output_path: Path):
    text = "रामायण • भाग 3"
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    font = ImageFont.truetype(font_path, 44)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 46, 16
    badge_w, badge_h = text_w + pad_x * 2, text_h + pad_y * 2
    badge_x, badge_y = (1080 - badge_w) // 2, 130

    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=26,
        fill=(12, 10, 8, 220),
        outline=(218, 165, 32, 245),
        width=3,
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), text, font=font, fill=(255, 255, 255, 255))
    img.save(output_path)


def create_subtitle_card(text: str, output_path: Path, speaker: str = None):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    font_main = ImageFont.truetype(font_path, 35)
    font_speaker = ImageFont.truetype(font_path, 31)

    lines = wrap_hindi_lines(draw, text, font_main, max_width=900)
    line_heights = [draw.textbbox((0, 0), l, font=font_main)[3] - draw.textbbox((0, 0), l, font=font_main)[1] for l in lines]
    total_text_h = sum(line_heights) + max(0, len(lines) - 1) * 14
    if speaker:
        total_text_h += 44

    pad_y, pad_x = 18, 36
    badge_h = total_text_h + pad_y * 2
    max_w = max(draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0] for l in lines)
    if speaker:
        s_bbox = draw.textbbox((0, 0), speaker, font=font_speaker)
        max_w = max(max_w, s_bbox[2] - s_bbox[0])

    badge_w = min(1000, max_w + pad_x * 2)
    badge_x = (1080 - badge_w) // 2
    badge_y = 1580 - badge_h // 2

    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=20,
        fill=(8, 8, 8, 220),
        outline=(218, 165, 32, 235) if speaker else (255, 255, 255, 145),
        width=2,
    )

    curr_y = badge_y + pad_y
    if speaker:
        s_w = draw.textbbox((0, 0), speaker, font=font_speaker)[2] - draw.textbbox((0, 0), speaker, font=font_speaker)[0]
        draw.text(((1080 - s_w) // 2, curr_y), speaker, font=font_speaker, fill=(255, 215, 0, 255))
        curr_y += 42

    for l in lines:
        l_w = draw.textbbox((0, 0), l, font=font_main)[2] - draw.textbbox((0, 0), l, font=font_main)[0]
        draw.text(((1080 - l_w) // 2, curr_y), l, font=font_main, fill=(255, 255, 255, 255))
        curr_y += 48

    img.save(output_path)


def main():
    print("🎬 Assembling Final 1080p Broadcast Master for Ramayana Episode 3...")

    norm_segments = []
    durations = []

    for idx, sid in enumerate(SCENE_IDS, 1):
        src = SCENES_DIR / f"{sid}.mp4"
        if not src.exists():
            raise FileNotFoundError(f"Missing scene file: {src}")
        dur = probe_duration(src)
        durations.append(dur)
        norm_out = WORK_DIR / f"norm_{idx:02d}_{sid}.mp4"
        fade_out_start = max(0.2, dur - 0.06)

        print(f"  [{idx}/6] Normalizing {sid} ({dur:.2f}s) at native 1.00x speed...")
        run([
            "ffmpeg", "-y",
            "-i", str(src),
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p[v_out];"
            f"[0:a]loudnorm=I=-14:LRA=7:TP=-1.5,afade=t=in:st=0:d=0.05,afade=t=out:st={fade_out_start:.2f}:d=0.06[a_out]",
            "-map", "[v_out]", "-map", "[a_out]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "16",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(norm_out)
        ])
        norm_segments.append(norm_out)

    # Concatenate normalized clips cleanly
    concat_txt = WORK_DIR / "concat.txt"
    concat_txt.write_text("\n".join(f"file '{p.resolve()}'" for p in norm_segments) + "\n")
    concat_raw = WORK_DIR / "concat_raw.mp4"
    print("\n--- Concatenating all 6 normalized 1080p Vertex scenes ---")
    run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(concat_raw)
    ])

    # Compute exact cumulative scene start/end offsets from ffprobe
    starts = []
    t = 0.0
    for d in durations:
        starts.append((t, t + d))
        t += d

    badge_png = WORK_DIR / "header_badge.png"
    create_header_badge(badge_png)

    # Subtitle beats aligned strictly to each Act's actual Vertex duration
    # Format: (start_sec, end_sec, text, speaker_label)
    (s1_0, s1_1), (s2_0, s2_1), (s3_0, s3_1), (s4_0, s4_1), (s5_0, s5_1), (s6_0, s6_1) = starts
    subtitle_specs = [
        (s1_0 + 0.3, s1_1 - 0.3, "परशुराम जी के जाने के बाद, राजा जनक ने अयोध्या संदेश भेजा—और भव्य बारात लेकर मिथिला पधारे महाराज दशरथ!", None),
        (s2_0 + 0.3, s2_1 - 0.3, "'स्वागत है समधी महाराज दशरथ! आपके पुत्र श्री राम ने आज समस्त मिथिला का हृदय जीत लिया है!'", "राजा जनक (मिथिला नरेश)"),
        (s3_0 + 0.3, s3_0 + 7.6, "'शुभ मुहूर्त आ गया है वत्स राम! धर्म के इस पावन बंधन में सीता का पाणिग्रहण करो!'", "महर्षि विश्वामित्र"),
        (s3_0 + 7.8, s3_1 - 0.2, "पावन वेदी पर दिव्य वरमाला — देवताओं ने पुष्प वर्षा कर श्री राम-सीता विवाह का अभिनंदन किया!", None),
        (s4_0 + 0.3, s4_0 + 7.4, "'हे सीते! अग्नि को साक्षी मान वचन देता हूँ—धर्म पथ पर हम सदैव एक रहेंगे।'", "प्रभु श्री राम"),
        (s4_0 + 7.5, s4_1 - 0.3, "'हे नाथ! सुख हो या वनवास, हर कदम पर मैं आपकी छाया बनकर चलूँगी।'", "माता सीता"),
        (s5_0 + 0.3, s5_0 + 7.4, "'हे राम! मेरी प्राणप्रिय जानकी को आपको सौंपता हूँ... इन्हें सदैव सम्मान देना!'", "राजा जनक"),
        (s5_0 + 7.6, s5_1 - 0.2, "संपूर्ण मिथिला की आँखें नम थीं... और प्रभु श्री राम अयोध्या लौट चले!", None),
        (s6_0 + 0.3, s6_0 + 8.5, "अयोध्या लौटते ही नगरी दीपों से जगमगा उठी! हर ओर केवल आनंद और मंगल था...", None),
        (s6_0 + 8.5, s6_1 - 0.2, "पर किसे पता था—कल राज्याभिषेक से पहले ही एक महाषड्यंत्र रचा जाने वाला है? जानिए भाग 4 में!", "अगला भाग • अयोध्या कांड"),
    ]

    input_args = ["-i", str(concat_raw), "-i", str(badge_png)]
    filter_parts = ["[0:v][1:v]overlay=0:0[v0]"]

    for i, (st, en, txt, spk) in enumerate(subtitle_specs):
        card = WORK_DIR / f"sub_{i:02d}.png"
        create_subtitle_card(txt, card, speaker=spk)
        input_args.extend(["-i", str(card)])
        in_idx = i + 2
        prev_lbl = f"v{i}"
        next_lbl = f"v{i+1}" if i < len(subtitle_specs) - 1 else "v_final"
        filter_parts.append(f"[{prev_lbl}][{in_idx}:v]overlay=0:0:enable='between(t,{st:.2f},{en:.2f})'[{next_lbl}]")

    print("\n--- Burning Gold Header Badge & Subtitles onto Master ---")
    run([
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[v_final]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart",
        str(FINAL_STORAGE)
    ])

    shutil.copy2(FINAL_STORAGE, FINAL_DOWNLOADS)
    final_dur = probe_duration(FINAL_DOWNLOADS)
    print(f"\n🎉 FINAL EPISODE 3 REVIEW MASTER READY:")
    print(f"   Path: {FINAL_DOWNLOADS}")
    print(f"   Duration: {final_dur:.2f}s | Size: {FINAL_DOWNLOADS.stat().st_size / (1024*1024):.2f} MB")


if __name__ == "__main__":
    main()
