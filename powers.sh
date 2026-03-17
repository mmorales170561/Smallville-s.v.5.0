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
        [[ -f "/tmp/subs.txt" ]] && SOURCE="/tmp/subs.txt" || SOURCE="$TARGET_URL"
        cat "$SOURCE" | $BIN_DIR/httpx -silent -sc -title -ip > /tmp/alive.txt
        cat /tmp/alive.txt
    fi

    # --- PHASE 3: HOOK (HYBRID PROBE) ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] HOOK: Active Payload Probing..."
        AI_PORTS="80,443,5000,8000,8080,8501,11434"
        [[ -f "/tmp/subs.txt" ]] && SOURCE="/tmp/subs.txt" || SOURCE="$TARGET_URL"

        # 1. Map the Services
        cat "$SOURCE" | $BIN_DIR/httpx -p $AI_PORTS -silent -web-server -status-code -td > /tmp/ports.txt
        
        # 2. Probe for Website Misconfigs (.env, .git, .config)
        echo ">> Testing Website Integrity (Sensitive Files)..."
        cat "$SOURCE" | $BIN_DIR/httpx -path "/.env","/.git/config","/.vscode/sftp.json","/phpinfo.php" -silent -mc 200 -title
        
        # 3. Probe for AI Agent Exposure (FastAPI/Ollama/Streamlit)
        echo ">> Testing AI Agent Exposure (No-Auth Check)..."
        cat /tmp/ports.txt | awk '{print $1}' | $BIN_DIR/httpx -path "/api/tags","/docs","/v1/models","/health" -silent -mc 200 -td
        
        cat /tmp/ports.txt
    fi

    # --- PHASE 4: STRIKE ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        if [ -f "/tmp/ports.txt" ]; then
            cat /tmp/ports.txt | awk '{print $1}' | $BIN_DIR/nuclei -silent -severity critical,high,medium
        else
            echo "$TARGET_URL" | $BIN_DIR/nuclei -silent -severity critical,high,medium
        fi
    fi

    # --- PHASE 5: ARCHITECT ---
    if [ "$RUN_P5" == "1" ]; then
        echo ">> [PHASE 5] ARCHITECT: AI Agent Repo Audit..."
        if [ -n "$GH_REPO" ]; then
            $BIN_DIR/nuclei -u "$GH_REPO" -silent -tags exposures,tokens,keys,misconfig -severity critical,high,medium
        fi
    fi

    echo "----------------------------------------"
    echo ">> [COMPLETE] MISSION SUCCESSFUL."
    rm -f /tmp/subs.txt /tmp/alive.txt /tmp/ports.txt
    exit 0
fi
