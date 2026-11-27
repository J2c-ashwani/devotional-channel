#!/bin/bash
# Syncs the workspace repository into ~/.itihasa_saga_runtime so macOS launchd
# background scheduled jobs run cleanly with ZERO TCC Downloads-folder blocks.

set -euo pipefail

SRC="/Users/ashwanikumar/Downloads/devotional"
DST="/Users/ashwanikumar/.itihasa_saga_runtime"

mkdir -p "$DST/storage/logs"

echo "🔄 Syncing code, config, credentials, and Python runtime to $DST..."
rsync -a --delete \
  --exclude 'storage/visuals' \
  --exclude 'storage/rendered' \
  --exclude 'storage/audio' \
  --exclude 'storage/logs' \
  --exclude '__pycache__' \
  --exclude '.git' \
  "$SRC/backend" "$SRC/config" "$SRC/scripts" "$SRC/.env" "$SRC/.env.local" "$SRC/service-account.json" "$SRC/client_secret.json" "$DST/"

mkdir -p "$DST/storage/logs" "$DST/storage/visuals" "$DST/storage/rendered" "$DST/storage/audio"
# Rewrite any ~/Downloads workspace paths in synced .env.local so daemon stays TCC-isolated
if [ -f "$DST/.env.local" ]; then
    sed -i '' "s|/Users/ashwanikumar/Downloads/devotional|$DST|g" "$DST/.env.local"
fi
cp -f "$SRC/storage/episodic_progress.json" "$DST/storage/episodic_progress.json" 2>/dev/null || true
cp -f "$SRC/storage/published_scripts_ledger.json" "$DST/storage/published_scripts_ledger.json" 2>/dev/null || true
chmod +x "$DST/scripts/run_scheduled_daemon.sh" "$SRC/scripts/run_scheduled_daemon.sh"

echo "✅ Daemon runtime synced cleanly to $DST"
