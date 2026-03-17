#!/bin/bash
BIN_DIR="/tmp/bin"
export PATH=$PATH:$BIN_DIR

# --- DEBUG REDIRECTION ---
# If DEBUG=1, we show stderr. If 0, we hide it.
[[ "$DEBUG" == "1" ]] && ERR_OUT="/dev/stderr" || ERR_OUT="/dev/null"

case "$1" in
    strike)
        echo ">> [INIT] LOCKING SEQUENCE FOR: $3"
        
        # 0. SCOPE PREP
        CLEAN_IN=$(echo "$IN_SCOPE" | tr ',' '\n' | tr ' ' '\n' | grep -v "^$")
        RAW_LIST=$( (echo "$2"; echo "$CLEAN_IN") | sort -u | grep -v "^$" )
        CLEAN_OUT=$(echo "$OUT_SCOPE" | tr ',' '\n' | tr ' ' '\n' | grep -v "^$")
        [[ -n "$CLEAN_OUT" ]] && PATTERN=$(echo "$CLEAN_OUT" | paste -sd "|" -) && FINAL_LIST=$(echo "$RAW_LIST" | grep -v -E "$PATTERN") || FINAL_LIST="$RAW_LIST"

        # PHASE 1: CEREBRO
        if [ "$RUN_P1" == "1" ]; then
            echo ">> [PHASE 1] SCARLET CEREBRO START..."
            # Using -v to ensure httpx waits for results
            echo "$FINAL_LIST" | $BIN_DIR/subfinder -silent 2>$ERR_OUT | $BIN_DIR/httpx -silent -title 2>$ERR_OUT
            echo ">> [PHASE 1] COMPLETE."
            sleep 1 # Hardware cool-down for Chromebook
        fi

        # PHASE 2: SHADOW
        if [ "$RUN_P2" == "1" ]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE START..."
            echo "$FINAL_LIST" | $BIN_DIR/gau --subs --threads 5 2>$ERR_OUT | head -n 10
            echo ">> [PHASE 2] COMPLETE."
            sleep 1
        fi

        # PHASE 3: HOOK
        if [ "$RUN_P3" == "1" ]; then
            echo ">> [PHASE 3] GRAPPLING HOOK START..."
            [[ "$PORT_PROFILE" == "Top 20 (Ghost)" ]] && P_VAL="-p 80,443,8080,8443,22,21" || P_VAL="-tp 100"
            echo "$FINAL_LIST" | $BIN_DIR/naabu $P_VAL -silent -unprivileged -rate 300 2>$ERR_OUT
            echo ">> [PHASE 3] COMPLETE."
            sleep 1
        fi

        # PHASE 4: STRIKE
        if [ "$RUN_P4" == "1" ]; then
            echo ">> [PHASE 4] RED KRYPTONITE STRIKE START..."
            # Force httpx to verify live hosts again before Nuclei fires
            LIVE=$(echo "$FINAL_LIST" | $BIN_DIR/httpx -silent 2>$ERR_OUT)
            if [ -n "$LIVE" ]; then
                echo "$LIVE" | $BIN_DIR/nuclei -silent -ni -severity critical,high 2>$ERR_OUT
            else
                echo ">> [!] NO LIVE ASSETS FOR PHASE 4."
            fi
            echo ">> [PHASE 4] COMPLETE."
        fi

        echo ">> [MISSION FINISHED] DATA SAVED TO LEDGER."
        ;;
esac
