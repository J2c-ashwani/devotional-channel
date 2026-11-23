#!/usr/bin/env python3
"""
Regenerate Scene 4 for Ramayana Episode 2 with 100% authentic canonical iconography:
- Maryada Purushottam Prabhu Shri Rama
- Authentic Surya-vamsha Royal Golden Crown (Kirita Mukuta) with pearls and rubies
- STRICTLY NO peacock feather / NO mayur pankh (peacock feather is exclusive to Shri Krishna)
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
out_file = OUTPUT_DIR / "shot4_rama_serenity_outro.mp4"

resp_fmt = interactions.VideoResponseFormat(
    type='video',
    aspect_ratio='9:16',
    duration='8s',
    resolution='720p',
    delivery='inline'
)

prompt = (
    "Cinematic 9:16 vertical shot of Maryada Purushottam Prabhu Shri Rama in the grand ancient palace of Mithila. "
    "A divinely serene, noble young prince of the Sun dynasty (Surya-vamsha) in glowing royal pitambara saffron silk robes and gold jewelry. "
    "He wears a classical ancient Vedic golden royal crown (Kirita Mukuta) adorned with radiant pearls and red rubies, traditional royal crest, strictly NO peacock feather, NO peacock plume, strictly regal crown only. "
    "He steps forward with gentle grace and folded hands (anjali mudra) with a calm, compassionate divine smile, radiating serene peace. "
    "Soft celestial golden aura illuminating the palace hall, dissolving the stormy darkness into spiritual peace. "
    "Photorealistic 8k, majestic Indian epic cinematography, supreme devotional grace."
)

print("🎬 Regenerating Shot 4: Shri Rama with authentic Surya-vamsha Kirita Crown (NO Peacock Feather)...")
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
        print(f"✅ Successfully saved corrected Shot 4: {out_file} ({len(raw_bytes)} bytes)!")
    else:
        print("❌ No video data:", interaction)
        sys.exit(1)
except Exception as e:
    print("❌ Error:", e)
    sys.exit(1)
