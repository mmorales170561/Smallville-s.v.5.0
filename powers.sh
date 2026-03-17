#!/bin/bash

# --- CONFIG ---
export PATH="/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: STRIKE ---
if [ "$ACTION" == "strike" ]; then
    echo ">> [INIT] MISSION: $MISSION"
    
    # Verify tool location
    SUB="/tmp/bin/subfinder"
    HTP="/tmp/bin/httpx"
    NUC="/tmp/bin/nuclei"

    if [ "$RUN_P1" == "1" ]; then
        echo "--- PHASE 1: CEREBRO ---"
        $SUB -d "$TARGET" -silent | $HTP -silent
    fi

    if [ "$RUN_P4" == "1" ]; then
        echo "--- PHASE 4: STRIKE ---"
        echo "$TARGET" | $NUC -silent -severity critical,high
    fi

    echo ">> [COMPLETE] SUCCESS."
    exit 0
fi
