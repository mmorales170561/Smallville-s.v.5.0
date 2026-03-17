#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET_URL="$2"; MISSION_NAME="$3"

# Cleanup Old Temp Data for Chromebook Storage (2GB Limit)
rm -f /tmp/raw_subs.txt /tmp/subs.txt /tmp/alive.txt /tmp/endpoints.txt

if [ "$ACTION" == "strike" ]; then
    echo ">> [LOCK] MISSION: $MISSION_NAME | TARGET: $TARGET_URL"
    
    # --- P0: DEPENDENCY CHECK ---
    echo ">> [PHASE 0] ARMORY STATUS CHECK:"
    for tool in subfinder httpx katana nuclei airix; do
        if command -v $tool >/dev/null 2>&1; then echo "   [✓] $tool: READY"; else echo "   [✗] $tool: MISSING"; fi
    done
    echo "----------------------------------------"

    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Hunt..."
        subfinder -d "$TARGET_URL" -silent > /tmp/raw_subs.txt
        # Apply Out-of-Scope Filter
        if [ -n "$OUT_SCOPE" ]; then
            grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|')" /tmp/raw_subs.txt > /tmp/subs.txt
        else
            cp /tmp/raw_subs.txt /tmp/subs.txt
        fi
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Discovery..."
        cat /tmp/subs.txt | httpx -silent -sc -td -ip > /tmp/alive.txt
        cat /tmp/alive.txt
    fi

    # --- P3: KATANA ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Crawling..."
        # If no subs found, use root URL
        [[ -s /tmp/alive.txt ]] && K_SRC="/tmp/alive.txt" || K_SRC="$TARGET_URL"
        cat "$K_SRC" | katana -silent -jc -kf all > /tmp/endpoints.txt
        echo ">> Found $(wc -l < /tmp/endpoints.txt) endpoints."
    fi

    # --- P4: STRIKE ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        [[ -s /tmp/endpoints.txt ]] && S_SRC="/tmp/endpoints.txt" || S_SRC="/tmp/alive.txt"
        cat "$S_SRC" | nuclei -silent -severity critical,high,medium
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
fi
