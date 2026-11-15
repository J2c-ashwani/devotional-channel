import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

class UploadLedger:
    """
    Module O: Upload Idempotency Ledger.
    Computes SHA-256 hash of rendered video files to ensure no file is ever uploaded twice.
    """

    @classmethod
    def compute_sha256(cls, file_path: Path) -> str:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
