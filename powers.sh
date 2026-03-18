#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 1. LOGIC GATES ---
if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK..."
    
    # Step A: Convert TARGET string to line-by-line file
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' > /tmp/raw_targets.txt
    
    # Step B: Apply Scope Filters (Simple Grep Logic)
    if [ -n "$OUT_SCOPE" ]; then
        grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|' | sed 's/|$//')" /tmp/raw_targets.txt > /tmp/target_list.txt
    else
        cp /tmp/raw_targets.txt /tmp/target_list.txt
    fi
    
    echo ">> Rules of Engagement Applied: $(wc -l < /tmp/target_list.txt) active targets."
    echo "----------------------------------------"

    # --- P1: CEREBRO (Recon) ---
    if [ "$RUN_P1" == "1" ] && [ "$FORCE_ROOT" != "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        while read -r domain; do
            subfinder -d "$domain" -silent >> /tmp/subfinder_out.txt
        done < /tmp/target_list.txt
        sort -u /tmp/subfinder_out.txt > /tmp/subs.txt
        echo ">> Subdomains found: $(wc -l < /tmp/subs.txt)"
    else
        echo ">> [PHASE 1] SKIPPED."
    fi

    # --- P2: SHADOW (Alive) ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Hosts..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
        cat "$SRC" | httpx -silent -sc -td -ip > /tmp/alive.txt
        echo ">> Alive hosts: $(wc -l < /tmp/alive.txt)"
    fi

    # --- P3: KATANA (Mining) ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Crawling Endpoints..."
        cat /tmp/alive.txt | awk '{print $1}' | katana -silent -jc -kf all > /tmp/endpoints.txt
    fi

    # --- P4 & P6: STRIKE & OLYMPUS (The Firepower) ---
    # Phase 4 handles standard Nuclei templates
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        cat /tmp/alive.txt | nuclei -silent -severity critical,high,medium
    fi

    # Phase 6 handles Fuzzing/Heavy payloads
    if [ "$RUN_P6" == "1" ]; then
        echo ">> [PHASE 6] OLYMPUS: Executing Heavy Strike..."
        cat /tmp/alive.txt | nuclei -silent -tags fuzz,sqli,xss -severity critical,high
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/*.txt
fi
