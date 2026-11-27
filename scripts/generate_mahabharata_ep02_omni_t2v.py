#!/usr/bin/env python3
"""
Pure Text-to-Video Generation for Mahabharata Episode 2 using Google Vertex AI (gemini-omni-1.2-flash).
Topic: देवव्रत की 'भीष्म प्रतिज्ञा': पिता के सुख के लिए आजीवन ब्रह्मचर्य और राज्य का त्याग
- 100% Pure Vertex Text-to-Video at native 1080x1920 (9:16). Zero static images, zero stretched TTS.
- Strictly paced at <=2 words/sec per spoken beat so ZERO words clip or cut off.
- Talking Heads: Nishadaraj (Acts 2 & 4) + Rajkumar Devavrata/Bhishma (Acts 3 & 5),
  with Kathavachak Narrator opening (Act 1) and epilogue + Part 3 Eklavya Hook (Act 6).
"""

import os
import sys
import time
import base64
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai._gaos.types import interactions
from google.cloud import storage

BASE_DIR = Path("/Users/ashwanikumar/Downloads/devotional")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(BASE_DIR / 'service-account.json')
os.environ['GOOGLE_CLOUD_PROJECT'] = 'devotional-youtube-514907'

OUTPUT_DIR = BASE_DIR / "storage" / "rendered" / "mahabharata_ep02"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GCS_BUCKET = "itihasa-saga-storage-514907"

SCENES = [
    {
        "id": "scene_01_ganga_returns_devavrata",
        "duration": "12s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian Mahabharata epic film scene on the misty golden banks of sacred river Ganga transitioning toward royal Hastinapur. No on-screen text.\n"
            "[0-7s] At glowing sunrise along holy river Ganga, celestial Goddess Ganga in shimmering white silk proudly presents tall, handsome young warrior prince Devavrata (ivory-white & gold Kuru warrior silk, golden royal headband crown, celestial bow quiver) to joyful aged King Shantanu (crimson-gold silk, white beard, royal crown).\n"
            "[7-12s] Cut to quiet twilight along the Yamuna riverbank where King Shantanu walks thoughtfully with wistful longing in his eyes.\n"
            "Voiceover [0.5s-10.2s] — Deep, warm resonant mature Indian male Kathavachak narrator speaking clearly and distinctly every single Hindi word over soft mystical bansuri and flowing river sounds, leaving 2s calm music at the end: "
            "'वर्षों बाद देवी गंगा ने शांतनु को महावीर पुत्र देवव्रत लौटाया। पर आगे सत्यवती के विवाह हेतु राजा शांतनु व्याकुल हो उठे!'"
        )
    },
    {
        "id": "scene_02_nishadaraj_condition",
        "duration": "12s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological talking-head scene inside a carved wooden riverside pavilion overlooking calm golden Yamuna waters at dusk. No on-screen text.\n"
            "[0-12s] Medium close-up talking-head of dignified elderly fisherman chieftain Nishadaraj (weathered wise Indian elder with silver beard, maroon cotton shawl, rudraksha mala) standing unyieldingly before handsome young Prince Devavrata (ivory-white and gold silk armor, golden royal crown circlet). "
            "Nishadaraj looks firmly at Devavrata and speaks clearly in a strong, stern elderly male Hindi voice with exact realistic lip-sync, finishing completely before 10s leaving 2s tense silence and river ambience: "
            "'राजकुमार देवव्रत! आपकी संतान के रहते मेरी पुत्री सत्यवती का पुत्र कभी हस्तिनापुर का सम्राट नहीं बन पाएगा!'"
        )
    },
    {
        "id": "scene_03_devavrata_renounces_throne",
        "duration": "12s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological hero talking-head scene on the wind-swept Yamuna riverbank in warm sunset light. No on-screen text.\n"
            "[0-12s] Heroic medium close-up talking-head of noble young warrior Prince Devavrata (tall radiant youth, luminous serene eyes blazing with filial devotion, ivory-white and gold embroidered Kuru royal silk, golden shoulder armor, carved golden headband crown). "
            "Stepping forward firmly with one hand extended in solemn promise, Devavrata speaks directly on camera in a clear, powerful youthful royal baritone Hindi voice with crisp lip-sync, finishing smoothly by 10s: "
            "'सुनिए निषादराज! आज ही मैं हस्तिनापुर के राजसिंहासन का त्याग करता हूँ—सत्यवती का पुत्र ही सम्राट होगा!'"
        )
    },
    {
        "id": "scene_04_nishadaraj_final_doubt",
        "duration": "12s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological talking-head scene in the Yamuna riverside pavilion at twilight. No on-screen text.\n"
            "[0-12s] Reverse close-up talking-head of cautious elderly chieftain Nishadaraj (grey beard, maroon cotton shawl, rudraksha mala) looking deeply skeptical and worried as he shakes his head subtly and speaks directly to Prince Devavrata in clear, anxious elderly male Hindi with realistic lip-sync, finishing comfortably by 10s: "
            "'राजकुमार! आप तो वचन के पक्के हैं... पर कल को आपकी संतानों ने राज्य मांग लिया, तब क्या होगा?'"
        )
    },
    {
        "id": "scene_05_bhishma_pratigya_oath",
        "duration": "15s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian epic climax scene on the sacred riverbank beneath dramatic swirling clouds and golden lightning rays. No on-screen text.\n"
            "[0-9.5s] Intense close-up talking-head of valiant Prince Devavrata (ivory-white & gold Kuru silk armor, golden royal headband crown, wind whipping dark locks) raising his right arm boldly toward the heavens in solemn sacred oath. With unwavering blazing resolve and exact Hindi lip-sync, he speaks powerfully in a deep resounding youthful heroic voice, finishing clearly by 9.2s: "
            "'तो सुनिए जगत के साक्षी! मैं आज से आजीवन अखंड ब्रह्मचर्य का पालन करूँगा—मैं कभी विवाह नहीं करूँगा!'\n"
            "[9.5-15s] Instant cosmic wonder: storm clouds part in brilliant golden god-rays, fragrant golden parijat flower petals shower gracefully from the sky across Devavrata's bowed noble figure amidst thunderous epic orchestral music and temple bells (no spoken speech after 9.5s)."
        )
    },
    {
        "id": "scene_06_bhishma_epilogue_eklavya_hook",
        "duration": "14s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological film finale transitioning from Hastinapur palace ramparts to a sacred forest ashram clearing at twilight. No on-screen text.\n"
            "[0-8s] Towering victorious Pitamaah Bhishma in gleaming ivory-white and gold silk stands serenely on Hastinapur palace courtyard under showering golden petals as elderly King Shantanu blesses him tearfully.\n"
            "[8-14s] Dramatic transition into a misty ancient forest clearing lit by ritual firelight where an intense young tribal forest archer draws a wooden bow in secret devotion before a clay guru idol while distant thunder rumbles and a resonant temple Shankh conch echoes loudly.\n"
            "Voiceover [0.5s-11.2s] — Deep, commanding Indian male Kathavachak narrator speaking clearly in Hindi with full sentence completion before the booming Shankh finish from 11.2s-14s: "
            "'उस दिन से देवव्रत भीष्म कहलाए! आगे गुरु द्रोण के किस शिष्य ने गुरु-दक्षिणा में अनूठा बलिदान दिया? जानिए भाग 3 में!'"
        )
    }
]


def generate_scene(scene_cfg: dict, idx: int, total: int):
    sid = scene_cfg["id"]
    out_file = OUTPUT_DIR / f"{sid}.mp4"
    if out_file.exists() and out_file.stat().st_size > 200_000:
        print(f"[{idx}/{total}] Skipping {sid} (already exists: {out_file.stat().st_size:,} bytes)")
        return out_file

    client = genai.Client(
        vertexai=True,
        project='devotional-youtube-514907',
        location='global',
        http_options={'timeout': 600000}
    )

    gcs_target = f"gs://{GCS_BUCKET}/mahabharata_ep02_t2v/{sid}_{int(time.time())}.mp4"
    fmt = interactions.VideoResponseFormat(
        type="video",
        aspect_ratio="9:16",
        duration=scene_cfg["duration"],
        resolution="1080p",
        delivery="uri",
        gcs_uri=gcs_target
    )

    print(f"[{idx}/{total}] 🎬 Generating 1080p Vertex Text-to-Video ({scene_cfg['duration']}): {sid}...")
    for attempt in range(2):
        try:
            interaction = client.interactions.create(
                model="gemini-omni-1.2-flash",
                input=scene_cfg["prompt"],
                response_format=fmt
            )
            ov = getattr(interaction, "output_video", None)
            uri = getattr(ov, "uri", None) if ov else None
            if not uri:
                for step in getattr(interaction, "steps", []) or []:
                    for c in getattr(step, "content", []) or []:
                        if getattr(c, "type", None) == "video" and getattr(c, "uri", None):
                            uri = c.uri
                            break
            if uri and uri.startswith("gs://"):
                parts = uri.replace("gs://", "").split("/", 1)
                sc = storage.Client(project="devotional-youtube-514907")
                sc.bucket(parts[0]).blob(parts[1]).download_to_filename(str(out_file))
                print(f"✅ [{idx}/{total}] {sid} ready: {out_file.stat().st_size:,} bytes (GCS)")
                return out_file
            elif ov and getattr(ov, "data", None):
                raw_bytes = base64.b64decode(ov.data) if isinstance(ov.data, str) else ov.data
                out_file.write_bytes(raw_bytes)
                print(f"✅ [{idx}/{total}] {sid} ready inline: {len(raw_bytes):,} bytes")
                return out_file
            raise RuntimeError(f"Empty video payload: status={interaction.status}")
        except Exception as e:
            print(f"⚠️ [{idx}/{total}] Attempt {attempt+1} failed for {sid}: {e}")
            if attempt == 0:
                time.sleep(3)
                fmt = interactions.VideoResponseFormat(
                    type="video", aspect_ratio="9:16", duration=scene_cfg["duration"],
                    resolution="720p", delivery="inline"
                )
    raise RuntimeError(f"Failed generating {sid}")


def main():
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    todo = [(i, s) for i, s in enumerate(SCENES, 1) if (only is None or s["id"] in only)]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(generate_scene, s, i, len(SCENES)): s["id"] for i, s in todo}
        for fut in as_completed(futs):
            fut.result()

    print("\n=== MAHABHARATA EP02 PROBE ===")
    for s in SCENES:
        p = OUTPUT_DIR / f"{s['id']}.mp4"
        if p.exists():
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "stream=width,height,codec_type:format=duration", "-of", "compact", str(p)],
                capture_output=True, text=True
            )
            print(f"{s['id']}: {probe.stdout.strip().replace(chr(10), ' | ')}")


if __name__ == "__main__":
    main()
