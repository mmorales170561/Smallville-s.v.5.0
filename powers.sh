#!/bin/bash

# --- CONFIG ---
export PATH="/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: PRIME ---
if [ "$ACTION" == "prime" ]; then
    echo ">> [INIT] ARMING SYSTEMS IN /tmp/bin..."
    mkdir -p /tmp/bin
    cd /tmp/bin
    
    # Download Subfinder
    echo ">> Installing Subfinder..."
    wget -q https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip
    unzip -o subfinder_2.6.6_linux_amd64.zip && chmod +x subfinder
    
    # Download HTTPX
    echo ">> Installing HTTPX..."
    wget -q https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip
    unzip -o httpx_1.6.4_linux_amd64.zip && chmod +x httpx

    # Download Nuclei
    echo ">> Installing Nuclei..."
    wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip
    unzip -o nuclei_3.2.9_linux_amd64.zip && chmod +x nuclei

    rm -f *.zip
    echo ">> [COMPLETE] ARMORY VERIFIED: $(ls /tmp/bin | tr '\n' ' ')"
    exit 0

# --- ACTION: STRIKE ---
elif [ "$ACTION" == "strike" ]; then
    echo ">> [INIT] LOCKING MISSION: $MISSION"
    
    # Check if tools exist before running
    if [[ ! -f "/tmp/bin/subfinder" ]]; then
        echo "[ERROR] Armory Empty. Please click 'PRIME ELITE TOOLS' in the sidebar."
        exit 1
    fi

    if [ "$RUN_P1" == "1" ]; then
        echo "--- PHASE 1: CEREBRO (RECON) ---"
        /tmp/bin/subfinder -d "$TARGET" -silent | /tmp/bin/httpx -silent
    fi

    if [ "$RUN_P4" == "1" ]; then
        echo "--- PHASE 4: STRIKE (VULN SCAN) ---"
        echo "$TARGET" | /tmp/bin/nuclei -silent -severity critical,high
    fi

    echo ">> [COMPLETE] MISSION SUCCESSFUL."
    exit 0
fi
