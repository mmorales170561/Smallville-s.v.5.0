#!/bin/bash
# --- 1. HARD PATHS & TOOL CHECK ---
BIN_DIR="/tmp/smallville_bin"
SUBFINDER="$BIN_DIR/subfinder"
HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"
NUCLEI="$BIN_DIR/nuclei"

ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 2. SHADOW STEP STEALTH ---
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
WAF_HEADERS="-H 'X-Forwarded-For: 127.0.0.1' -H 'X-Real-IP: 127.0.0.1'"

if [ "$RUN_STEALTH" == "1" ]; then
    RL="-rl 1 -c 1 -mhe 100 -timeout 10 -H 'User-Agent: $UA'"
    K_RL="-c 1 -d 2 -rl 1" 
else
    RL="-c 20 -H 'User-Agent: $UA'"
    K_RL="-c 5"
fi

if [ "$ACTION" == "strike" ]; then
    echo ">> [SYSTEM] INITIALIZING BULLETPROOF EXECUTION..."
    
    # 3. SELF-HEALING TARGET PREP
    # We ensure the target list is created and PERSISTS
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' | grep "." > /tmp/target_list.txt
    
    if [ ! -s /tmp/target_list.txt ]; then
        echo ">> [!] ERROR: Target list is empty. Mission Aborted."
        exit 1
    fi
    echo "----------------------------------------"

    # --- PHASE 1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Hunt..."
        if [ -f "$SUBFINDER" ]; then
            $SUBFINDER -list /tmp/target_list.txt -silent > /tmp/subs.txt
        else
            echo "   [!] Subfinder missing. Skipping to Root."
        fi
    fi

    # --- PHASE 2: SHADOW (FIXED SYNTAX) ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Targets..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
        
        if [ -f "$HTTPX" ]; then
            # Fixed the variable call to ensure -silent isn't treated as a command
            $HTTPX -l "$SRC" -silent -sc -td -ip $WAF_HEADERS -retries 2 > /tmp/alive.txt
        fi
        
        # Fallback if httpx fails or is missing
        if [ ! -s /tmp/alive.txt ]; then
            echo "   [!] WAF/Path Block. Forcing Shadow Injection..."
            while read -r line; do
                echo "https://$line" >> /tmp/alive.txt
            done < /tmp/target_list.txt
        fi
        echo "   [✓] $(wc -l < /tmp/alive.txt) targets ready."
    fi

    # --- PHASE 4/6: STRIKE ---
    if [ -f "$NUCLEI" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 4/6] FIREPOWER: Vulnerability Engine..."
        # Running core scan
        $NUCLEI -l /tmp/alive.txt $RL -silent -severity critical,high,medium
    else
        echo ">> [!] Firepower skipped. Check Binaries or Targets."
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
fi
