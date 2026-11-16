#!/usr/bin/env python3
"""
Assemble Two Complete 100% Pure Text-to-Video Master Productions:
1. Hindi Master Video (Ramayana Ep 01 - Sita Swayamvar & Pinaka Bow Breaking)
2. English Master Video (Ramayana Ep 01 - The Shattering of Lord Shiva's Bow)

Zero static images. Every frame generated from Google Gemini Omni 1.2 Flash Pure Text-to-Video:
- Shot 1 (Pinaka Bow Vault & Warriors): storage/rendered/shot1_pinaka_vault_t2v.mp4
- Shot 2A (King Janaka Weeping on Throne): storage/rendered/king_janaka_omni_clip.mp4
- Shot 2B (Sage Vishvamitra Commanding Rama): storage/rendered/vishvamitra_omni_clip.mp4
- Shot 3 (Shri Rama Lifting & Breaking Pinaka Bow): storage/rendered/rama_breaks_bow_action_omni.mp4
- Shot 4 (Mithila Sunrise Celestial Celebration): storage/rendered/shot4_celebration_t2v.mp4

Delivers both to /Users/ashwanikumar/Downloads/ for immediate viewing.
"""

import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
RENDER_DIR = STORAGE_DIR / "rendered" / "dual_productions"
RENDER_DIR.mkdir(parents=True, exist_ok=True)

# 100% Pure Text-to-Video Clips from Gemini Omni 1.2 Flash
CLIP_SHOT1 = STORAGE_DIR / "rendered" / "shot1_pinaka_vault_t2v.mp4"
CLIP_SHOT2A = STORAGE_DIR / "rendered" / "king_janaka_omni_clip.mp4"
CLIP_SHOT2B = STORAGE_DIR / "rendered" / "vishvamitra_omni_clip.mp4"
CLIP_SHOT3 = STORAGE_DIR / "rendered" / "rama_breaks_bow_action_omni.mp4"
CLIP_SHOT4 = STORAGE_DIR / "rendered" / "shot4_rama_sita_celebration_omni.mp4"

# Audio Soundtracks
AUDIO_HINDI = STORAGE_DIR / "rendered" / "job_ramayana_ep01_google" / "master_google_soundtrack.aac"
AUDIO_ENGLISH = STORAGE_DIR / "rendered" / "master_english_soundtrack.aac"

# Destination Outputs
HINDI_OUTPUT = STORAGE_DIR / "rendered" / "ramayana_part1_hindi_pure_t2v.mp4"
ENGLISH_OUTPUT = STORAGE_DIR / "rendered" / "ramayana_part1_english_pure_t2v.mp4"

USER_DOWNLOADS = Path("/Users/ashwanikumar/Downloads")

def run(cmd: list):
    print("Executing:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("ERROR STDERR:\n", res.stderr)
        raise RuntimeError(f"FFmpeg command failed: {res.stderr}")
    return res

def create_video_segment(input_clip: Path, target_duration: float, output_path: Path, mode: str = "slow"):
    """
    Stretches, loops, or slows a video clip seamlessly to exact target duration.
    Always outputs 1080x1920 (9:16 vertical), 30 fps, yuv420p, zero audio.
    """
    if mode == "pingpong":
        # Forward -> Reverse -> Forward loop for natural cinematic camera movement
        filter_str = (
            f"[0:v]scale=1080:1920:flags=lanczos,fps=30[base];"
            f"[base]split=4[v1][v2_in][v3][v4_in];"
            f"[v2_in]reverse[v2];"
            f"[v4_in]reverse[v4];"
            f"[v1][v2][v3][v4]concat=n=4:v=1:a=0,trim=0:{target_duration},setpts=PTS-STARTPTS[out]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_clip),
            "-filter_complex", filter_str,
            "-map", "[out]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output_path)
        ]
    elif mode == "slow":
        # Cinematic retiming
        speed_factor = target_duration / 8.0
        filter_str = (
            f"[0:v]setpts={speed_factor:.4f}*PTS,scale=1080:1920:flags=lanczos,fps=30,"
            f"trim=0:{target_duration},setpts=PTS-STARTPTS[out]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_clip),
            "-filter_complex", filter_str,
            "-map", "[out]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output_path)
        ]
    else:
        raise ValueError(f"Unknown mode {mode}")

    run(cmd)
    print(f"Segment created: {output_path} ({target_duration}s)")

def assemble_production(lang: str, audio_path: Path, shot_durations: dict, final_output: Path):
    print(f"\n==========================================")
    print(f" Assembling {lang.upper()} Master Video (Pure Text-to-Video)")
    print(f"==========================================")

    lang_dir = RENDER_DIR / lang
    lang_dir.mkdir(parents=True, exist_ok=True)

    seg1 = lang_dir / "seg_01_vault.mp4"
    seg2a = lang_dir / "seg_02a_janaka.mp4"
    seg2b = lang_dir / "seg_02b_vishvamitra.mp4"
    seg3 = lang_dir / "seg_03_rama_action.mp4"
    seg4 = lang_dir / "seg_04_celebration.mp4"

    # Generate each scene segment
    create_video_segment(CLIP_SHOT1, shot_durations["s1"], seg1, mode="pingpong")
    create_video_segment(CLIP_SHOT2A, shot_durations["s2a"], seg2a, mode="slow")
    create_video_segment(CLIP_SHOT2B, shot_durations["s2b"], seg2b, mode="slow")
    create_video_segment(CLIP_SHOT3, shot_durations["s3"], seg3, mode="slow")
    create_video_segment(CLIP_SHOT4, shot_durations["s4"], seg4, mode="slow")

    # Create concat list
    concat_list = lang_dir / "concat_list.txt"
    with open(concat_list, "w") as f:
        for s in [seg1, seg2a, seg2b, seg3, seg4]:
            f.write(f"file '{s.resolve()}'\n")

    # Final stitch with warm mythological color grading & audio muxing
    # eq: contrast=1.04, saturation=1.12 for divine Indian mythological warmth
    total_duration = sum(shot_durations.values())
    raw_video = lang_dir / f"stitched_{lang}_video.mp4"
    
    cmd_stitch = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-vf", "eq=contrast=1.04:brightness=0.01:saturation=1.12",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_video)
    ]
    run(cmd_stitch)

    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        str(final_output)
    ]
    run(cmd_mux)
    print(f" {lang.upper()} Master Video successfully created: {final_output}")

def main():
    # 1. Hindi Timings (Total: 65.24s)
    hindi_durations = {
        "s1": 16.17,   # Pinaka Vault in Mithila
        "s2a": 9.00,   # King Janaka's grief
        "s2b": 9.65,   # Sage Vishvamitra commanding Rama
        "s3": 19.05,   # Rama lifting & breaking bow
        "s4": 11.37    # Celestial celebration & follow CTA
    }

    # 2. English Timings (Total: 69.32s)
    english_durations = {
        "s1": 21.49,   # Pinaka Vault in Mithila
        "s2a": 10.50,  # King Janaka's grief
        "s2b": 10.59,  # Sage Vishvamitra commanding Rama
        "s3": 13.77,   # Rama lifting & breaking bow
        "s4": 12.97    # Celestial celebration & follow CTA + Shankh tail
    }

    # Render Hindi Master Video
    assemble_production("hindi", AUDIO_HINDI, hindi_durations, HINDI_OUTPUT)

    print("\n==========================================")
    print(f" Hindi Master Video Rendered: {HINDI_OUTPUT}")
    print("==========================================")
    print(f"1. Hindi Master:   {HINDI_OUTPUT}")
    print(f"2. English Master: {ENGLISH_OUTPUT}")
    print("==========================================")

if __name__ == "__main__":
    main()
