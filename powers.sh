#!/bin/bash
# --- 1. PATHS ---
BIN_DIR="$HOME/.smallville_bin"
KATANA="$BIN_DIR/katana"; NUCLEI="$BIN_DIR/nuclei"
ACTION="$1"; TARGET="$2"

if [ "$ACTION" == "strike" ]; then
    echo ">> [OVERLORD] INITIATING MULTI-DOMAIN STRIKE..."
    
    # --- PHASE 1: WEB3 & FRONTEND RECON ---
    # Hunting for RSC (React Server Components) leaks used in Web3 frontends
    echo ">> [PHASE 1] Analyzing Web3 frontend architecture..."
    $NUCLEI -u "$TARGET" -silent -t http/vulnerabilities/react/ -t protocols/web3/
    
    # --- PHASE 2: AI AGENT PROBING ---
    # Using Katana to find 'hidden' AI endpoints and Chatbot APIs
    echo ">> [PHASE 2] Hunting for AI Agent Endpoints..."
    $KATANA -u "$TARGET" -headless -system-chrome -jc -em "ai,chat,agent,llm,openai,anthropic" -silent > /tmp/ai_endpoints.txt

    # --- PHASE 4: THE TAKEOVER (DNS & CLOUD) ---
    # Automatically verifying if the Web3 domain has dangling DNS
    $NUCLEI -l /tmp/targets.txt -silent -severity critical -t takeovers/ | while read -r line; do
        DOMAIN=$(echo "$line" | awk '{print $NF}' | sed 's/[()]//g')
        echo "[takeover] VERIFIED: $line | CNAME: $(dig +short $DOMAIN CNAME)"
    done
fi
