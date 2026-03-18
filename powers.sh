#!/bin/bash
# --- 1. HARD PATHS ---
BIN_DIR="/tmp/smallville_bin"
SUBFINDER="$BIN_DIR/subfinder"; HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"; NUCLEI="$BIN_DIR/nuclei"

ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 2. COMPLIANCE & STEALTH ---
H1_HEADER="X-Bug-Bounty: HackerOne-$H1_USER"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
GLOBAL_HEADERS="-H '$H1_HEADER' -H 'User-Agent: $UA' -H 'X-Forwarded-For: 127.0.0.1'"

[[ "$RUN_STEALTH" == "1" ]] && RL="-rl 1 -c 1 -mhe 100 $GLOBAL_HEADERS" || RL="-c 20 $GLOBAL_HEADERS"

if [ "$ACTION" == "strike" ]; then
    echo ">> [SYSTEM] INITIALIZING AEGIS-VALIDATED EXECUTION..."
    echo ">> [!] Compliance Header: $H1_HEADER"
    
    # --- PHASE 0: THE AEGIS VALIDATOR ---
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' | grep "." > /tmp/raw_targets.txt
    
    if [ -n "$OUT_SCOPE_LIST" ]; then
        # Convert comma-list to grep pattern
        PATTERN=$(echo "$OUT_SCOPE_LIST" | tr ',' '|')
        grep -v -E "$PATTERN" /tmp/raw_targets.txt > /tmp/target_list.txt
        REMOVED=$(($(wc -l < /tmp/raw_targets.txt) - $(wc -l < /tmp/target_list.txt)))
        [[ $REMOVED -gt 0 ]] && echo ">> [!] AEGIS: Blocked $REMOVED out-of-scope targets."
    else
        cp /tmp/raw_targets.txt /tmp/target_list.txt
    fi
    echo "----------------------------------------"

    # --- PHASE 2: SHADOW (Httpx) ---
    if [ "$RUN_P2" == "1" ] && [ -f "$HTTPX" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Targets..."
        # We always check the Aegis-cleaned list
        $HTTPX -l /tmp/target_list.txt -silent -sc -td -ip $GLOBAL_HEADERS -retries 2 > /tmp/alive.txt
        
        if [ ! -s /tmp/alive.txt ]; then
            echo "   [!] WAF Block. Forcing Shadow Injection..."
            while read -r line; do echo "https://$line" >> /tmp/alive.txt; done < /tmp/target_list.txt
        fi
        echo "   [✓] $(wc -l < /tmp/alive.txt) hosts ready."
    fi

    # --- PHASE 4: STRIKE (Nuclei) ---
    if [ "$RUN_P4" == "1" ] && [ -f "$NUCLEI" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        $NUCLEI -l /tmp/alive.txt $RL -silent -severity critical,high,medium
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
fi
