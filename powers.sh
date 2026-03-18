#!/bin/bash
# --- 1. HARD PATHS ---
BIN_DIR="/tmp/smallville_bin"
SUBFINDER="$BIN_DIR/subfinder"; HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"; NUCLEI="$BIN_DIR/nuclei"

ACTION="$1"; TARGET="$2"

# --- 2. COMPLIANCE & STEALTH ---
H1_HEADER="X-Bug-Bounty: HackerOne-$H1_USER"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
GLOBAL_HEADERS="-H '$H1_HEADER' -H 'User-Agent: $UA' -H 'X-Forwarded-For: 127.0.0.1'"

if [ "$RUN_STEALTH" == "1" ]; then
    RL="-rl 1 -c 1 -mhe 100 $GLOBAL_HEADERS"
    K_RL="-c 1 -d 2 -rl 1 -H '$H1_HEADER' -H 'User-Agent: $UA'"
else
    RL="-c 20 $GLOBAL_HEADERS"
    K_RL="-c 5 -H '$H1_HEADER' -H 'User-Agent: $UA'"
fi

if [ "$ACTION" == "strike" ]; then
    echo ">> [SYSTEM] INITIALIZING GHOST-PROTOCOL EXECUTION..."
    echo ">> [!] Identification: $H1_HEADER"
    
    # --- PHASE 0: AEGIS VALIDATOR ---
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' | grep "." > /tmp/raw_targets.txt
    if [ -n "$OUT_SCOPE_LIST" ]; then
        PATTERN=$(echo "$OUT_SCOPE_LIST" | tr ',' '|')
        grep -v -E "$PATTERN" /tmp/raw_targets.txt > /tmp/target_list.txt
    else
        cp /tmp/raw_targets.txt /tmp/target_list.txt
    fi
    echo "----------------------------------------"

    # --- PHASE 1: CEREBRO ---
    if [ "$RUN_P1" == "1" ] && [ -f "$SUBFINDER" ]; then
        echo ">> [PHASE 1] CEREBRO: Subdomain Hunt..."
        $SUBFINDER -list /tmp/target_list.txt -silent > /tmp/subs.txt
    fi

    # --- PHASE 2: SHADOW ---
    if [ "$RUN_P2" == "1" ] && [ -f "$HTTPX" ]; then
        echo ">> [PHASE 2] SHADOW: Resolving Targets..."
        [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
        $HTTPX -l "$SRC" -silent -sc -td -ip $GLOBAL_HEADERS -retries 2 > /tmp/alive.txt
        if [ ! -s /tmp/alive.txt ]; then
            echo "   [!] WAF Block. Injecting Shadow Targets..."
            while read -r line; do echo "https://$line" >> /tmp/alive.txt; done < /tmp/target_list.txt
        fi
        echo "   [✓] $(wc -l < /tmp/alive.txt) targets ready."
    fi

    # --- PHASE 3: KATANA ---
    if [ "$RUN_P3" == "1" ] && [ -f "$KATANA" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 3] KATANA: Mining Endpoints..."
        cat /tmp/alive.txt | $KATANA $K_RL -silent -jc -kf all > /tmp/endpoints.txt
    fi

    # --- PHASE 5: ARCHITECT (AI GitHub Intel) ---
    if [ "$RUN_P5" == "1" ]; then
        echo ">> [PHASE 5] ARCHITECT: Scanning GitHub for AI/LLM Leaks..."
        while read -r domain; do
            echo "   [LINK] https://github.com/search?q=%22$domain%22+ollama+OR+openai_key&type=code"
            echo "   [LINK] https://github.com/search?q=%22$domain%22+langchain+config&type=code"
        done < /tmp/target_list.txt
    fi

    # --- PHASE 4/6: STRIKE ---
    if [ "$RUN_P4" == "1" ] && [ -f "$NUCLEI" ] && [ -s /tmp/alive.txt ]; then
        echo ">> [PHASE 4/6] STRIKE: Vulnerability Engine..."
        $NUCLEI -l /tmp/alive.txt $RL -silent -severity critical,high,medium
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    rm -f /tmp/*.txt
fi
