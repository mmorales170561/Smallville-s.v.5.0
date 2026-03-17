#!/bin/bash

# --- CONFIG ---
export PATH="/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: PRIME ---
if [ "$ACTION" == "prime" ]; then
    echo ">> [INIT] ARMING SYSTEMS IN /tmp/bin (DIRECT-SCRIPT MODE)..."
    mkdir -p /tmp/bin
    cd /tmp/bin
    
    # 1. Install Subfinder via official script
    echo ">> Installing Subfinder..."
    curl -sL https://raw.githubusercontent.com/projectdiscovery/subfinder/main/install.sh | bash
    mv /tmp/bin/subfinder /tmp/bin/subfinder_tmp 2>/dev/null || true
    
    # 2. Install HTTPX via official script
    echo ">> Installing HTTPX..."
    curl -sL https://raw.githubusercontent.com/projectdiscovery/httpx/main/install.sh | bash

    # 3. Install Nuclei via official script
    echo ">> Installing Nuclei..."
    curl -sL https://raw.githubusercontent.com/projectdiscovery/nuclei/main/install.sh | bash

    # 4. Final Permission Strike
    chmod +x /tmp/bin/*
    echo ">> [COMPLETE] ARMORY VERIFIED: $(ls /tmp/bin | grep -E 'subfinder|httpx|nuclei' | tr '\n' ' ')"
    exit 0

# --- ACTION: STRIKE ---
elif [ "$ACTION" == "strike" ]; then
    if [[ ! -f "/tmp/bin/subfinder" ]] && [[ ! -f "/usr/local/bin/subfinder" ]]; then
        echo "[ERROR] Armory Empty. Run PRIME first."
        exit 1
    fi
    
    echo "--- PHASE 1: CEREBRO (RECON) ---"
    # Using 'command -v' to find the tool wherever it landed
    SUB=$(command -v subfinder || echo "/tmp/bin/subfinder")
    HTP=$(command -v httpx || echo "/tmp/bin/httpx")
    NUC=$(command -v nuclei || echo "/tmp/bin/nuclei")

    $SUB -d "$TARGET" -silent | $HTP -silent
    echo "$TARGET" | $NUC -silent -severity critical,high
    
    echo ">> [COMPLETE] MISSION SUCCESSFUL."
    exit 0
fi
