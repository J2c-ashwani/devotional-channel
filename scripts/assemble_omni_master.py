#!/usr/bin/env python3
"""
Assemble the 5-Shot Master Video for Ramayana Episode 1 using GEMINI OMNI 1.2 FLASH:
- Shot 1 (0 to 16.17s): Mithila Court & 8-wheeled Pinaka vault (Ultra-realistic keyframe + 2.5D camera pan)
- Shot 2A (16.17s to 25.17s = 9.0s): King Janaka's grief & question (Gemini Omni 1.2 Flash Live Video)
- Shot 2B (25.17s to 34.82s = 9.65s): Sage Vishvamitra commanding Prince Rama (Gemini Omni 1.2 Flash Live Video)
- Shot 3 (34.82s to 53.87s = 19.05s): Shri Rama breaking Pinaka bow with cosmic lightning (Climax Keyframe)
- Shot 4 (53.87s to 65.24s = 11.37s): Celestial aftermath, flowers shower, shankh conch, Follow for Part 2!
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
OUTPUT_DIR = STORAGE_DIR / "rendered" / "job_ramayana_ep01_omni"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Image paths
IMG_SHOT1 = Path("/Users/ashwanikumar/.gemini/antigravity/brain/a656ac81-e178-40b9-8293-9783dd71323a/mithila_pinaka_court_1794775884188.jpg")
IMG_SHOT3 = Path("/Users/ashwanikumar/.gemini/antigravity/brain/a656ac81-e178-40b9-8293-9783dd71323a/scene_3_rama_breaks_pinaka_bow_1794776003893.jpg")
IMG_SHOT4 = Path("/Users/ashwanikumar/.gemini/antigravity/brain/a656ac81-e178-40b9-8293-9783dd71323a/vishvamitra_orders_rama_mithila_1794775952411.jpg")

# Video paths from Gemini Omni 1.2 Flash
VIDEO_SHOT2A = STORAGE_DIR / "rendered" / "king_janaka_omni_clip.mp4"
VIDEO_SHOT2B = STORAGE_DIR / "rendered" / "vishvamitra_omni_clip.mp4"

# Master audio
AUDIO_PATH = STORAGE_DIR / "rendered" / "job_ramayana_ep01_google" / "master_google_soundtrack.aac"

# Shot clips output
CLIP1 = OUTPUT_DIR / "shot_01.mp4"
CLIP2A = OUTPUT_DIR / "shot_02a.mp4"
CLIP2B = OUTPUT_DIR / "shot_02b.mp4"
CLIP3 = OUTPUT_DIR / "shot_03.mp4"
CLIP4 = OUTPUT_DIR / "shot_04.mp4"

FINAL_VIDEO = OUTPUT_DIR / "ramayana_part1_omni_flash_master.mp4"

def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR:", res.stderr)
        raise RuntimeError(f"Command failed: {res.stderr}")
    return res

def main():
    print("=== Rendering 5-Shot Gemini Omni 1.2 Flash Master Video ===")
    
    # 1. Shot 1: Mithila court & Pinaka bow (16.17s)
    cmd_shot1 = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(IMG_SHOT1),
        "-t", "16.17",
        "-filter_complex",
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0004,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=485:s=1080x1920:fps=30,"
        "format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP1)
    ]
    run_cmd(cmd_shot1)

    # 2. Shot 2A: King Janaka Omni 1.2 Flash live video (9.0s)
    # Omni clip is 8.04s -> setpts=9.0/8.042 = 1.119
    cmd_shot2a = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT2A),
        "-filter_complex",
        "setpts=1.119*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "9.0",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP2A)
    ]
    run_cmd(cmd_shot2a)

    # 3. Shot 2B: Sage Vishvamitra & Rama Omni 1.2 Flash live video (9.65s)
    # Omni clip is 8.04s -> setpts=9.65/8.042 = 1.200
    cmd_shot2b = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT2B),
        "-filter_complex",
        "setpts=1.200*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "9.65",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP2B)
    ]
    run_cmd(cmd_shot2b)

    # 4. Shot 3: Shri Rama Breaking Pinaka Bow (19.05s)
    cmd_shot3 = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(IMG_SHOT3),
        "-t", "19.05",
        "-filter_complex",
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0003,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=572:s=1080x1920:fps=30,"
        "format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP3)
    ]
    run_cmd(cmd_shot3)

    # 5. Shot 4: Celestial aftermath, shankh conch & Follow CTA (11.37s)
    cmd_shot4 = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(IMG_SHOT4),
        "-t", "11.37",
        "-filter_complex",
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='max(1.10-0.0004*on,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=341:s=1080x1920:fps=30,"
        "format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP4)
    ]
    run_cmd(cmd_shot4)

    # 6. Concat visual shots
    concat_list = OUTPUT_DIR / "shots_concat.txt"
    with open(concat_list, "w") as f:
        for clip in [CLIP1, CLIP2A, CLIP2B, CLIP3, CLIP4]:
            f.write(f"file '{clip.resolve()}'\n")

    raw_video = OUTPUT_DIR / "raw_concat_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(raw_video)
    ]
    run_cmd(cmd_concat)

    # 7. Mux master soundtrack
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(AUDIO_PATH),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        str(FINAL_VIDEO)
    ]
    run_cmd(cmd_final)

    print(f"\n Master Gemini Omni 1.2 Flash Video rendered successfully at:")
    print(FINAL_VIDEO)

if __name__ == "__main__":
    main()
