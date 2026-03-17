#!/bin/bash
# --- SMALLVILLE S.V. 5.0 ENGINE ---
# Optimized for Chromebook/Crostini Linux

BIN_DIR="/tmp/bin"
export PATH=$PATH:$BIN_DIR

# --- DEBUG & OUTPUT ROUTING ---
# If DEBUG=1 (set from app.py), we show errors. Otherwise, we hide noise.
[[ "$DEBUG" == "1" ]] && ERR_OUT="/dev/stderr" || ERR_OUT="/dev/null"

case "$1" in
    prime)
        echo ">> [ARMORY] INITIALIZING WEAPON CACHE..."
        # This section ensures all binaries are executable
        chmod +x $BIN_DIR/* 2>/dev/null
        echo ">> [ARMORY] SYSTEMS CALIBRATED."
        ;;

    strike)
        TARGET_DOMAIN="$2"
        MISSION_NAME="$3"
        
        echo ">> [INIT] LOCKING SEQUENCE FOR MISSION: $MISSION_NAME"
        
        # --- 0. SCOPE CLEANING & DEDUPLICATION ---
        # Cleans up the input from the Streamlit text areas
        CLEAN_IN=$(echo "$IN_SCOPE" | tr ',' '\n' | tr ' ' '\n' | grep -v "^$")
        RAW_LIST=$( (echo "$TARGET_DOMAIN"; echo "$CLEAN_IN") | sort -u | grep -v "^$" )
        
        CLEAN_OUT=$(echo "$OUT_SCOPE" | tr ',' '\n' | tr ' ' '\n' | grep -v "^$")
        if [ -n "$CLEAN_OUT" ]; then
            PATTERN=$(echo "$CLEAN_OUT" | paste -sd "|" -)
            FINAL_LIST=$(echo "$RAW_LIST" | grep -v -E "$PATTERN")
        else
            FINAL_LIST="$RAW_LIST"
        fi

        # --- PHASE 1: SCARLET CEREBRO (Passive Recon) ---
        if [ "$RUN_P1" == "1" ]; then
            echo ">> [PHASE 1] SCARLET CEREBRO START..."
            # Subfinder for subdomains -> httpx for live web servers
            echo "$FINAL_LIST" | subfinder -silent 2>$ERR_OUT | httpx -silent -title 2>$ERR_OUT
            echo ">> [PHASE 1] COMPLETE."
            sleep 1
        fi

        # --- PHASE 2: SHADOW ARCHIVE (URL Discovery) ---
        if [ "$RUN_P2" == "1" ]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE START..."
            # gau fetches historical URLs from WayBack, AlienVault, etc.
            echo "$FINAL_LIST" | gau --subs --threads 5 2>$ERR_OUT | head -n
