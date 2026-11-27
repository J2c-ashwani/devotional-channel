#!/usr/bin/env python3
"""
Generate Shot 5 for the Expanded Ramayana Episode 2 (65s Long Cut):
Bhagwan Parashurama bowing with folded hands and tearful devotion before Maryada Purushottam Prabhu Shri Rama,
realizing that Shri Rama is Bhagwan Vishnu himself! Golden celestial flower petals raining in Mithila palace.
"""

import os
import sys
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
out_file = OUTPUT_DIR / "shot5_parashurama_bowing_to_rama.mp4"

resp_fmt = interactions.VideoResponseFormat(
    type='video',
    aspect_ratio='9:16',
    duration='8s',
    resolution='720p',
    delivery='inline'
)

prompt = (
    "Cinematic 9:16 vertical shot in the ancient grand royal durbar of Mithila. "
    "The mighty warrior-sage Bhagwan Parashurama, now humbled with tearful devotion, bows with folded hands before Prabhu Shri Rama. "
    "Prabhu Shri Rama stands majestic in royal saffron pitambara silk and golden Surya-vamsha Kirita crown (strictly no peacock feather), smiling with divine compassion. "
    "Golden celestial light radiates across the palace pillars, golden lotus petals rain gently from above, epic emotional spiritual climax, photorealistic 8k."
)

print("🎬 Generating Shot 5: Parashurama bowing before Shri Rama in divine revelation...")
try:
    interaction = client.interactions.create(
        model='gemini-omni-1.2-flash',
        input=prompt,
        response_format=resp_fmt
    )
    print("Status:", interaction.status)
    if interaction.output_video and interaction.output_video.data:
        data = interaction.output_video.data
        raw_bytes = base64.b64decode(data) if isinstance(data, str) else data
        with open(out_file, 'wb') as f:
            f.write(raw_bytes)
        print(f"✅ Successfully saved Shot 5: {out_file} ({len(raw_bytes)} bytes)!")
    else:
        print("❌ No video data:", interaction)
        sys.exit(1)
except Exception as e:
    print("❌ Error:", e)
    sys.exit(1)
