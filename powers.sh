#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 1. STEALTH SETTINGS ---
if [ "$RUN_STEALTH" == "1" ]; then
    RL="-rl 5 -c 2"; K_LIMIT="-rl 5 -c 2"
else
    RL="-c 50"; K_LIMIT=""
fi

if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK..."
    # Sanitize TARGET list immediately
    echo "$TARGET" | tr ',' '\n' > /tmp/target_list.txt
    echo "----------------------------------------"

    # --- P1: CEREBRO (Subdomains) ---
    if [ "$RUN_P1" == "1" ] && [ "$FORCE_ROOT" != "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        # We loop through each target provided
        while read -r domain; do
            subfinder -d "$domain" -silent >> /tmp/raw_subs.txt
        done < /tmp/target_list.txt
        sort -u /tmp/raw_subs.txt > /tmp/subs.txt
        echo ">> Found $(wc -l < /tmp/subs.txt) subdomains."
    else
        echo ">> [PHASE 1] SKIPPED (Force Root active)."
    fi

    # --- P2: SHADOW (Alive Check) ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Alive Targets..."
        if [ -s /tmp/subs.txt ]; then
            cat /tmp/subs.txt | httpx -silent -sc -td -ip > /tmp/alive.txt
        else
            cat /tmp/target_list.txt | httpx -silent -sc -td -ip > /tmp/alive.txt
        fi
        echo ">> Alive hosts: $(wc -l < /tmp/alive.txt)"
    fi

    # --- P3: KATANA (Deep Crawl) ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Mining Endpoints..."
        cat /tmp/alive.txt | awk '{print $1}' | katana $K_LIMIT -silent -jc -kf all > /tmp/endpoints.txt
        echo ">> Endpoints discovered: $(wc -l < /tmp/endpoints.txt)"
    fi

    # --- P4: STRIKE (Standard Vuln) ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        [[ -s /tmp/endpoints.txt ]] && S_SRC="/tmp/endpoints.txt" || S_SRC="/tmp/alive.txt"
        cat "$S_SRC" | nuclei $RL -silent -severity critical,high,medium
    fi

    # --- P6: OLYMPUS (The Heavy Fuzz) ---
    if [ "$RUN_P6" == "1" ]; then
        echo ">> [PHASE 6] OLYMPUS: Executing Heavy Strike..."
        cat /tmp/alive.txt | nuclei $RL -silent -tags fuzz,sqli,xss,ssrf -severity critical,high
        echo ">> Scanning for Hidden Configs..."
        cat /tmp/alive.txt | nuclei $RL -silent -id backup-files,config-files,exposed-git,exposed-env
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/*.txt
fi
