#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET_URL="$2"; MISSION_NAME="$3"

if [ "$ACTION" == "strike" ]; then
    echo ">> [LOCK] MISSION: $MISSION_NAME | TARGET: $TARGET_URL"
    
    # --- P1: CEREBRO ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Hunt..."
        subfinder -d "$TARGET_URL" -silent > /tmp/subs.txt
    fi

    # --- P2: SHADOW ---
    if [ "$RUN_P2" == "1" ]; then
        echo ">> [PHASE 2] SHADOW: Discovery & Tech Detection..."
        cat /tmp/subs.txt | httpx -silent -sc -td -ip > /tmp/alive.txt
        cat /tmp/alive.txt
    fi

    # --- P3: KATANA (DEEP CRAWL & JS SCAN) ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [PHASE 3] KATANA: Crawling Endpoints & JS Secrets..."
        cat /tmp/alive.txt | awk '{print $1}' | katana -silent -jc -kf all -d 3 > /tmp/endpoints.txt
        echo ">> Endpoints found: $(wc -l < /tmp/endpoints.txt)"
    fi

    # --- P4: STRIKE (VULNS + INTERACTSH) ---
    if [ "$RUN_P4" == "1" ]; then
        echo ">> [PHASE 4] STRIKE: Nuclei + OOB Detection..."
        # Launch interactsh-client in background if needed for OOB
        cat /tmp/endpoints.txt | nuclei -silent -severity critical,high,medium -interactsh-url interact.sh
    fi

    # --- P5: ARCHITECT (AI REPO) ---
    if [ "$RUN_P5" == "1" ]; then
        echo ">> [PHASE 5] ARCHITECT: Auditing AI Agent Code..."
        [[ -n "$GH_REPO" ]] && nuclei -u "$GH_REPO" -silent -tags tokens,exposures,keys
    fi

    # --- P6: OLYMPUS (AI FUZZING) ---
    if [ "$RUN_P6" == "1" ]; then
        echo ">> [PHASE 6] OLYMPUS: LLM Prompt Injection Fuzzing..."
        # Airix targets AI endpoints found during Katana crawl
        cat /tmp/endpoints.txt | grep -E "api|v1|chat|ai" | airix -silent
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    # Storage Safety: Clean up large temp files but keep small logs
    rm -f /tmp/subs.txt /tmp/endpoints.txt
    exit 0
fi
