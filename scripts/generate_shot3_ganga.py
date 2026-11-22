#!/usr/bin/env python3
"""
Generate Shot 3: Goddess Ganga speaking in Hindi using Gemini Omni 1.2 Flash
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
out_file = OUTPUT_DIR / "shot3_ganga_speaking_hindi.mp4"

resp_fmt = interactions.VideoResponseFormat(
    type='video',
    aspect_ratio='9:16',
    duration='8s',
    resolution='720p',
    delivery='inline'
)

# Hindi screenplay script with precise Hindi dialogue and cinematic visual cues
prompt = (
    "Cinematic 9:16 vertical close-up shot of Goddess Ganga amidst mystical glowing river mist. "
    "A radiant celestial goddess in glowing pristine white silk attire and divine golden ornaments, "
    "holding a sacred glowing golden lotus in her hands. "
    "She speaks directly to the camera in Hindi with majestic grace and divine calm: "
    "'हे राजन्! तुमने अपना वचन तोड़ दिया! अब मैं तुम्हारे साथ नहीं रह सकती, पर देवव्रत अवश्य जीवित रहेगा!' "
    "Photorealistic 8k, realistic lip-sync speaking Hindi words, divine celestial aura, cinematic lighting."
)

print("🎬 Calling Gemini Omni 1.2 Flash for Shot 3 (Goddess Ganga speaking Hindi)...")
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
        print("❌ No video data in interaction output:", interaction)
except Exception as e:
    print("❌ Error generating Shot 3:", e)
    sys.exit(1)
