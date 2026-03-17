#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

if [ "$ACTION" == "strike" ]; then
    echo ">> [PHASE 0] ARMORY STATUS CHECK:"
    for tool in subfinder httpx katana nuclei; do
        command -v $tool >/dev/null 2>&1 && echo "   [✓] $tool READY" || echo "   [✗] $tool MISSING"
    done
    echo "----------------------------------------"

    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Hunting Subdomains..."
        subfinder -d "$TARGET" -silent > /tmp/raw.txt
        
        # Filter Out-of-Scope
        if [ -n "$OUT_SCOPE" ]; then
            grep -v -E "$(echo "$OUT_SCOPE" | tr '\n' '|')" /tmp/raw.txt > /tmp/subs.txt
        else
            cp /tmp/raw.txt /tmp/subs.txt
        fi
        
        SUB_COUNT=$(wc -l < /tmp/subs.txt)
        echo ">> Found $SUB_COUNT subdomains."
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Hosts..."
        # FAILOVER LOGIC: If subs.txt is empty, use the Target URL directly
        if [ ! -s /tmp/subs.txt ]; then
            echo ">> [!] No subdomains found. Pivoting to Root Target: $TARGET"
            echo "$TARGET" | httpx -silent -sc -td -ip > /tmp/alive.txt
        else
            cat /tmp/subs.txt | httpx -silent -sc -td -ip > /tmp/alive.txt
        fi
        cat /tmp/alive.txt
    fi

    # --- P3: KATANA ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Deep Crawling..."
        # Ensure we have something to crawl
        if [ -s /tmp/alive.txt ]; then
            cat /tmp/alive.txt | awk '{print $1}' | katana -silent -jc -kf all -d 2 > /tmp/endpoints.txt
            echo ">> Endpoints discovered: $(wc -l < /tmp/endpoints.txt)"
        else
            echo ">> [!] No alive hosts found to crawl."
        fi
    fi

    # --- P4: STRIKE ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Vulnerability Engine..."
        # Use endpoints if they exist, otherwise use alive hosts
        if [ -s /tmp/endpoints.txt ]; then
            cat /tmp/endpoints.txt | nuclei -silent -severity critical,high,medium
        elif [ -s /tmp/alive.txt ]; then
            echo ">> [!] No endpoints found. Running Nuclei on alive hosts..."
            cat /tmp/alive.txt | nuclei -silent -severity critical,high,medium
        fi
    fi

    # --- P5: ARCHITECT ---
    if [ "$RUN_P5" == "1" ] && [ -n "$GH_REPO" ]; then
        echo ">> [PHASE 5] ARCHITECT: Auditing GitHub..."
        nuclei -u "$GH_REPO" -silent -tags tokens,keys,exposures
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
fi
