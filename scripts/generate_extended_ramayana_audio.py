#!/usr/bin/env python3
"""
Generate complete, crystal-clear Google Charon narration and dialogue stems
for the Extended Ramayana Episode 2 (60-65s Master Cut):
- Track 1: Opening Hook & Context (Parashurama's wrath)
- Track 2: Bridge to Lakshmana & Reaction
- Track 3: Shri Rama's introduction & peaceful dialogue ("नाथ संभुधनु भंजनिहारा...")
- Track 4: Parashurama's realization that Rama is Bhagwan Vishnu & bow of surrender
- Track 5: Outro & Part 3 Hook with Shankh
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

AUDIO_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/audio/ramayana_ep02/extended")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

STEMS = [
    {
        "id": "ext_01_hook_parashurama",
        "text": "मिथिला में शिवजी का पिनाक धनुष टूटते ही तीनों लोक कांप उठे! तभी हाथ में काल-समान फरसा लिए, क्रोधाग्नि में जलते हुए स्वयं भगवान परशुराम राजसभा में प्रगट हुए!"
    },
    {
        "id": "ext_02_lakshmana_bridge",
        "text": "पूरी सभा भयभीत थी, किंतु निर्भीक लक्ष्मण मुस्कुराते हुए आगे आए और व्यंग्य किया! लक्ष्मण की बात सुनते ही परशुराम ने उन पर फरसा तान लिया!"
    },
    {
        "id": "ext_03_rama_entry_and_dialogue",
        "text": "लक्ष्मण की रक्षा करने और मुनि के क्रोध को शांत करने के लिए आगे बढ़े स्वयं मर्यादा पुरुषोत्तम प्रभु श्री राम! उन्होंने दोनों हाथ जोड़कर अत्यंत विनम्रता से कहा—'हे नाथ! शिवजी के धनुष को तोड़ने वाला आपका ही कोई दास होगा!' "
    },
    {
        "id": "ext_04_divine_revelation",
        "text": "श्री राम की असीम विनम्रता और मुख पर दिव्य तेज देखकर परशुराम समझ गए कि उनके सामने साक्षात भगवान विष्णु खड़े हैं! उनका सारा क्रोध पिघल गया और वे प्रभु के चरणों में नतमस्तक हो गए!"
    },
    {
        "id": "ext_05_outro",
        "text": "इस प्रकार प्रभु श्री राम ने अपनी मर्यादा और सौम्यता से महाप्रलय को टाल दिया! देखिए अगला भाग 3: श्री राम और सीता जी का दिव्य विवाह! इतिहास सागा को अभी फॉलो करें!"
    }
]

def main():
    for item in STEMS:
        stem_id = item["id"]
        raw_pcm = AUDIO_DIR / f"{stem_id}_raw.pcm"
        wav_path = AUDIO_DIR / f"{stem_id}.wav"
        
        print(f"🎙️ Generating Charon Voiceover for {stem_id}...")
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
        
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "s16le", "-ar", "24000", "-ac", "1",
            "-i", str(raw_pcm),
            "-ar", "48000", "-ac", "2",
            str(wav_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(wav_path)
        ], capture_output=True, text=True, check=True)
        dur = float(probe.stdout.strip())
        print(f"✅ Generated {wav_path.name}: {dur:.2f}s")

if __name__ == "__main__":
    main()
