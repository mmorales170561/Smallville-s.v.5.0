#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- 1. STORAGE & PERMS CHECK ---
if [ "$ACTION" == "strike" ]; then
    echo "--- MISSION START: $MISSION ---"
    echo ">> [PHASE 0] ARMORY STATUS CHECK:"
    
    # Check if tools exist and are executable
    for tool in subfinder httpx katana nuclei airix; do
        if command -v $tool >/dev/null 2>&1; then
            echo "   [✓] $tool: READY"
        else
            echo "   [✗] $tool: MISSING OR NOT EXECUTABLE"
        fi
    done
    echo "----------------------------------------"

    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Hunt..."
        subfinder -d "$TARGET" -silent > /tmp/raw_subs.txt
        # Apply Out-of-Scope Filter
        if [ -n "$OUT_SCOPE" ]; then
            grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|')" /tmp/raw_subs.txt > /tmp/subs.txt
        else
            cp /tmp/raw_subs.txt /tmp/subs.txt
        fi
        echo ">> Targets in Scope: $(wc -l < /tmp/subs.txt)"
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Discovery..."
        # If P1 was skipped or failed, use root target
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="$TARGET"
        cat "$SRC" | httpx -silent -sc -td -ip > /tmp/alive.txt
        cat /tmp/alive.txt
    fi

    # --- P3: KATANA ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Deep Crawling..."
        [[ -s /tmp/alive.txt ]] && KSRC="/tmp/alive.txt" || KSRC="$TARGET"
        # Using a limited crawl for Chromebook performance
        cat "$KSRC" | awk '{print $1}' | katana -silent -jc -kf all -d 2 > /tmp/endpoints.txt
        echo ">> Endpoints discovered: $(wc -l < /tmp/endpoints.txt)"
    fi

    # --- P4: STRIKE ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        [[ -s /tmp/endpoints.txt ]] && SSRC="/tmp/endpoints.txt" || SSRC="/tmp/alive.txt"
        cat "$SSRC" | nuclei -silent -severity critical,high,medium
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    # Storage Safety Cleanup
    rm -f /tmp/raw_subs.txt /tmp/subs.txt /tmp/alive.txt /tmp/endpoints.txt
fi
