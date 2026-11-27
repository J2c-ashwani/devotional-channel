#!/bin/bash
# ==============================================================================
# Itihasa Saga Autonomous Production Daemon Runner
# Runs via macOS LaunchAgent at 06:40 AM IST (Ramayana -> ~07:00 AM Live)
# and 06:10 PM IST (Mahabharata -> ~06:30 PM Live)
# Resolves REPO_DIR dynamically so it executes outside TCC-restricted ~/Downloads.
# ==============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$REPO_DIR/storage/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/daemon_$(date +%Y%m%d_%H%M%S).log"

exec >> "$LOG_FILE" 2>&1

echo "============================================================"
echo "⏰ Autonomous Daemon Triggered: $(date)"
echo "📂 Runtime Directory: $REPO_DIR"
echo "============================================================"

cd "$REPO_DIR"

# Source environment (.env defaults first, .env.local secrets/overrides second!)
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

if [ -f .env.local ]; then
    set -a
    source .env.local
    set +a
fi

export PYTHONPATH="$REPO_DIR"
export GOOGLE_APPLICATION_CREDENTIALS="$REPO_DIR/service-account.json"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Wait up to 90s for DNS/Wi-Fi readiness after macOS wake-from-sleep
echo "🌐 Checking network/DNS readiness..."
NET_READY=0
for attempt in $(seq 1 18); do
    if curl -sIf --max-time 5 https://oauth2.googleapis.com >/dev/null 2>&1 || curl -sI --max-time 5 https://www.googleapis.com >/dev/null 2>&1; then
        NET_READY=1
        break
    fi
    echo "   Waiting for network/DNS ($attempt/18)..."
    sleep 5
done

# Run production pipeline with AUTO track detection under caffeinate so Mac doesn't sleep mid-upload
# Before 12:00 PM IST = RAMAYANA (Morning Slot 7:00 AM IST)
# After 12:00 PM IST = MAHABHARATA (Evening Slot 6:30 PM IST)
echo "🚀 Executing Autonomous Pipeline (Vertex T2V Locked, caffeinate enabled)..."
caffeinate -i -s "$REPO_DIR/backend/.venv/bin/python" "$REPO_DIR/scripts/run_pipeline.py" --format SHORT --track AUTO "$@"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Pipeline completed and published successfully!"
    osascript -e 'display notification "Episode produced and published cleanly!" with title "Itihasa Saga Autonomous Pipeline" sound name "Glass"' 2>/dev/null || true
else
    echo "❌ Pipeline failed with exit code $EXIT_CODE"
    osascript -e 'display notification "Episode production failed! Check daemon logs." with title "Itihasa Saga Autonomous Pipeline Error" sound name "Basso"' 2>/dev/null || true
fi

echo "🏁 Finished at $(date)"
exit $EXIT_CODE
