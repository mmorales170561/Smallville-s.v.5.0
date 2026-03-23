#!/bin/bash
# --- 1. PATHS & VARS ---
BIN_DIR="$HOME/.smallville_bin"
SUBFINDER="$BIN_DIR/subfinder"; HTTPX="$BIN_DIR/httpx"
KATANA="$BIN_DIR/katana"; NUCLEI="$BIN_DIR/nuclei"
SHOT_DIR="/tmp/screenshots"
ACTION="$1"; TARGET="$2"

# --- 2. HEADERS ---
mkdir -p "$SHOT_DIR"
H1_HEADER="X-Bug-Bounty: HackerOne-$H1_USER"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0"
GLOBAL_ARGS="-H '$H1_HEADER' -H 'User-Agent: $UA'"

if [ "$ACTION" == "strike" ]; then
    echo ">> [OVERLORD] INITIALIZING APEX ATTACK SURFACE..."
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' > /tmp/targets.txt

    # --- PHASE 1: RECON ---
    if [ "$RUN_P1" == "1" ]; then
        echo ">> [P1] CEREBRO: Finding Subdomains..."
        $SUBFINDER -list /tmp/targets.txt -silent > /tmp/all_subs.txt
    fi

    # --- PHASE 3: HEADLESS + AI HUNT ---
    if [ "$RUN_P3" == "1" ]; then
        echo ">> [P3] KATANA: Headless Crawl & AI Endpoint Discovery..."
        $KATANA -list /tmp/all_subs.txt -headless -system-chrome -jc -silent -ss -sd "$SHOT_DIR" $GLOBAL_ARGS > /tmp/endpoints.txt
        # Extracting AI/Web3 secrets
        grep -E "sk_live|AIza|infura|alchemy|rpc" /tmp/endpoints.txt >> /tmp/leaked_secrets.txt
    fi

    # --- PHASE 4: TAKEOVER & WEB3 ---
    if [ "$RUN_P4" == "1" ] || [ "$RUN_STO" == "1" ]; then
        echo ">> [P4/STO] STRIKE: Hunting for Takeovers & RPC Leaks..."
        $NUCLEI -l /tmp/all_subs.txt -silent -severity critical -t takeovers/ -t dns/dangling-dns.yaml $GLOBAL_ARGS | while read -r line; do
            DOMAIN=$(echo "$line" | awk '{print $NF}' | sed 's/[()]//g')
            CNAME=$(dig +short $DOMAIN CNAME)
            echo "[takeover] VERIFIED: $line | CNAME: $CNAME"
        done
    fi

    # --- PHASE 7/8: AI & WEB3 VALIDATION ---
    if [ "$RUN_P8" == "1" ]; then
        echo ">> [P8] WEB3: Validating RPC Node Access..."
        grep "rpc" /tmp/endpoints.txt | while read -r rpc; do
            res=$(curl -s -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}' "$rpc")
            [[ $res == *"jsonrpc"* ]] && echo "[critical] WEB3: Active RPC Node Found at $rpc"
        done
    fi

    echo ">> [SUCCESS] MISSION COMPLETE. DATA STAGED."
fi
