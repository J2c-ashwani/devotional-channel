#!/usr/bin/env python3
"""
Assemble the Final Broadcast Master for Mahabharata Episode 2 (For User Review):
- Source: 100% Pure Google Vertex Text-to-Video (gemini-omni-1.2-flash, native 1080x1920)
- Native 1.00x speed & native Vertex multi-character talking heads + Kathavachak voiceover
- Dynamic ffprobe-exact timing for Hindi subtitle cards & gold header badge ('महाभारत • भाग 2')
- Outputs:
    /Users/ashwanikumar/Downloads/Itihasa_Saga_Mahabharata_Ep02_Hindi_REVIEW.mp4
    storage/rendered/mahabharata_ep02/Itihasa_Saga_Mahabharata_Ep02_Hindi_REVIEW.mp4
"""

import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
SCENES_DIR = BASE_DIR / "storage" / "rendered" / "mahabharata_ep02"
WORK_DIR = SCENES_DIR / "work_master"
WORK_DIR.mkdir(parents=True, exist_ok=True)

SCENE_IDS = [
    "scene_01_ganga_returns_devavrata",
    "scene_02_nishadaraj_condition",
    "scene_03_devavrata_renounces_throne",
    "scene_04_nishadaraj_final_doubt",
    "scene_05_bhishma_pratigya_oath",
    "scene_06_bhishma_epilogue_eklavya_hook",
]

FINAL_STORAGE = SCENES_DIR / "Itihasa_Saga_Mahabharata_Ep02_Hindi_REVIEW.mp4"
FINAL_DOWNLOADS = Path("/Users/ashwanikumar/Downloads/Itihasa_Saga_Mahabharata_Ep02_Hindi_REVIEW.mp4")


def run(cmd: list):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{' '.join(cmd)}\nSTDERR:\n{res.stderr}")
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
    lines, cur = [], ""
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
    text = "महाभारत • भाग 2"
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 44)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 46, 16
    badge_w, badge_h = text_w + pad_x * 2, text_h + pad_y * 2
    badge_x, badge_y = (1080 - badge_w) // 2, 130
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=26, fill=(12, 10, 8, 220), outline=(218, 165, 32, 245), width=3,
    )
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), text, font=font, fill=(255, 255, 255, 255))
    img.save(output_path)


def create_subtitle_card(text: str, output_path: Path, speaker: str = None):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 35)
    font_speaker = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 31)

    lines = wrap_hindi_lines(draw, text, font_main, max_width=900)
    line_heights = [draw.textbbox((0, 0), l, font=font_main)[3] - draw.textbbox((0, 0), l, font=font_main)[1] for l in lines]
    total_text_h = sum(line_heights) + max(0, len(lines) - 1) * 14 + (44 if speaker else 0)

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
        radius=20, fill=(8, 8, 8, 220),
        outline=(218, 165, 32, 235) if speaker else (255, 255, 255, 145), width=2,
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
    print("🎬 Assembling Final 1080p Broadcast Master for Mahabharata Episode 2...")
    norm_segments, durations = [], []

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
            "ffmpeg", "-y", "-i", str(src),
            "-filter_complex",
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p[v_out];"
            f"[0:a]loudnorm=I=-14:LRA=7:TP=-1.5,afade=t=in:st=0:d=0.05,afade=t=out:st={fade_out_start:.2f}:d=0.06[a_out]",
            "-map", "[v_out]", "-map", "[a_out]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "16",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            str(norm_out)
        ])
        norm_segments.append(norm_out)

    concat_txt = WORK_DIR / "concat.txt"
    concat_txt.write_text("\n".join(f"file '{p.resolve()}'" for p in norm_segments) + "\n")
    concat_raw = WORK_DIR / "concat_raw.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(concat_raw)])

    starts, t = [], 0.0
    for d in durations:
        starts.append((t, t + d))
        t += d

    badge_png = WORK_DIR / "header_badge.png"
    create_header_badge(badge_png)

    (s1_0, s1_1), (s2_0, s2_1), (s3_0, s3_1), (s4_0, s4_1), (s5_0, s5_1), (s6_0, s6_1) = starts
    subtitle_specs = [
        (s1_0 + 0.3, s1_1 - 0.3, "वर्षों बाद देवी गंगा ने शांतनु को महावीर पुत्र देवव्रत लौटाया। पर आगे सत्यवती के विवाह हेतु राजा शांतनु व्याकुल हो उठे!", None),
        (s2_0 + 0.3, s2_1 - 0.3, "'राजकुमार देवव्रत! आपकी संतान के रहते मेरी पुत्री सत्यवती का पुत्र कभी हस्तिनापुर का सम्राट नहीं बन पाएगा!'", "निषादराज"),
        (s3_0 + 0.3, s3_1 - 0.3, "'सुनिए निषादराज! आज ही मैं हस्तिनापुर के राजसिंहासन का त्याग करता हूँ—सत्यवती का पुत्र ही सम्राट होगा!'", "राजकुमार देवव्रत"),
        (s4_0 + 0.3, s4_1 - 0.3, "'राजकुमार! आप तो वचन के पक्के हैं... पर कल को आपकी संतानों ने राज्य मांग लिया, तब क्या होगा?'", "निषादराज"),
        (s5_0 + 0.3, s5_0 + 9.5, "'तो सुनिए जगत के साक्षी! मैं आज से आजीवन अखंड ब्रह्मचर्य का पालन करूँगा—मैं कभी विवाह नहीं करूँगा!'", "राजकुमार देवव्रत (भीष्म प्रतिज्ञा)"),
        (s5_0 + 9.7, s5_1 - 0.2, "आकाश से देवताओं ने पुष्प वर्षा की और तीनों लोकों में गूंज उठा—'भीष्म! भीष्म!'", None),
        (s6_0 + 0.3, s6_0 + 7.5, "उस दिन से देवव्रत संसार में 'भीष्म' कहलाए, जिन्होंने पिता के सुख हेतु सर्वस्व त्याग दिया!", None),
        (s6_0 + 7.6, s6_1 - 0.2, "आगे गुरु द्रोण के किस शिष्य ने गुरु-दक्षिणा में अनूठा बलिदान दिया? जानिए भाग 3 में!", "अगला भाग • एकलव्य"),
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

    print("\n--- Burning Gold Header Badge & Subtitles onto Mahabharata Ep 2 Master ---")
    run([
        "ffmpeg", "-y", *input_args,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[v_final]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart",
        str(FINAL_STORAGE)
    ])

    shutil.copy2(FINAL_STORAGE, FINAL_DOWNLOADS)
    final_dur = probe_duration(FINAL_DOWNLOADS)
    print(f"\n🎉 FINAL MAHABHARATA EP 02 REVIEW MASTER READY:")
    print(f"   Path: {FINAL_DOWNLOADS}")
    print(f"   Duration: {final_dur:.2f}s | Size: {FINAL_DOWNLOADS.stat().st_size / (1024*1024):.2f} MB")


if __name__ == "__main__":
    main()
