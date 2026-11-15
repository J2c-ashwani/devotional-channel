import asyncio
import argparse
import json
import sys
from backend.app.pipeline.orchestrator import ProductionPipelineOrchestrator
from backend.app.pipeline.emergency import EmergencyKillSwitch

async def main():
    parser = argparse.ArgumentParser(description="Autonomous YouTube Content Production CLI")
    parser.add_argument("--format", choices=["SHORT", "LONG_FORM", "MONTHLY_SPECIAL"], default="SHORT", help="Format to produce")
    parser.add_argument("--scene-duration", type=float, default=None, help="Optional scene duration override in seconds (useful for fast verification)")
    parser.add_argument("--simulate-upload", action="store_true", default=True, help="Simulate upload if live credentials are not set")
    parser.add_argument("--kill-switch", action="store_true", help="Arm emergency kill switch")
    args = parser.parse_args()

    if args.kill_switch:
        EmergencyKillSwitch.activate("CLI command")
        print("🚨 Emergency Kill Switch Activated. All production stopped.")
        sys.exit(0)

    print(f"🎬 Initiating Autonomous Pipeline Run for: {args.format}...")
    orchestrator = ProductionPipelineOrchestrator()
    result = await orchestrator.execute_production_run(
        format_type=args.format,
        simulate_upload=args.simulate_upload,
        scene_duration_override=args.scene_duration
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
        print(f"✅ Production & Scheduling Succeeded! QC Score: {result.get('qc_score')} / 100")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
