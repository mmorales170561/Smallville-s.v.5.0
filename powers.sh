#!/bin/bash

# --- 1. CONFIGURATION ---
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"
TARGET_URL="$2"
MISSION_NAME="$3"

# --- 2. ACTION: STRIKE ---
if [ "$ACTION" == "strike" ]; then
    echo ">> [LOCK] MISSION: $MISSION_NAME"
    echo ">> [TARGET] $TARGET_URL"
    echo ">> [TIME] $(date)"
    echo "----------------------------------------"
    
    # --- PHASE 1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Reconnaissance..."
        $BIN_DIR/subfinder -d "$TARGET_URL" -silent > /tmp/subs.txt
        cat /tmp/subs.txt
    fi

    # --- PHASE 2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Live Host Discovery..."
        if [ -f "/tmp/subs.txt" ]; then
            cat /tmp/subs.txt | $BIN_DIR/httpx -silent -sc -title -ip > /tmp/alive.txt
        else
            echo "$TARGET_URL" | $BIN_DIR/httpx -silent -sc -title -ip > /tmp/alive.txt
        fi
        cat /tmp/alive.txt
    fi

    # --- PHASE 4: STRIKE ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        if [ -f "/tmp/alive.txt" ]; then
            cat /tmp/alive.txt | awk '{print $1}' | $BIN_DIR/nuclei -silent -severity critical,high,medium
        else
            echo "$TARGET_URL" | $BIN_DIR/nuclei -silent -severity critical,high,medium
        fi
    fi

    # --- PHASE 5: ARCHITECT ---
    if [ "$RUN_P5" == "1" ]; then
        echo ">> [PHASE 5] ARCHITECT: AI Agent Repo Audit..."
        if [ -n "$GH_REPO" ]; then
            echo ">> Repository: $GH_REPO"
            $BIN_DIR/nuclei -u "$GH_REPO" -silent -tags exposures,tokens,keys,misconfig -severity critical,high,medium
        else
            echo "[SKIP] No GitHub URL provided."
        fi
    fi

    echo "----------------------------------------"
    echo ">> [COMPLETE] MISSION SUCCESSFUL."
    rm -f /tmp/subs.txt /tmp/alive.txt
    exit 0
fi
