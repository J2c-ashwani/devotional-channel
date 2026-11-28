#!/usr/bin/env python3
"""
Syncs local runtime secrets (.env.local + service-account.json) to GitHub Actions Secrets
for J2c-ashwani/devotional-channel using GitHub REST API + LibSodium SealedBox encryption.
Never prints secret values.
"""

import base64
import json
import subprocess
import urllib.request
from pathlib import Path
from nacl import encoding, public

REPO = "J2c-ashwani/devotional-channel"
BASE_DIR = Path(__file__).resolve().parent.parent


def _get_github_token() -> str:
    cred = subprocess.check_output(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n",
        text=True,
    )
    for line in cred.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("Could not obtain GitHub token from git credential helper.")


def _encrypt_secret(public_key_b64: str, secret_value: str) -> str:
    pk = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed = public.SealedBox(pk).encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(sealed).decode("utf-8")


def sync_secrets(keys_to_sync=None):
    token = _get_github_token()
    hdr = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }

    req_pk = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/secrets/public-key",
        headers=hdr,
    )
    with urllib.request.urlopen(req_pk) as resp:
        pk_data = json.loads(resp.read().decode("utf-8"))
    key_id = pk_data["key_id"]
    pub_key = pk_data["key"]

    env_local = {}
    env_path = BASE_DIR / ".env.local"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_local[k.strip()] = v.strip()

    secret_map = {
        "GEMINI_API_KEY": env_local.get("GEMINI_API_KEY", ""),
        "YOUTUBE_CLIENT_ID": env_local.get("YOUTUBE_CLIENT_ID", ""),
        "YOUTUBE_CLIENT_SECRET": env_local.get("YOUTUBE_CLIENT_SECRET", ""),
        "YOUTUBE_REFRESH_TOKEN": env_local.get("YOUTUBE_REFRESH_TOKEN", ""),
        "META_PERMANENT_ACCESS_TOKEN": env_local.get("META_PERMANENT_ACCESS_TOKEN", ""),
        "INSTAGRAM_ACCOUNT_ID": env_local.get("INSTAGRAM_ACCOUNT_ID", ""),
        "FACEBOOK_PAGE_ID": env_local.get("FACEBOOK_PAGE_ID", ""),
    }
    sa_path = BASE_DIR / "service-account.json"
    if sa_path.exists():
        secret_map["GCP_SA_KEY"] = sa_path.read_text(encoding="utf-8")

    for name, val in secret_map.items():
        if keys_to_sync and name not in keys_to_sync:
            continue
        if not val or "mock" in val.lower():
            continue
        payload = json.dumps({
            "encrypted_value": _encrypt_secret(pub_key, val),
            "key_id": key_id,
        }).encode("utf-8")
        req_put = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/actions/secrets/{name}",
            data=payload,
            headers=hdr,
            method="PUT",
        )
        with urllib.request.urlopen(req_put) as resp:
            if resp.status not in (201, 204):
                raise RuntimeError(f"Failed syncing secret {name}: HTTP {resp.status}")
        print(f"✅ Synced GitHub Secret: {name}")


if __name__ == "__main__":
    sync_secrets()
