#!/usr/bin/env python3
"""
Generate Pure Text-to-Video for Scene 1 and Scene 4 using Gemini Omni 1.2 Flash:
- Scene 1: Eight-wheeled iron vault in Mithila with warriors
- Scene 4: Celestial sunrise flower shower and celebration in Mithila
"""

import os
import time
import base64
from pathlib import Path
from backend.app.config import settings
from google import genai
from google.genai._gaos.types import interactions

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
os.environ['GOOGLE_CLOUD_PROJECT'] = settings.GOOGLE_CLOUD_PROJECT

client = genai.Client(
    vertexai=True,
    project=settings.GOOGLE_CLOUD_PROJECT,
    location='global'
)

STORAGE_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/rendered")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "name": "shot1_pinaka_vault_t2v",
        "prompt": "Cinematic 9:16 vertical shot in grand ancient royal court of Mithila. A massive eight-wheeled iron vault holding Lord Shiva's divine bow, muscular warriors straining on heavy chains, atmospheric dust drifting in golden volumetric sunlight, dramatic royal palace ambiance, photorealistic 8k",
        "out": STORAGE_DIR / "shot1_pinaka_vault_t2v.mp4"
    },
    {
        "name": "shot4_celebration_t2v",
        "prompt": "Cinematic 9:16 vertical shot of grand Mithila palace courtyard at golden dawn sunrise. Raining divine golden flower petals gently falling from heaven, royal assembly cheering in celebration, triumphant sacred atmosphere, photorealistic 8k",
        "out": STORAGE_DIR / "shot4_celebration_t2v.mp4"
    }
]

def main():
    resp_fmt = interactions.VideoResponseFormat(
        type='video',
        aspect_ratio='9:16',
        duration='8s',
        resolution='720p',
        delivery='inline'
    )

    for job in JOBS:
        out_file = job["out"]
        if out_file.exists() and out_file.stat().st_size > 100000:
            print(f"Skipping {job['name']} (already exists: {out_file.stat().st_size} bytes)")
            continue

        print(f"\n--- Generating Pure Text-to-Video: {job['name']} ---")
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
            print(f"[{job['name']}] Saved: {out_file} ({len(raw_bytes)} bytes)!")

if __name__ == "__main__":
    main()
