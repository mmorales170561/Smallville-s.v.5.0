#!/bin/bash
# --- 1. HARD PATHS ---
BIN_DIR="/tmp/smallville_bin"
SUBFINDER="$BIN_DIR/subfinder"
HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"
NUCLEI="$BIN_DIR/nuclei"

ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 2. GHOST STEALTH SETTINGS ---
# We use a Chrome User-Agent and Jitter to bypass behavior-based WAFs
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

if [ "$RUN_STEALTH" == "1" ]; then
    # -rl (Rate Limit), -c (Concurrency), -je (Jitter)
    RL="-rl 5 -c 2 -je 0.2 -H 'User-Agent: $UA'"
    K_RL="-c 2 -p 2 -rl 5" # Katana specific stealth
else
    RL="-c 40 -H 'User-Agent: $UA'"
    K_RL="-c 10"
fi

# WAF Bypass Headers
WAF_HEADERS="-H 'X-Forwarded-For: 127.0.0.1' -H 'X-Real-IP: 127.0.0.1' -H 'X-Originating-IP: 127.0.0.1' -H 'Client-IP: 127.0.0.1'"

if [ "$ACTION" == "strike" ]; then
    echo ">> [SYSTEM] INITIALIZING GHOST-PROTOCOL EXECUTION..."
    
    # Clean and Prep Target List
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' > /tmp/target_list.txt
    touch /tmp/subs.txt /tmp/alive.txt /tmp/endpoints.txt /tmp/secrets.txt
    
    # Apply Out-Scope filter
    if [ -n "$OUT_SCOPE" ]; then
        grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|' | sed 's/|$//')" /tmp/target_list.txt > /tmp/clean_targets.txt
        mv /tmp/clean_targets.txt /tmp/target_list.txt
    fi
    echo "----------------------------------------"

    # --- PHASE 1: CEREBRO (Subdomains) ---
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

    # --- PHASE 2: SHADOW (Alive Check) ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Targets with WAF Bypass..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
        
        # Using HTTPX with multiple bypass headers
        cat "$SRC" | $HTTPX -silent -sc -td -ip $WAF_HEADERS -H "User-Agent: $UA" > /tmp/alive.txt
        
        # FORCE INJECTION: If blocked, force protocol URLs
        if [ ! -s /tmp/alive.txt ]; then
            echo "   [!] Resolution blocked. Forcing Protocol Injection..."
            while read -r line; do
                echo "https://$line" >> /tmp/alive.txt
                echo "http://$line" >> /tmp/alive.txt
            done < /tmp/target_list.txt
        fi
        echo "   [✓] $(wc -l < /tmp/alive.txt) hosts ready."
    fi

    # --- PHASE 3: KATANA (Deep Crawl) ---
    if [ "$RUN_P3" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 3] KATANA: Mining for Endpoints..."
        cat /tmp/alive.txt | $KATANA $K_RL -silent -jc -kf all -d 2 > /tmp/endpoints.txt
        
        # JS Secret Finder Logic
        grep -iE "(\.js|\.json|config|admin|api|v1|secret|token|key|env)" /tmp/endpoints.txt > /tmp/secrets.txt
        [[ -s /tmp/secrets.txt ]] && echo -e "   \033[0;31m[!] HIGH-VALUE PATHS IDENTIFIED\033[0m"
    fi

    # --- PHASE 4: STRIKE (Vulnerability Scan) ---
    if [ "$RUN_P4" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        cat /tmp/alive.txt /tmp/secrets.txt 2>/dev/null | sort -u > /tmp/final_strike.txt
        cat /tmp/final_strike.txt | $NUCLEI $RL -silent -severity critical,high,medium
    fi

    # --- PHASE 6: OLYMPUS (Heavy Fuzzing) ---
    if [ "$RUN_P6" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 6] OLYMPUS: Commencing Heavy Fuzzing..."
        cat /tmp/alive.txt | $NUCLEI $RL -silent -tags fuzz,sqli,xss,lfi -severity critical,high
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/*.txt
fi
