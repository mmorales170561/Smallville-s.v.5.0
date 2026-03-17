#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK..."
    # ... (Standard tool check)

    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ] && [ "$FORCE_ROOT" != "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        subfinder -d "$TARGET" -silent > /tmp/raw.txt
        
        # APPLY SCOPE RULES
        if [ -n "$OUT_SCOPE" ]; then
            echo ">> Applying Out-of-Scope Filters..."
            grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|' | sed 's/|$//')" /tmp/raw.txt > /tmp/subs.txt
        else
            cp /tmp/raw.txt /tmp/subs.txt
        fi
        echo ">> Targets remaining after Scope filter: $(wc -l < /tmp/subs.txt)"
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Alive Targets..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="$TARGET"
        echo "$SRC" | httpx -silent -sc -td -ip > /tmp/alive.txt
    fi

    # ... (Rest of P3, P4, and JS Secret Finder logic)
    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
fi
