#!/usr/bin/env python3
"""
One-Click YouTube OAuth2 Authorization Helper for Itihasa Saga.
Authorizes the studio pipeline to upload videos directly to YouTube.
"""

import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
ENV_LOCAL_PATH = BASE_DIR / ".env.local"
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]

def update_env_local(key: str, val: str):
    lines = []
    found = False
    if ENV_LOCAL_PATH.exists():
        with open(ENV_LOCAL_PATH, "r") as f:
            lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={val}\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"{key}={val}\n")
        
    with open(ENV_LOCAL_PATH, "w") as f:
        f.writelines(new_lines)
    print(f"✅ Saved {key} to .env.local")

def main():
    if not CLIENT_SECRET_FILE.exists():
        print(f"❌ Error: {CLIENT_SECRET_FILE} not found!")
        sys.exit(1)

    print("\n" + "="*60)
    print("🏹 ITIHASA SAGA — YOUTUBE CHANNEL OAUTH AUTHORIZATION")
    print("="*60)

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE),
        scopes=SCOPES,
    )

    # Let run_local_server handle the flow directly to ensure matching CSRF state
    creds = flow.run_local_server(
        host="localhost",
        port=8088,
        authorization_prompt_message=(
            "\n👉 Please authorize the Itihasa Saga YouTube connection:\n"
            "------------------------------------------------------------\n"
            "{url}\n"
            "------------------------------------------------------------\n"
            "🌐 Opening in your browser now...\n"
        ),
        success_message="🎉 Authorization successful! You can close this window now.",
        open_browser=True,
        access_type="offline",
        prompt="consent",
    )

    print("\n" + "="*60)
    print("🎉 AUTHORIZATION SUCCESSFUL!")
    print("="*60)

    refresh_token = creds.refresh_token
    client_id = creds.client_id
    client_secret = creds.client_secret

    update_env_local("YOUTUBE_CLIENT_ID", client_id)
    update_env_local("YOUTUBE_CLIENT_SECRET", client_secret)
    update_env_local("YOUTUBE_REFRESH_TOKEN", refresh_token)

    # Test API connection
    try:
        youtube = build("youtube", "v3", credentials=creds)
        res = youtube.channels().list(mine=True, part="snippet,statistics").execute()
        if res.get("items"):
            channel = res["items"][0]
            title = channel["snippet"]["title"]
            cid = channel["id"]
            subs = channel["statistics"].get("subscriberCount", "0")
            vids = channel["statistics"].get("videoCount", "0")
            update_env_local("YOUTUBE_CHANNEL_ID", cid)
            print(f"✅ Verified Channel: {title}")
            print(f"   Channel ID: {cid}")
            print(f"   Subscribers: {subs} | Videos: {vids}")
    except Exception as e:
        print("Note on verification:", e)

    # Automatically sync refreshed YouTube OAuth credentials to GitHub Actions Secrets
    try:
        from scripts.sync_github_secrets import sync_secrets
        sync_secrets(["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"])
        print("✅ GitHub Actions Secrets updated cleanly with the new YouTube token!")
    except Exception as e:
        print("⚠️ Note syncing GitHub Secrets:", e)

    print("="*60)
    print("🚀 Channel is now connected locally AND on GitHub Actions Cloud!")

if __name__ == "__main__":
    main()
