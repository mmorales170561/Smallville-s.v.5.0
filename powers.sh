#!/bin/bash
BIN_DIR="/tmp/bin"
export PATH=$PATH:$BIN_DIR
[[ "$DEBUG" == "1" ]] && ERR_OUT="/dev/stderr" || ERR_OUT="/dev/null"

case "$1" in
    prime)
        echo ">> [ARMORY] FETCHING WEAPONS..."
        # Add your wget/unpack logic here for nuclei, subfinder, httpx, naabu, gau, mantra
        ;;
    strike)
        # 1. SCOPE CLEANING
        CLEAN_IN=$(echo "$IN_SCOPE" | tr ',' '\n' | tr ' ' '\n' | grep -v "^$")
        RAW_LIST=$( (echo "$2"; echo "$CLEAN_IN") | sort -u | grep -v "^$" )
        CLEAN_OUT=$(echo "$OUT_SCOPE" | tr ',' '\n' | tr ' ' '\n' | grep -v "^$")
        [[ -n "$CLEAN_OUT" ]] && PATTERN=$(echo "$CLEAN_OUT" | paste -sd "|" -) && FINAL_LIST=$(echo "$RAW_LIST" | grep -v -E "$PATTERN") || FINAL_LIST="$RAW_LIST"

        # PHASE 1: CEREBRO
        if [ "$RUN_P1" == "1" ]; then
            echo ">> [PHASE 1] SCARLET CEREBRO START..."
            echo "$FINAL_LIST" | $BIN_DIR/subfinder -silent 2>$ERR_OUT | $BIN_DIR/httpx -silent -title 2>$ERR_OUT
            sleep 1
        fi

        # PHASE 2: SHADOW
        if [ "$RUN_P2" == "1" ]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE START..."
            echo "$FINAL_LIST" | $BIN_DIR/gau --subs --threads 5 2>$ERR_OUT | head -n 10
            sleep 1
        fi

        # PHASE 3: HOOK (FIXED FOR CHROMEBOOK)
        if [ "$RUN_P3" == "1" ]; then
            echo ">> [PHASE 3] GRAPPLING HOOK START..."
            [[ "$PORT_PROFILE" == "Top 20 (Ghost)" ]] && P_VAL="-p 80,443,8080,8443,22,21" || P_VAL="-tp 100"
            # Using -s c (Connect Scan) to bypass privileged socket errors
            echo "$FINAL_LIST" | $BIN_DIR/naabu $P_VAL -s c -silent -rate 300 2>$ERR_OUT
            sleep 1
        fi

        # PHASE 4: STRIKE
        if [ "$RUN_P4" == "1" ]; then
            echo ">> [PHASE 4] RED KRYPTONITE STRIKE START..."
            LIVE=$(echo "$FINAL_LIST" | $BIN_DIR/httpx -silent 2>$ERR_OUT)
            if [ -n "$LIVE" ]; then
                echo "$LIVE" | $BIN_DIR/nuclei -silent -ni -severity critical,high 2>$ERR_OUT
                echo "$LIVE" | $BIN_DIR/mantra -silent 2>$ERR_OUT
            fi
        fi
        echo ">> [MISSION FINISHED] LOGS EXPORTED."
        ;;
esac
