#!/usr/bin/env python3
"""
Generate the English Master Soundtrack using Google Charon TTS:
- 4 Scene stems generated with Google Charon English neural voice
- Converted from raw PCM to 24kHz WAV
- Mixed with sacred ambient sitar/tanpura music, thunder climax SFX, and shankh conch finale
- Mastered to broadcast standard -14 LUFS
"""

import os
import subprocess
import time
from pathlib import Path
from backend.app.config import settings
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
AUDIO_DIR = STORAGE_DIR / "audio" / "english_narration"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

SFX_DIR = STORAGE_DIR / "audio" / "sfx"
MUSIC_DIR = STORAGE_DIR / "audio" / "music"

client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
    http_options={'api_version': 'v1beta'}
)

SCENES = [
    {
        "id": "scene_01",
        "text": "Imagine! In the grand royal assembly of King Janaka, the pride of the mightiest warriors of the three worlds was crushed to dust! The colossal Pinaka bow of Lord Shiva, sealed inside a massive eight-wheeled iron vault, that five thousand battle-hardened warriors could not even budge!"
    },
    {
        "id": "scene_02",
        "text": "A chilling silence engulfed the court! King Janaka wept in despair: 'Has this earth become devoid of all true warriors?' And right then, the roar of Sage Vishvamitra echoed: 'Rise, Rama! Rise, my child, and string this divine bow!'"
    },
    {
        "id": "scene_03",
        "text": "Prince Rama stepped forward, lifted the celestial bow as effortlessly as a lotus flower, and the moment he pulled the bowstring—with a cataclysmic crack of thunder, the mighty bow snapped in half!"
    },
    {
        "id": "scene_04",
        "text": "The heavens erupted in celebration, showering divine golden flowers upon Mithila! To witness the next glorious chapter of Lord Rama—follow for Part 2!"
    }
]

def generate_voice_stem(scene_id: str, text: str) -> Path:
    raw_pcm = AUDIO_DIR / f"{scene_id}_raw.pcm"
    wav_path = AUDIO_DIR / f"{scene_id}.wav"
    
    if wav_path.exists() and wav_path.stat().st_size > 10000:
        print(f"Skipping {scene_id} (already generated)")
        return wav_path

    print(f"Generating English TTS for {scene_id} with voice 'Charon'...")
    res = client.models.generate_content(
        model='gemini-2.5-flash-preview-tts',
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Charon'
                    )
                )
            )
        )
    )
    raw_bytes = res.parts[0].inline_data.data
    raw_pcm.write_bytes(raw_bytes)

    # Convert PCM to 24kHz WAV
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", str(raw_pcm),
        "-c:a", "pcm_s16le",
        str(wav_path)
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_pcm.unlink(missing_ok=True)
    print(f"Saved {wav_path}!")
    return wav_path

def main():
    wav_files = []
    for sc in SCENES:
        wav = generate_voice_stem(sc["id"], sc["text"])
        wav_files.append(wav)
        time.sleep(22)  # Respect free tier rate limits

    # Concat voiceover
    concat_list = AUDIO_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for w in wav_files:
            f.write(f"file '{w.resolve()}'\n")

    full_voice = AUDIO_DIR / "full_english_voice.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(full_voice)
    ], check=True)

    # Master Soundtrack with BGM & SFX
    master_soundtrack = STORAGE_DIR / "rendered" / "master_english_soundtrack.aac"
    
    bgm = MUSIC_DIR / "bgm_sacred_epic_orchestral.aac"
    thunder = SFX_DIR / "sfx_thunder_rumble.aac"
    shankh = SFX_DIR / "sfx_divine_shankh.aac"

    # Total voice duration is ~67.92s
    # Thunder hits at ~51s (Scene 3 climax)
    # Shankh hits at ~58s (Scene 4 celebration)
    filter_complex = (
        "[0:a]volume=1.0[v];"
        "[1:a]volume=0.22,afade=t=in:ss=0:d=1.5,afade=t=out:st=64:d=3[m];"
        "[2:a]adelay=51000|51000,volume=0.9[sfx1];"
        "[3:a]adelay=58000|58000,volume=0.85[sfx2];"
        "[v][m][sfx1][sfx2]amix=inputs=4:duration=first:dropout_transition=2,"
        "loudnorm=I=-14:LRA=7:TP=-1.5[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(full_voice),
        "-i", str(bgm),
        "-i", str(thunder),
        "-i", str(shankh),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "aac", "-b:a", "256k",
        str(master_soundtrack)
    ]
    subprocess.run(cmd, check=True)
    print(f"\n Master English Soundtrack created: {master_soundtrack}!")

if __name__ == "__main__":
    main()
