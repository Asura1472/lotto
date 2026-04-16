#!/bin/sh
set -e

REPO_DIR="$HOME/git/lotto"
LOG_FILE="$REPO_DIR/update.log"

cd "$REPO_DIR"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') START =====" >> "$LOG_FILE"

git pull origin main >> "$LOG_FILE" 2>&1
python3 update_lotto.py >> "$LOG_FILE" 2>&1

git add all.json latest.json

if ! git diff --cached --quiet; then
    git commit -m "Update lotto JSON" >> "$LOG_FILE" 2>&1
    git push origin main >> "$LOG_FILE" 2>&1
    echo "Pushed changes." >> "$LOG_FILE"
else
    echo "No changes to commit." >> "$LOG_FILE"
fi

echo "===== END =====" >> "$LOG_FILE"
