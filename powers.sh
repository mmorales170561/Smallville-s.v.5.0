#!/bin/bash

# --- 1. CONFIGURATION ---
# We use the deep-write directory to bypass Streamlit permission locks
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"

ACTION="$1"
TARGET_URL="$2"
MISSION_NAME="$3"

# --- 2. ACTION: STRIKE ---
if [ "$ACTION" == "strike" ]; then
    echo ">> [INIT] LOCKING MISSION: $MISSION_NAME"
    echo ">> [TIME] $(date)"
    
    # Verify Armory before firing
    if [[ ! -f "$BIN_DIR/subfinder" ]]; then
        echo "[ERROR] Armory Empty. Please click 'PRIME ELITE TOOLS' in the sidebar."
        exit 1
    fi

    # --- PHASE 1: CEREBRO (RECON) ---
    if [ "$RUN_P1" == "1" ]; then
        echo "--- PHASE 1: CEREBRO (RECON) ---"
        echo ">> Hunting Subdomains for: $TARGET_URL"
        $BIN_DIR/subfinder -d "$TARGET_URL" -silent | $BIN_DIR/httpx -silent -title -sc -ip
    fi

    # --- PHASE 4: STRIKE (VULN SCAN) ---
    if [ "$RUN_P4" == "1" ]; then
        echo "--- PHASE 4: STRIKE (VULN SCAN) ---"
        echo ">> Scanning Target: $TARGET_URL"
        echo "$TARGET_URL" | $BIN_DIR/nuclei -silent -severity critical,high,medium
    fi

    # --- PHASE 5: ARCHITECT (AI AGENT & REPO AUDIT) ---
    if [ "$RUN_P5" == "1" ]; then
        echo "--- PHASE 5: ARCHITECT (AI AGENT AUDIT) ---"
        if [ -n "$GH_REPO" ]; then
            echo ">> Target Repository: $GH_REPO"
            echo ">> Checking for AI Agent Logic Bugs & Token Exposures..."
            
            # Using Nuclei with specific tags for AI/LLM exposures and misconfigs
            $BIN_DIR/nuclei -u "$GH_REPO" -silent \
                -tags exposures,tokens,keys,misconfig,python,javascript \
                -severity critical,high,medium
        else
            echo "[SKIP] Phase 5 Active but no GitHub Repo URL provided."
        fi
    fi

    echo "--- MISSION COMPLETE ---"
    exit 0

# --- 3. ACTION: PRIME (BACKUP LOGIC) ---
elif [ "$ACTION" == "prime" ]; then
    # Note: Primary priming is handled by app.py (Python) to bypass 404s
    echo ">> Manual Prime Check: $(ls $BIN_DIR)"
    exit 0
fi
