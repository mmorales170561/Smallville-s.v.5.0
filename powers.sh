#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET_URL="$2"; MISSION_NAME="$3"

# Stealth Settings
if [ "$RUN_STEALTH" == "1" ]; then
    RL_LIMIT="-rl 5 -c 2"
    KATANA_LIMIT="-f qurl -strategy depth -p 2 -rl 5"
else
    RL_LIMIT="-c 50"
    KATANA_LIMIT=""
fi

if [ "$ACTION" == "strike" ]; then
    echo ">> [LOCK] MISSION: $MISSION_NAME | TARGET: $TARGET_URL"
    
    # --- PHASE 0: DEPENDENCY CHECK ---
    echo ">> [PHASE 0] ARMORY STATUS CHECK:"
    for tool in subfinder httpx katana nuclei airix; do
        if command -v $tool >/dev/null 2>&1; then
            echo "   [✓] $tool: READY"
        else
            echo "   [✗] $tool: MISSING"
        fi
    done
    echo "----------------------------------------"

    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Hunt..."
        subfinder -d "$TARGET_URL" -silent > /tmp/subs.txt
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Discovery..."
        [[ -f "/tmp/subs.txt" ]] && SOURCE="/tmp/subs.txt" || SOURCE="$TARGET_URL"
        cat "$SOURCE" | httpx $RL_LIMIT -silent -sc -td -ip > /tmp/alive.txt
        cat /tmp/alive.txt
    fi

    # --- P3: KATANA ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Deep Crawling..."
        # Check if katana exists before running to avoid crash
        if command -v katana >/dev/null 2>&1; then
            cat /tmp/alive.txt | awk '{print $1}' | katana $KATANA_LIMIT -silent -jc -kf all > /tmp/endpoints.txt
            echo ">> Endpoints discovered: $(wc -l < /tmp/endpoints.txt)"
        fi
    fi

    # --- P4: STRIKE ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        # Fixed syntax: Nuclei handles OOB automatically now
        [[ -f "/tmp/endpoints.txt" ]] && STRIKE_SOURCE="/tmp/endpoints.txt" || STRIKE_SOURCE="/tmp/alive.txt"
        cat "$STRIKE_SOURCE" | nuclei $RL_LIMIT -silent -severity critical,high,medium
    fi

    # --- P6: OLYMPUS ---
    if [ "$RUN_P6" == "1" ]; then
        echo ">> [PHASE 6] OLYMPUS: AI Fuzzing..."
        if command -v airix >/dev/null 2>&1; then
            cat /tmp/endpoints.txt | grep -E "api|v1|chat|ai" | airix -silent
        fi
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/subs.txt /tmp/alive.txt /tmp/endpoints.txt
    exit 0
fi
