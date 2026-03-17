#!/bin/bash
BIN_DIR="/tmp/bin"
mkdir -p $BIN_DIR
export PATH=$PATH:$BIN_DIR

# --- [PRIME LOGIC OMITTED] ---

case "$1" in
    prime) prime_tools ;;
    strike)
        # 1. SCOPE PREPARATION
        FILTER_PATTERN=$(echo "$OUT_SCOPE" | sed 's/, /\\|/g' | sed 's/,/\\|/g')
        FULL_LIST=$( (echo "$2"; echo "$IN_SCOPE" | tr ',' '\n' | tr ' ' '\n') | sort -u | grep -v "^$" )
        [ -n "$FILTER_PATTERN" ] && FULL_LIST=$(echo "$FULL_LIST" | grep -v "$FILTER_PATTERN")

        echo ">> [PHASE 1] SCARLET CEREBRO: MAPPING..."
        RESULTS=$(echo "$FULL_LIST" | $BIN_DIR/subfinder -silent 2>/dev/null | $BIN_DIR/httpx -silent -title)
        echo "$RESULTS"

        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE..."
            echo "$FULL_LIST" | $BIN_DIR/gau --subs --threads 10 2>/dev/null | head -n 10
        fi

        if [[ "$PORTS" == "1" ]]; then
            echo ">> [PHASE 3] GRAPPLING HOOK..."
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu
            echo "$FULL_LIST" | $BIN_DIR/naabu -top-ports 20 -silent -rate 500 2>/dev/null
        fi

        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        VULNS=$(echo "$FULL_LIST" | $BIN_DIR/httpx -silent | $BIN_DIR/nuclei -silent -ni -severity critical)
        echo "$VULNS"

        # --- DATABASE INJECTION ---
        echo ">> [LOGGING] ARCHIVING MISSION DATA..."
        # Clean the results for the DB
        INTEL_SUMMARY=$(echo "$VULNS" | tr '\n' ' ' | sed "s/'//g" | cut -c1-250)
        
        python3 -c "
import sqlite3, datetime
conn = sqlite3.connect('red_kryptonite_ledger.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT)')
# Using the root target $2 for the entry
c.execute(\"INSERT INTO ledger (timestamp, target, intel) VALUES (?, ?, ?)\", 
          (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '$2', '$INTEL_SUMMARY' if '$INTEL_SUMMARY' else 'Scan Complete: No Crit Found'))
conn.commit()
conn.close()
"
        echo ">> [COMPLETE] MISSION LOGGED."
        ;;
esac
