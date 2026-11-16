#!/usr/bin/env python3
"""
Generate 100% Full Video for all 5 scenes using Google Veo 3.1 & Omni Flash Image-to-Video (I2V):
- Shot 1: Mithila Court & 8-wheeled Pinaka vault (already generated: storage/rendered/shot1_i2v_pinaka.mp4)
- Shot 2A: King Janaka's anguish on throne (from king_janaka_anguish_mithila_court_1794820082978.jpg)
- Shot 2B: Sage Vishvamitra commanding young Prince Rama (from vishvamitra_orders_rama_mithila_1794775952411.jpg)
- Shot 3: Shri Rama breaking the Pinaka bow with lightning (from scene_3_rama_breaks_pinaka_bow_1794776003893.jpg)
- Shot 4: Sacred aftermath & conch (from mithila_pinaka_court_1794775884188.jpg)
"""

import os
import time
from pathlib import Path
from backend.app.config import settings
from google import genai
from google.genai import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
os.environ['GOOGLE_CLOUD_PROJECT'] = settings.GOOGLE_CLOUD_PROJECT

client = genai.Client(
    vertexai=True,
    project=settings.GOOGLE_CLOUD_PROJECT,
    location=settings.GOOGLE_CLOUD_LOCATION
)

STORAGE_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/rendered")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

JOBS = [
    {
        "name": "shot2a_janaka",
        "img": "/Users/ashwanikumar/.gemini/antigravity/brain/a656ac81-e178-40b9-8293-9783dd71323a/king_janaka_anguish_mithila_court_1794820082978.jpg",
        "prompt": "Cinematic slow camera tracking forward toward King Janaka standing by his golden throne, royal robes gently swaying, volumetric sunbeams shimmering in Mithila palace, dramatic sorrowful expression, photorealistic 8k",
        "out": STORAGE_DIR / "shot2a_i2v_janaka.mp4"
    },
    {
        "name": "shot2b_vishvamitra",
        "img": "/Users/ashwanikumar/.gemini/antigravity/brain/a656ac81-e178-40b9-8293-9783dd71323a/vishvamitra_orders_rama_mithila_1794775952411.jpg",
        "prompt": "Cinematic slow upward tilt, holy incense smoke rising from the golden altar, Sage Vishvamitra radiating golden aura with raised blessing hand, Prince Rama bowing reverently, divine atmosphere, photorealistic 8k",
        "out": STORAGE_DIR / "shot2b_i2v_vishvamitra.mp4"
    },
    {
        "name": "shot3_rama_bow",
        "img": "/Users/ashwanikumar/.gemini/antigravity/brain/a656ac81-e178-40b9-8293-9783dd71323a/scene_3_rama_breaks_pinaka_bow_1794776003893.jpg",
        "prompt": "Cinematic intense slow-motion, divine celestial lightning crackling and bursting from the shattering Pinaka bow, energy sparks flying outward, Prince Rama standing victorious, epic godlike climax, photorealistic 8k",
        "out": STORAGE_DIR / "shot3_i2v_rama_bow.mp4"
    }
]

def generate_and_poll(job):
    out_file = job["out"]
    if out_file.exists() and out_file.stat().st_size > 100000:
        print(f"Skipping {job['name']} (already generated: {out_file.stat().st_size} bytes)")
        return

    print(f"\n--- Starting Image-to-Video for {job['name']} ---")
    image = types.Image.from_file(location=job["img"])
    operation = client.models.generate_videos(
        model='veo-3.1-fast-generate-001',
        source=types.GenerateVideosSource(
            prompt=job["prompt"],
            image=image
        ),
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            duration_seconds=6,
            aspect_ratio='9:16'
        )
    )
    print(f"Operation created for {job['name']}: {operation.name}")

    for attempt in range(15):
        time.sleep(15)
        res = client.operations.get(operation)
        print(f"[{job['name']}] Attempt {attempt+1}: done={res.done}")
        if res.done:
            if res.error:
                print(f"[{job['name']}] Error:", res.error)
            elif res.response and res.response.generated_videos:
                video = res.response.generated_videos[0].video
                for attr in ['video_bytes', 'bytes', 'data', 'content']:
                    if hasattr(video, attr) and getattr(video, attr):
                        with open(out_file, 'wb') as f:
                            f.write(getattr(video, attr))
                        print(f" Successfully saved: {out_file} ({out_file.stat().st_size} bytes)")
                        break
            break

def main():
    for job in JOBS:
        generate_and_poll(job)
    print("\nAll Image-to-Video jobs processed!")

if __name__ == "__main__":
    main()
