#!/bin/bash

# --- 1. CONFIGURATION ---
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"

ACTION="$1"
TARGET_URL="$2"
MISSION_NAME="$3"

# --- 2. ACTION: STRIKE ---
if [ "$ACTION" == "strike" ]; then
    echo ">> [INIT] LOCKING MISSION: $MISSION_NAME"
    echo ">> [TIME] $(date)"
    
    # --- PHASE 1: CEREBRO (SUBDOMAIN RECON) ---
    if [ "$RUN_P1" == "1" ]; then
        echo "--- PHASE 1: CEREBRO (RECON) ---"
        echo ">> Hunting Subdomains for: $TARGET_URL"
        $BIN_DIR/subfinder -d "$TARGET_URL" -silent > /tmp/subs.txt
        cat /tmp/subs.txt
    fi

    # --- PHASE 2: SHADOW (ALIVE HOST DISCOVERY) ---
    if [ "$RUN_P2" == "1" ]; then
        echo "--- PHASE 2: SHADOW (DISCOVERY) ---"
        if [ -f "/tmp/subs.txt" ]; then
            echo ">> Filtering Active Hosts..."
            cat /tmp/subs.txt | $BIN_DIR/httpx -silent -sc -title -ip > /tmp/alive.txt
            cat /tmp/alive.txt
        else
            echo "$TARGET_URL" | $BIN_DIR/httpx -silent -sc -title -ip > /tmp/alive.txt
            cat /tmp/alive.txt
        fi
    fi

    # --- PHASE 3: HOOK (PORT & SERVICE SCAN) ---
    if [ "$RUN_P3" == "1" ]; then
        echo "--- PHASE 3: HOOK (SERVICE MAPPING) ---"
        # Using httpx to probe common web ports if subfinder found targets
        TARGET_SOURCE=${1:-"/tmp/subs.txt"}
        if [ -f "$TARGET_SOURCE" ]; then
             cat "$TARGET_SOURCE" | $BIN_DIR/httpx -p 80,443,8080,8443,9000 -silent -web-server
        else
             echo "$TARGET_URL" | $BIN_DIR/httpx -p 80,443,8080,8443,9000 -silent -web-server
        fi
    fi

    # --- PHASE 4: STRIKE (VULNERABILITY SCAN) ---
    if [ "$RUN_P4" == "1" ]; then
        echo "--- PHASE 4: STRIKE (VULN SCAN) ---"
        echo ">> Launching Nuclei Engine..."
        # If we have alive hosts from P2, scan those. Otherwise, scan the root.
        if [ -f "/tmp/alive.txt" ]; then
            cat /tmp/alive.txt | awk '{print $1}' | $BIN_DIR/nuclei -silent -severity critical,high,medium
        else
            echo "$TARGET_URL" | $BIN_DIR/nuclei -silent -severity critical,high,medium
        fi
    fi

    # --- PHASE 5: ARCHITECT (AI AGENT & REPO AUDIT) ---
    if [ "$RUN_P5" == "1" ]; then
        echo "--- PHASE 5: ARCHITECT (AI AGENT AUDIT) ---"
        if [ -n "$GH_REPO" ]; then
            echo ">> Auditing Repository: $GH_REPO"
            $BIN_DIR/nuclei -u "$GH_REPO" -silent -tags exposures,tokens,keys,misconfig -severity critical,high,medium
        else
            echo "[SKIP] Phase 5 Active but no GitHub Repo URL provided."
        fi
    fi

    # Cleanup temporary session files
    rm -f /tmp/subs.txt /tmp/alive.txt
    echo "--- [SUCCESS] MISSION COMPLETE: $MISSION_NAME ---"
    exit 0
fi
