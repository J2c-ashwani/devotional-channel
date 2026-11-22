#!/usr/bin/env python3
"""
Generate Pure Text-to-Video Scenes for Mahabharata Episode 1 using Gemini Omni 1.2 Flash:
- Shot 1: Goddess Ganga on the sacred river banks with divine aura
- Shot 2: King Shantanu speaking in Hindi with tearful anguish (Already generated!)
- Shot 3: Goddess Ganga speaking in Hindi (Divine revelation & farewell)
- Shot 4: Celestial departure in the river mist, promising the return of Devavrata
"""

import os
import time
import base64
from pathlib import Path
from google import genai
from google.genai._gaos.types import interactions

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/ashwanikumar/Downloads/devotional/service-account.json'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'devotional-youtube-514907'

client = genai.Client(
    vertexai=True,
    project='devotional-youtube-514907',
    location='global'
)

OUTPUT_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/rendered/mahabharata_ep01")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

resp_fmt = interactions.VideoResponseFormat(
    type='video',
    aspect_ratio='9:16',
    duration='8s',
    resolution='720p',
    delivery='inline'
)

JOBS = [
    {
        "name": "shot1_ganga_river_banks",
        "prompt": (
            "Cinematic 9:16 vertical shot on the mystical ancient banks of the sacred river Ganga at twilight. "
            "A celestial, ethereal woman in flowing radiant white garments, Goddess Ganga, stands in the sacred misty waters. "
            "Ancient Indian sacred forest along the shore, golden moonlight reflecting on water ripples, photorealistic 8k, mystical epic ambiance."
        ),
        "out": OUTPUT_DIR / "shot1_ganga_river_banks.mp4"
    },
    {
        "name": "shot3_ganga_speaking_hindi",
        "prompt": (
            "Cinematic 9:16 vertical close-up shot of Goddess Ganga on the misty river Ganga. "
            "A radiant celestial goddess with a subtle golden crown and glowing white garments, cradling a divine baby prince. "
            "She speaks directly in Hindi with majestic calm and authority: 'हे राजन्! तुमने अपना वचन तोड़ दिया! अब मैं तुम्हारे साथ नहीं रह सकती, पर यह बालक जीवित रहेगा!' "
            "Photorealistic 8k, realistic mouth speaking Hindi dialogue, divine celestial aura, cinematic lighting."
        ),
        "out": OUTPUT_DIR / "shot3_ganga_speaking_hindi.mp4"
    },
    {
        "name": "shot4_ganga_departure",
        "prompt": (
            "Cinematic 9:16 vertical shot of Goddess Ganga walking gracefully into the divine swirling mist of the sacred river Ganga with the infant prince. "
            "Golden celestial light rays piercing through river mist, divine atmospheric aura, epic cinematic farewell, photorealistic 8k."
        ),
        "out": OUTPUT_DIR / "shot4_ganga_departure.mp4"
    }
]

def main():
    for job in JOBS:
        out_file = job["out"]
        if out_file.exists() and out_file.stat().st_size > 100000:
            print(f"Skipping {job['name']} (already generated: {out_file.stat().st_size} bytes)")
            continue

        print(f"\n🎬 Generating Omni 1.2 Flash Pure Video: {job['name']}...")
        try:
            interaction = client.interactions.create(
                model='gemini-omni-1.2-flash',
                input=job["prompt"],
                response_format=resp_fmt
            )
            print(f"[{job['name']}] Status: {interaction.status}")
            if interaction.output_video and interaction.output_video.data:
                data = interaction.output_video.data
                raw_bytes = base64.b64decode(data) if isinstance(data, str) else data
                with open(out_file, 'wb') as f:
                    f.write(raw_bytes)
                print(f"[{job['name']}] ✅ Saved: {out_file} ({len(raw_bytes)} bytes)!")
        except Exception as e:
            print(f"[{job['name']}] ❌ Error:", e)

if __name__ == "__main__":
    main()
