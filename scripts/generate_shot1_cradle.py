#!/usr/bin/env python3
"""
Generate Shot 1: Goddess Ganga gently placing infant in the flowing river Ganga
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

OUTPUT_DIR = Path("/Users/ashwanikumar/Downloads/devotional/storage/rendered/mahabharata_ep01")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
out_file = OUTPUT_DIR / "shot1_ganga_cradle_baby.mp4"

resp_fmt = interactions.VideoResponseFormat(
    type='video',
    aspect_ratio='9:16',
    duration='8s',
    resolution='720p',
    delivery='inline'
)

prompt = (
    "Cinematic 9:16 vertical shot of Goddess Ganga, an ethereal celestial goddess in flowing glowing white silk garments, "
    "standing in the sacred misty waters of river Ganga at twilight. "
    "She is gently placing a sacred glowing golden cradle containing a divine infant prince into the flowing sacred river waters. "
    "Ancient Indian sacred forest shore, golden twilight reflections on water ripples, divine flowers floating, photorealistic 8k, mythical epic ambiance."
)

print("🎬 Calling Gemini Omni 1.2 Flash for Shot 1 (Goddess Ganga flowing infant in river)...")
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
        print(f"✅ Successfully saved: {out_file} ({len(raw_bytes)} bytes)!")
    else:
        print("❌ No video data:", interaction)
except Exception as e:
    print("❌ Error:", e)
    sys.exit(1)
