#!/bin/bash
# --- 1. SET HARD PATHS ---
BIN_DIR="/tmp/smallville_bin"

# Explicitly define tool locations to avoid "command not found"
SUBFINDER="$BIN_DIR/subfinder"
HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"
NUCLEI="$BIN_DIR/nuclei"

ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 2. STEALTH SETTINGS ---
if [ "$RUN_STEALTH" == "1" ]; then
    RL="-rl 5 -c 2"
else
    RL="-c 50"
fi

if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK..."
    
    # Verify binaries exist before trying to run them
    for tool in "$SUBFINDER" "$HTTPX" "$KATANA" "$NUCLEI"; do
        if [ ! -f "$tool" ]; then
            echo ">> [!] WARNING: $(basename $tool) not found in $BIN_DIR. Did you PRIME the armory?"
        else
            chmod +x "$tool"
        fi
    done

    # Convert TARGET string to line-by-line file
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' > /tmp/raw_targets.txt
    
    # Apply Scope Filters
    if [ -n "$OUT_SCOPE" ]; then
        grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|' | sed 's/|$//')" /tmp/raw_targets.txt > /tmp/target_list.txt
    else
        cp /tmp/raw_targets.txt /tmp/target_list.txt
    fi
    
    echo ">> Rules of Engagement Applied: $(wc -l < /tmp/target_list.txt) active targets."
    echo "----------------------------------------"

    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ] && [ "$FORCE_ROOT" != "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        while read -r domain; do
            $SUBFINDER -d "$domain" -silent >> /tmp/subfinder_out.txt
        done < /tmp/target_list.txt
        sort -u /tmp/subfinder_out.txt > /tmp/subs.txt
        echo ">> Subdomains found: $(wc -l < /tmp/subs.txt)"
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Hosts..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
        cat "$SRC" | $HTTPX -silent -sc -td -ip > /tmp/alive.txt
        echo ">> Alive hosts: $(wc -l < /tmp/alive.txt)"
    fi

    # --- P3: KATANA ---
    if [ "$RUN_P3" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 3] KATANA: Crawling Endpoints..."
        cat /tmp/alive.txt | awk '{print $1}' | $KATANA -silent -jc -kf all > /tmp/endpoints.txt
    fi

    # --- P4 & P6: STRIKE & OLYMPUS ---
    if [ "$RUN_P4" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        cat /tmp/alive.txt | $NUCLEI -silent -severity critical,high,medium
    fi

    if [ "$RUN_P6" == "1" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 6] OLYMPUS: Executing Heavy Strike..."
        cat /tmp/alive.txt | $NUCLEI -silent -tags fuzz,sqli,xss -severity critical,high
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/*.txt
fi
