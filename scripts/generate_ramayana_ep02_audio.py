#!/usr/bin/env python3
"""
Generate authentic Google Gemini Charon TTS voiceovers for Ramayana Episode 2:
- Scene 1 Hook: "शिवजी के पिनाक धनुष के टूटते ही कांप उठी मिथिला, जब स्वयं भगवान परशुराम हाथ में काल-समान फरसा लिए, क्रोधाग्नि में जलते हुए राजदरबार में प्रगट हुए!"
- Scene 4 Outro: "और तब आगे बढ़े प्रभु श्री राम... मर्यादा और सौम्यता का वह संवाद, जिसने परशुराम के क्रोध को शांत कर दिया! भाग 3 के लिए अभी सब्सक्राइब और फॉलो करें!"
"""

import os
import subprocess
from pathlib import Path
from google import genai
from google.genai import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ashwanikumar/Downloads/devotional/service-account.json'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'devotional-youtube-514907'

client = genai.Client(
    vertexai=True,
    project='devotional-youtube-514907',
    location='global'
)

AUDIO_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/audio/ramayana_ep02")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = [
    {
        "id": "scene_01_hook_charon",
        "text": "शिवजी के पिनाक धनुष के टूटते ही कांप उठी मिथिला, जब स्वयं भगवान परशुराम हाथ में काल-समान फरसा लिए, क्रोधाग्नि में जलते हुए राजदरबार में प्रगट हुए!"
    },
    {
        "id": "scene_04_outro_charon",
        "text": "और तब आगे बढ़े प्रभु श्री राम... मर्यादा और सौम्यता का वह संवाद, जिसने परशुराम के क्रोध को शांत कर दिया! भाग 3 के लिए अभी सब्सक्राइब और फॉलो करें!"
    }
]

def main():
    for item in ITEMS:
        stem_id = item["id"]
        raw_pcm = AUDIO_DIR / f"{stem_id}_raw.pcm"
        wav_path = AUDIO_DIR / f"{stem_id}.wav"
        
        print(f"🎙️ Generating Google Charon Voiceover for {stem_id}...")
        res = client.models.generate_content(
            model='gemini-2.5-flash-preview-tts',
            contents=item["text"],
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
        
        # Convert PCM to 44.1kHz stereo WAV
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "s16le", "-ar", "24000", "-ac", "1",
            "-i", str(raw_pcm),
            "-ar", "44100", "-ac", "2",
            str(wav_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Probe exact duration
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(wav_path)
        ], capture_output=True, text=True, check=True)
        dur = float(probe.stdout.strip())
        print(f"✅ Generated {wav_path.name}: {dur:.2f}s ({wav_path.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
