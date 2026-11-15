import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from backend.app.config import settings

class AutonomousRecoveryEngine:
    """
    Module T: Autonomous Recovery & Checkpoint Engine.
    Preserves pipeline progress across state transitions:
    - CHECKPOINT_RESEARCH
    - CHECKPOINT_FACT_CHECK
    - CHECKPOINT_SCREENPLAY
    - CHECKPOINT_STORYBOARD
    - CHECKPOINT_VOICEOVER
    - CHECKPOINT_VISUALS
    - CHECKPOINT_RENDER
    - CHECKPOINT_QC
    - CHECKPOINT_UPLOAD

    If any API or worker times out or crashes, the pipeline resumes from the last
    checkpoint without re-spending credits on completed steps.
    """

    CHECKPOINT_DIR = settings.STORAGE_DIR / "checkpoints"

    @classmethod
    def save_checkpoint(cls, job_id: str, stage_name: str, payload: Dict[str, Any]) -> Path:
        cls.CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        job_dir = cls.CHECKPOINT_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        checkpoint_path = job_dir / f"{stage_name}.json"
        data = {
            "job_id": job_id,
            "stage": stage_name,
            "saved_at": datetime.utcnow().isoformat(),
            "payload": payload
        }
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return checkpoint_path

    @classmethod
    def load_last_checkpoint(cls, job_id: str) -> Optional[Dict[str, Any]]:
        job_dir = cls.CHECKPOINT_DIR / job_id
        if not job_dir.exists():
            return None

        # Sorted by creation time descending
        checkpoints = sorted(job_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not checkpoints:
            return None

        try:
            with open(checkpoints[0], "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    @classmethod
    def clear_job_checkpoints(cls, job_id: str):
        job_dir = cls.CHECKPOINT_DIR / job_id
        if job_dir.exists():
            for f in job_dir.glob("*.json"):
                f.unlink(missing_ok=True)
