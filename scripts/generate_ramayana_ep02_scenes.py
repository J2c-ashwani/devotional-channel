#!/usr/bin/env python3
"""
Generate Pure Text-to-Video Scenes for Ramayana Episode 2 using Gemini Omni 1.2 Flash:
- Shot 1: Bhagwan Parashurama arriving in Mithila court shaking with thunder and carrying glowing Parashu
- Shot 2: Bhagwan Parashurama speaking in Hindi with righteous fury (talking head lip-sync)
- Shot 3: Prince Lakshmana speaking in Hindi with fearless smile and witty courage (talking head lip-sync)
- Shot 4: Maryada Purushottam Shri Rama stepping forward with folded hands in divine serenity and peace
"""

import os
import sys
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

OUTPUT_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/rendered/ramayana_ep02")
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
        "name": "shot1_parashurama_arrival",
        "prompt": (
            "Cinematic 9:16 vertical shot in the grand ancient royal durbar of King Janaka in Mithila. "
            "Seismic tremors shake the marble pillars as stormy thunderclouds gather outside. "
            "The mighty warrior-sage Bhagwan Parashurama enters, a towering sage with fierce glowing eyes, "
            "ascetic matted hair, wearing saffron bark garments and rudraksha beads, with a glowing sharp battleaxe resting on his shoulder. "
            "Fiery celestial energy aura radiating around him, ancient Indian epic aesthetic, 8k photorealistic detail, dramatic mythological lighting."
        ),
        "out": OUTPUT_DIR / "shot1_parashurama_arrival.mp4"
    },
    {
        "name": "shot2_parashurama_speaking_hindi",
        "prompt": (
            "Cinematic 9:16 vertical dramatic close-up of Bhagwan Parashurama, an intensely powerful ancient Indian warrior-sage with glowing wrathful eyes and long matted hair. "
            "He speaks forcefully and furiously in Hindi with realistic mouth movement and lip-sync: "
            "'किसने तोड़ा मेरे गुरु महादेव का यह पावन पिनाक? सामने आ, वर्ना आज पूरी मिथिला को भस्म कर दूँगा!' "
            "Golden royal palace pillars in background, dramatic volumetric rim lighting, 8k photorealistic quality, divine rage."
        ),
        "out": OUTPUT_DIR / "shot2_parashurama_speaking_hindi.mp4"
    },
    {
        "name": "shot3_lakshmana_speaking_hindi",
        "prompt": (
            "Cinematic 9:16 vertical medium shot of Prince Lakshmana, a young, handsome warrior prince in radiant royal silk robes and gold ornaments. "
            "Standing courageously in the royal court, he smiles defiantly with fearless eyes and speaks witty Hindi dialogue with realistic lip-sync: "
            "'हे मुनिवर! बचपन में हमने कई धनुहियां तोड़ीं, तब तो कभी ऐसा क्रोध नहीं किया! इस पुराने धनुष पर इतनी ममता क्यों?' "
            "Opulent ancient palace background, warm cinematic lighting, photorealistic 8k, heroic determination."
        ),
        "out": OUTPUT_DIR / "shot3_lakshmana_speaking_hindi.mp4"
    },
    {
        "name": "shot4_rama_serenity_outro",
        "prompt": (
            "Cinematic 9:16 vertical shot of Maryada Purushottam Prabhu Shri Rama, a serene and divinely beautiful youthful prince in royal saffron silk, "
            "stepping forward with gentle grace and folded hands in deep humility and peaceful authority. "
            "A celestial golden aura emanates from Him, turning the stormy court atmosphere into divine peaceful radiance. "
            "Ancient Indian epic aesthetic, majestic Mithila palace hall, 8k photorealistic quality, serene spiritual atmosphere."
        ),
        "out": OUTPUT_DIR / "shot4_rama_serenity_outro.mp4"
    }
]

def main():
    for idx, job in enumerate(JOBS, 1):
        out_file = job["out"]
        if out_file.exists() and out_file.stat().st_size > 100000:
            print(f"[{idx}/4] Skipping {job['name']} (already generated: {out_file.stat().st_size} bytes)")
            continue

        print(f"\n[{idx}/4] 🎬 Generating Gemini Omni 1.2 Flash Pure Video: {job['name']}...")
        try:
            interaction = client.interactions.create(
                model='gemini-omni-1.2-flash',
                input=job["prompt"],
                response_format=resp_fmt
            )
            print("Status:", interaction.status)
            if interaction.output_video and interaction.output_video.data:
                data = interaction.output_video.data
                raw_bytes = base64.b64decode(data) if isinstance(data, str) else data
                with open(out_file, 'wb') as f:
                    f.write(raw_bytes)
                print(f"✅ Successfully saved: {out_file} ({len(raw_bytes)} bytes)!")
            else:
                print(f"❌ No video data returned for {job['name']}: {interaction}")
        except Exception as e:
            print(f"❌ Error generating {job['name']}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
