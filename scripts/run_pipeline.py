import asyncio
import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.pipeline.orchestrator import ProductionPipelineOrchestrator
from backend.app.pipeline.emergency import EmergencyKillSwitch
from backend.app.config import settings

async def main():
    parser = argparse.ArgumentParser(description="Itihasa Saga Autonomous Production CLI")
    parser.add_argument("--format", choices=["SHORT", "LONG_FORM", "MONTHLY_SPECIAL"], default="SHORT", help="Format to produce")
    parser.add_argument("--track", choices=["RAMAYANA", "MAHABHARATA", "AUTO"], default="AUTO", help="Epic Track: Morning = RAMAYANA, Evening = MAHABHARATA")
    parser.add_argument("--scene-duration", type=float, default=None, help="Optional scene duration override in seconds")
    parser.add_argument("--simulate-upload", action="store_true", default=False, help="Simulate upload instead of live publishing")
    parser.add_argument("--allow-republish", action="store_true", default=False, help="Allow republishing even if episode marked complete (bypasses Single-Shot duplicate lock)")
    parser.add_argument("--kill-switch", action="store_true", help="Arm emergency kill switch")
    args = parser.parse_args()

    if args.kill_switch:
        EmergencyKillSwitch.activate("CLI command")
        print("🚨 Emergency Kill Switch Activated. All production stopped.")
        sys.exit(0)

    # Determine track automatically based on IST hour if AUTO
    track = args.track
    if track == "AUTO":
        import datetime
        import pytz
        ist = pytz.timezone(settings.PUBLISH_TIMEZONE)
        now_ist = datetime.datetime.now(ist)
        # Before 12:00 PM IST is Morning Ramayana; after 12:00 PM IST is Evening Mahabharata
        if now_ist.hour < 12:
            track = "RAMAYANA"
        else:
            track = "MAHABHARATA"

    print(f"\n" + "="*60)
    print(f"🎬 ITIHASA SAGA AUTONOMOUS PIPELINE RUN")
    print(f"Format: {args.format} | Track: {track} | Live Upload: {not args.simulate_upload}")
    print("="*60)

    orchestrator = ProductionPipelineOrchestrator()
    result = await orchestrator.execute_production_run(
        format_type=args.format,
        simulate_upload=args.simulate_upload,
        scene_duration_override=args.scene_duration,
        track=track,
        allow_republish=args.allow_republish
    )

    print("\n" + "="*60)
    print("PRODUCTION RUN RESULT:")
    print("="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*60)

    if not result.get("success"):
        print(f"❌ Production Failed / Quarantined: {result.get('error')}")
        sys.exit(1)
    else:
        print(f"✅ Production & Multi-Platform Publishing Succeeded! QC Score: {result.get('qc_score')} / 100")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
