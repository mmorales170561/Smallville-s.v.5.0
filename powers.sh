#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 1. STEALTH & RATE LIMITS ---
if [ "$RUN_STEALTH" == "1" ]; then
    RL_LIMIT="-rl 5 -c 2"
    K_LIMIT="-f qurl -strategy depth -p 2 -rl 5"
else
    RL_LIMIT="-c 50"
    K_LIMIT=""
fi

if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK:"
    for tool in subfinder httpx katana nuclei; do
        command -v $tool >/dev/null 2>&1 && echo "   [✓] $tool READY" || echo "   [✗] $tool MISSING"
    done
    echo "----------------------------------------"

    # --- P1 & P2: RECON & FAILOVER ---
    if [ "$FORCE_ROOT" == "1" ]; then
        echo ">> [!] FORCE ROOT ENABLED: Skipping Subfinder..."
        echo "$TARGET" | httpx -silent -sc -td -ip > /tmp/alive.txt
    else
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        subfinder -d "$TARGET" -silent > /tmp/raw.txt
        [[ -n "$OUT_SCOPE" ]] && grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|')" /tmp/raw.txt > /tmp/subs.txt || cp /tmp/raw.txt /tmp/subs.txt
        
        if [ -s /tmp/subs.txt ]; then
            cat /tmp/subs.txt | httpx -silent -sc -td -ip > /tmp/alive.txt
        else
            echo ">> [!] Subfinder 0. Pivoting to Root: $TARGET"
            echo "$TARGET" | httpx -silent -sc -td -ip > /tmp/alive.txt
        fi
    fi

    # --- P3: KATANA (The Miner) ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Mining Endpoints..."
        cat /tmp/alive.txt | awk '{print $1}' | katana $K_LIMIT -silent -jc -kf all > /tmp/endpoints.txt
        
        # --- NEW: JS SECRET FINDER ---
        echo ">> [ANALYSIS] SCANNING FOR SENSITIVE PATHS..."
        grep -iE "(\.js|\.json|\.env|\.xml|config|admin|auth|api|v1|v2|debug|test|dev|secret|password|key|token)" /tmp/endpoints.txt | sort -u > /tmp/secrets.txt
        
        if [ -s /tmp/secrets.txt ]; then
            echo -e "\033[0;31m>> HIGH-VALUE TARGETS IDENTIFIED:\033[0m"
            cat /tmp/secrets.txt | head -n 15 # Shows top 15 secrets in terminal
            echo ">> Total Secrets Mined: $(wc -l < /tmp/secrets.txt)"
        fi
    fi

    # --- P4: STRIKE (Heavy Artillery) ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        # If we found secrets, Nuclei should hit them first
        [[ -s /tmp/secrets.txt ]] && S_SRC="/tmp/secrets.txt" || S_SRC="/tmp/alive.txt"
        cat "$S_SRC" | nuclei $RL_LIMIT -silent -severity critical,high,medium
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/raw.txt /tmp/subs.txt /tmp/alive.txt /tmp/endpoints.txt /tmp/secrets.txt
fi
