#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK:"
    for tool in subfinder httpx katana nuclei; do
        command -v $tool >/dev/null 2>&1 && echo "   [✓] $tool READY" || echo "   [✗] $tool MISSING"
    done
    echo "----------------------------------------"

    # P1: CEREBRO (Recon)
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        subfinder -d "$TARGET" -silent > /tmp/raw.txt
        if [ -n "$OUT_SCOPE" ]; then
            grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|')" /tmp/raw.txt > /tmp/subs.txt
        else
            cp /tmp/raw.txt /tmp/subs.txt
        fi
        echo ">> Found $(wc -l < /tmp/subs.txt) subdomains."
    fi

    # P2: SHADOW (Alive)
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Hosts..."
        [[ -s /tmp/subs.txt ]] && cat /tmp/subs.txt | httpx -silent > /tmp/alive.txt || echo "$TARGET" | httpx -silent > /tmp/alive.txt
        cat /tmp/alive.txt
    fi

    # P5: ARCHITECT (GitHub - Restore Point)
    if [ "$RUN_P5" == "1" ] && [ -n "$GH_REPO" ]; then
        echo ">> [PHASE 5] ARCHITECT: Auditing GitHub..."
        nuclei -u "$GH_REPO" -silent -tags tokens,keys,exposures
    fi

    echo "----------------------------------------"
    echo ">> MISSION COMPLETE."
fi
