#!/bin/bash

# --- CONFIG ---
export PATH="/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: PRIME (Downloads the tools) ---
if [ "$ACTION" == "prime" ]; then
    echo ">> [INIT] ARMING SYSTEMS IN /tmp/bin..."
    mkdir -p /tmp/bin
    cd /tmp/bin
    
    # Download 64-bit Linux binaries for Streamlit Cloud
    echo ">> Downloading subfinder..."
    wget -q https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip && unzip -o subfinder*.zip && rm *.zip
    
    echo ">> Downloading nuclei..."
    wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip && unzip -o nuclei*.zip && rm *.zip
    
    echo ">> Downloading httpx..."
    wget -q https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip && unzip -o httpx*.zip && rm *.zip

    chmod +x /tmp/bin/*
    echo ">> [COMPLETE] ARMORY IS FULL."
    exit 0

# --- ACTION: STRIKE (Runs the scan) ---
elif [ "$ACTION" == "strike" ]; then
    echo ">> [INIT] LOCKING MISSION: $MISSION"
    
    if [ "$RUN_P1" == "1" ]; then
        echo "--- PHASE 1: CEREBRO (RECON) ---"
        subfinder -d "$TARGET" -silent | httpx -silent
    fi

    if [ "$RUN_P4" == "1" ]; then
        echo "--- PHASE 4: STRIKE (VULN SCAN) ---"
        echo "$TARGET" | nuclei -silent -severity critical,high
    fi

    echo ">> [COMPLETE] MISSION SUCCESSFUL."
    exit 0
fi
