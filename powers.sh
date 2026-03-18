#!/bin/bash
# --- 1. HARD PATHS ---
BIN_DIR="/tmp/smallville_bin"
SUBFINDER="$BIN_DIR/subfinder"
HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"
NUCLEI="$BIN_DIR/nuclei"

ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 2. STEALTH SETTINGS ---
[[ "$RUN_STEALTH" == "1" ]] && RL="-rl 7 -c 2" || RL="-c 50"

if [ "$ACTION" == "strike" ]; then
    echo ">> [SYSTEM] INITIALIZING PHASE-GATED EXECUTION..."
    
    # Clean and Prep Target List
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' > /tmp/target_list.txt
    touch /tmp/subs.txt /tmp/alive.txt /tmp/endpoints.txt /tmp/secrets.txt
    
    # Apply Out-Scope filter to initial targets
    if [ -n "$OUT_SCOPE" ]; then
        grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|' | sed 's/|$//')" /tmp/target_list.txt > /tmp/clean_targets.txt
        mv /tmp/clean_targets.txt /tmp/target_list.txt
    fi
    echo "----------------------------------------"

    # --- PHASE 1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        if [ "$FORCE_ROOT" == "1" ]; then
            echo "   [!] Skipping Subfinder (Force Root Active)."
        else
            while read -r domain; do
                $SUBFINDER -d "$domain" -silent >> /tmp/raw_subs.txt
            done < /tmp/target_list.txt
            sort -u /tmp/raw_subs.txt > /tmp/subs.txt
        fi
        [[ -s /tmp/subs.txt ]] && echo "   [✓] Found $(wc -l < /tmp/subs.txt) subdomains." || echo "   [!] No subdomains found. Using Root Fallback."
    fi

    # --- PHASE 2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Targets..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
        
        # WAF Bypass Header Injection
        cat "$SRC" | $HTTPX -silent -sc -td -ip -H "X-Forwarded-For: 127.0.0.1" -H "X-Originating-IP: 127.0.0.1" > /tmp/alive.txt
        
        # FORCE INJECTION: If httpx fails, force protocol URLs
        if [ ! -s /tmp/alive.txt ]; then
            echo "   [!] Resolution blocked. Forcing Protocol Injection..."
            while read -r line; do
                echo "https://$line" >> /tmp/alive.txt
                echo "http://$line" >> /tmp/alive.txt
            done < /tmp/target_list.txt
        fi
        echo "   [✓] $(wc -l < /tmp/alive.txt) hosts ready."
    fi

    # --- PHASE 3: KATANA ---
    if [ "$RUN_P3" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 3] KATANA: Mining for Endpoints..."
        cat /tmp/alive.txt | $KATANA -silent -jc -kf all -d 2 -c 5 > /tmp/endpoints.txt
        
        # JS Secret Finder
        grep -iE "(\.js|\.json|config|admin|api|v1|secret|token|key|env)" /tmp/endpoints.txt > /tmp/secrets.txt
        [[ -s /tmp/secrets.txt ]] && echo -e "   \033[0;31m[!] HIGH-VALUE PATHS IDENTIFIED\033[0m"
    fi

    # --- PHASE 4: STRIKE ---
    if [ "$RUN_P4" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        # Merge alive hosts and mined secrets for scanning
        cat /tmp/alive.txt /tmp/secrets.txt 2>/dev/null | sort -u > /tmp/final_strike.txt
        cat /tmp/final_strike.txt | $NUCLEI $RL -silent -severity critical,high,medium
    fi

    # --- PHASE 6: OLYMPUS ---
    if [ "$RUN_P6" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 6] OLYMPUS: Commencing Heavy Fuzzing..."
        cat /tmp/alive.txt | $NUCLEI $RL -silent -tags fuzz,sqli,xss,lfi -severity critical,high
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/*.txt
fi
