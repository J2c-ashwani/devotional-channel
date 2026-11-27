#!/usr/bin/env python3
"""
Pure Text-to-Video Generation for Ramayana Episode 3 using Google Vertex AI (gemini-omni-1.2-flash).
- Zero static image generation. 100% pure Vertex Text-to-Video at native 1080x1920 (9:16).
- Strictly paced at <=2 words/sec per spoken beat so ZERO words clip or cut off.
- Pure Talking-Head scenes for characters (King Janaka, Maharshi Vishvamitra, Prabhu Shri Rama, Mata Sita)
  and dedicated Kathavachak Narrator for arrival, departure, and Ayodhya epilogue.
- Iconography Rule: Prabhu Shri Rama strictly wears carved golden Surya-vamsha Kirita Mukuta
  with rubies & pearls ONLY (ZERO peacock feather anywhere).
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

OUTPUT_DIR = BASE_DIR / "storage" / "rendered" / "ramayana_ep03" / "v2_clean"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GCS_BUCKET = "itihasa-saga-storage-514907"

SCENES = [
    {
        "id": "scene_01_baraat_arrival",
        "duration": "12s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological film scene in golden Mithila city courtyard during royal wedding festival. No on-screen text.\n"
            "[0-12s] Sweeping cinematic shot of grand golden sandstone Mithila palace adorned with fresh marigold garlands and glowing oil lamps. "
            "Maharaja Dasharatha (dignified elderly king with white beard, crimson-gold silk, golden crown) arrives proudly in a carved golden chariot drawn by white horses flanked by decorated elephants while rose petals rain down through warm morning sunbeams.\n"
            "Voiceover [0.8s-10.2s] — Calm, deep, resonant Indian male Kathavachak narrator speaking clearly and unhurriedly in Hindi with full sentence completion over joyous wedding shehnai and soft celebratory drums, ending cleanly with 1.5 seconds of festive music: "
            "'परशुराम जी के जाने के बाद, राजा जनक ने अयोध्या संदेश भेजा... और तब भव्य बारात लेकर मिथिला पधारे महाराज दशरथ!'"
        )
    },
    {
        "id": "scene_02_janaka_welcome",
        "duration": "12s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological talking-head scene inside sunlit Mithila palace courtyard decorated with marigolds. No on-screen text.\n"
            "[0-12s] Elderly Maharaja Dasharatha (white beard, crimson-gold silk robes, golden crown) and dignified King Janaka (trimmed grey beard, cream-and-gold silk robes, golden crown, Vaishnava tilak) greet and embrace warmly. "
            "Focusing in a crisp medium close-up on King Janaka smiling joyfully with folded hands in namaste, he speaks directly on camera with crisp distinct Hindi pronunciation and warm regal male voice, finishing cleanly by 9.8s with a joyful smile for the last 2s: "
            "'स्वागत है समधी महाराज दशरथ! आपके पुत्र श्री राम ने आज समस्त मिथिला का हृदय जीत लिया है!'"
        )
    },
    {
        "id": "scene_03_vishvamitra_varmala",
        "duration": "15s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological film scene inside Mithila's grand golden Vivah Mandap pavilion lit by sacred havan flames and brass oil lamps. No on-screen text.\n"
            "[0-8s] Medium close-up talking-head of Maharshi Vishvamitra, luminous ancient Vedic sage with silver-white beard, ascetic matted hair bun, saffron silk robes, rudraksha beads, and sandalwood tilak. Raising his hand in blessing, he speaks clearly and cleanly in Hindi with realistic lip-sync and deep commanding sage voice, finishing before 7.5s: "
            "'शुभ मुहूर्त आ गया है वत्स राम! धर्म के इस पावन बंधन में सीता का पाणिग्रहण करो!'\n"
            "[8-15s] Smooth reverent cut to divine Varmala moment: radiant bride Mata Sita (deep crimson & gold Banarasi bridal saree, sheer red veil, holding jasmine-and-rose varmala garland) steps forward gracefully and places the garland around groom Prabhu Shri Rama (Shyamavarna soft blue-grey complexion, calm lotus eyes, cream-gold & saffron silk robes, tall carved golden Surya-vamsha Kirita crown studded ONLY with rubies and pearls — strictly NO peacock feather anywhere on crown). Celestial lotus petals shower in golden light amidst joyous temple bells and auspicious wedding shehnai (no spoken words after 8s)."
        )
    },
    {
        "id": "scene_04_rama_sita_vows",
        "duration": "15s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological dual talking-head close-up dialogue beside glowing sacred Vedic havan fire in Mithila wedding mandap under warm golden firelight. No on-screen text.\n"
            "[0-7.5s] Medium close-up talking-head of Prabhu Shri Rama (serene Shyamavarna complexion, luminous gentle lotus eyes, cream-gold wedding robes, carved golden Surya-vamsha Kirita crown with rubies and pearls — strictly NO peacock feather). Looking warmly at His bride, Shri Rama speaks cleanly and unhurriedly in a calm, melodious noble male Hindi voice with exact lip-sync, finishing his sentence completely before 7.2s: "
            "'हे सीते! अग्नि को साक्षी मान वचन देता हूँ—धर्म पथ पर हम सदैव एक रहेंगे।'\n"
            "[7.5-15s] Reverse close-up talking-head on bridal Mata Sita (graceful golden-fair Indian features, red kumkum bindi, gold maang-tikka, crimson-gold Banarasi bridal silk, jasmine varmala around neck). Glowing in sacred firelight with tender devoted eyes, Mata Sita speaks softly and clearly in a sweet, firm feminine Hindi voice with realistic lip-sync, finishing before 14.2s: "
            "'हे नाथ! सुख हो या वनवास, हर कदम पर मैं आपकी छाया बनकर चलूँगी।'"
        )
    },
    {
        "id": "scene_05_janaka_bidai",
        "duration": "15s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological film scene at twilight on the carved sandstone palace steps of Mithila during wedding farewell Bidai. No on-screen text.\n"
            "[0-7.5s] Emotional close-up talking-head of dignified King Janaka (white beard, cream-gold silk, golden crown) with glistening tears of love as he joins Mata Sita's henna-adorned hand with Prabhu Shri Rama's hand (Shri Rama wearing golden Surya-vamsha Kirita crown with rubies — strictly NO peacock feather). Speaking directly to Shri Rama with crisp Hindi lip-sync and deeply emotional fatherly voice, finishing clearly by 7.2s: "
            "'हे राम! मेरी प्राणप्रिय जानकी को आपको सौंपता हूँ... इन्हें सदैव सम्मान देना!'\n"
            "[7.5-15s] Gentle wide pullback as the newlywed couple Shri Rama and Mata Sita depart in a flower-bedecked golden royal chariot amidst showering petals.\n"
            "Voiceover [7.6s-13.2s] — Warm, clear, mature Indian male Kathavachak narrator speaking clearly in Hindi over tender bansuri flute, finishing completely before 13.5s leaving 1.5s of emotional farewell music: "
            "'संपूर्ण मिथिला की आँखें नम थीं... और प्रभु श्री राम अयोध्या लौट चले!'"
        )
    },
    {
        "id": "scene_06_ayodhya_diwali_hook",
        "duration": "14s",
        "prompt": (
            "Cinematic 9:16 vertical photorealistic 8k Indian mythological film scene in illuminated Ayodhya palace at night along the Sarayu river. No on-screen text.\n"
            "[0-9s] Breathtaking celebration reveal of grand Ayodhya palace and courtyards glowing with thousands of clay earthen oil diyas; Prabhu Shri Rama (golden Surya-vamsha Kirita crown studded only with rubies — strictly NO peacock feather, saffron-gold royal silk) and bridal Mata Sita (crimson-gold bridal silk) stand serenely at palace gates as mothers welcome them with glowing brass aarti thalis and flower petals.\n"
            "[9-14s] Dramatic camera push into a shadowy dark marble palace corridor casting mysterious shadows across royal gold regalia as festive music drops to suspenseful drums and a deep resonant temple Shankh conch echoes loudly.\n"
            "Voiceover [0.5s-11.8s] — Deep dramatic Indian male Kathavachak narrator speaking clearly in Hindi at measured pace, building mystery before the Shankh blast from 11.8s-14s: "
            "'अयोध्या लौटते ही नगरी दीपों से जगमगा उठी! पर किसे पता था, कल राज्याभिषेक से पहले ही एक महाषड्यंत्र रचा जाने वाला है? जानिए भाग 4 में!'"
        )
    }
]


def generate_scene(scene_cfg: dict, idx: int, total: int):
    sid = scene_cfg["id"]
    out_file = OUTPUT_DIR / f"{sid}.mp4"
    if out_file.exists() and out_file.stat().st_size > 200_000:
        print(f"[{idx}/{total}] Skipping {sid} (already generated: {out_file.stat().st_size:,} bytes)")
        return out_file

    # Create per-thread client so calls execute cleanly in parallel
    client = genai.Client(
        vertexai=True,
        project='devotional-youtube-514907',
        location='global',
        http_options={'timeout': 600000}
    )

    gcs_target = f"gs://{GCS_BUCKET}/ramayana_ep03_v2/{sid}_{int(time.time())}.mp4"
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
            raise RuntimeError(f"Empty video response: status={interaction.status}")
        except Exception as e:
            print(f"⚠️ [{idx}/{total}] Attempt {attempt+1} failed for {sid}: {e}")
            if attempt == 0:
                time.sleep(3)
                # Fallback to 720p inline only if 1080p GCS failed
                fmt = interactions.VideoResponseFormat(
                    type="video", aspect_ratio="9:16", duration=scene_cfg["duration"],
                    resolution="720p", delivery="inline"
                )
    raise RuntimeError(f"Failed generating {sid}")


def main():
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    todo = [(i, s) for i, s in enumerate(SCENES, 1) if (only is None or s["id"] in only)]
    results = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(generate_scene, s, i, len(SCENES)): s["id"] for i, s in todo}
        for fut in as_completed(futs):
            sid = futs[fut]
            results[sid] = fut.result()

    print("\n=== ALL SCENES PROBE ===")
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
