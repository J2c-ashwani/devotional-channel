#!/usr/bin/env python3
"""
Assemble the 100% PURE MOTION MASTER VIDEO for Ramayana Episode 1:
- Every single scene is a fluid, high-motion AI-generated video (Google Veo 3.1 Image-to-Video)
- ZERO static photo slides
- ZERO lip-sync or facial distortion issues
- 100% Character consistency (Shri Rama, King Janaka, Sage Vishvamitra, and Mithila palace)
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
OUTPUT_DIR = STORAGE_DIR / "rendered" / "job_ramayana_ep01_full_motion"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 5 Pure Video Clips generated from Google Veo 3.1 I2V
VIDEO_SHOT1 = STORAGE_DIR / "rendered" / "shot1_i2v_pinaka.mp4"
VIDEO_SHOT2A = STORAGE_DIR / "rendered" / "shot2a_i2v_janaka.mp4"
VIDEO_SHOT2B = STORAGE_DIR / "rendered" / "shot2b_i2v_vishvamitra.mp4"
VIDEO_SHOT3 = STORAGE_DIR / "rendered" / "shot3_i2v_rama_bow.mp4"
VIDEO_SHOT4 = STORAGE_DIR / "rendered" / "shot4_i2v_celebration.mp4"

AUDIO_PATH = STORAGE_DIR / "rendered" / "job_ramayana_ep01_google" / "master_google_soundtrack.aac"

CLIP1 = OUTPUT_DIR / "motion_shot_01.mp4"
CLIP2A = OUTPUT_DIR / "motion_shot_02a.mp4"
CLIP2B = OUTPUT_DIR / "motion_shot_02b.mp4"
CLIP3 = OUTPUT_DIR / "motion_shot_03.mp4"
CLIP4 = OUTPUT_DIR / "motion_shot_04.mp4"

FINAL_VIDEO = OUTPUT_DIR / "ramayana_part1_100pct_full_motion_master.mp4"

def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR:", res.stderr)
        raise RuntimeError(f"Command failed: {res.stderr}")
    return res

def main():
    print("=== Rendering 100% Pure Motion Master Video ===")
    
    # 1. Shot 1: 8-wheeled Pinaka vault video (16.17s)
    # Slow cinematic motion: scale to 1080x1920, 30fps
    cmd_shot1 = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT1),
        "-filter_complex",
        "setpts=2.688*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "16.17",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP1)
    ]
    run_cmd(cmd_shot1)

    # 2. Shot 2A: King Janaka video (9.0s)
    cmd_shot2a = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT2A),
        "-filter_complex",
        "setpts=1.496*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "9.0",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP2A)
    ]
    run_cmd(cmd_shot2a)

    # 3. Shot 2B: Sage Vishvamitra & Shri Rama video (9.65s)
    cmd_shot2b = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT2B),
        "-filter_complex",
        "setpts=1.604*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "9.65",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP2B)
    ]
    run_cmd(cmd_shot2b)

    # 4. Shot 3: Shri Rama Breaking Pinaka Bow video (19.05s)
    # Slow-motion divine cosmic lightning explosion
    cmd_shot3 = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT3),
        "-filter_complex",
        "setpts=3.166*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "19.05",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP3)
    ]
    run_cmd(cmd_shot3)

    # 5. Shot 4: Celestial sunrise flower shower celebration video (11.37s)
    cmd_shot4 = [
        "ffmpeg", "-y", "-i", str(VIDEO_SHOT4),
        "-filter_complex",
        "setpts=1.890*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-t", "11.37",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(CLIP4)
    ]
    run_cmd(cmd_shot4)

    # 6. Concat all 5 motion video clips
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

    # 7. Mux master soundtrack (Google Charon 1.0x Kathavachak + divine sitar/flute + thunder & shankh SFX)
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

    print(f"\n Master 100% Full Motion Video rendered successfully at:")
    print(FINAL_VIDEO)

if __name__ == "__main__":
    main()
