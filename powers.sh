#!/bin/bash

# --- CONFIG ---
export PATH="/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: PRIME ---
if [ "$ACTION" == "prime" ]; then
    echo ">> [INIT] ARMING SYSTEMS IN /tmp/bin (TAR MODE)..."
    mkdir -p /tmp/bin
    cd /tmp/bin
    
    # Download Subfinder (.tar.gz)
    echo ">> Installing Subfinder..."
    wget -q https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.tar.gz
    tar -xzf subfinder_2.6.6_linux_amd64.tar.gz && chmod +x subfinder
    
    # Download HTTPX (.tar.gz)
    echo ">> Installing HTTPX..."
    wget -q https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.tar.gz
    tar -xzf httpx_1.6.4_linux_amd64.tar.gz && chmod +x httpx

    # Download Nuclei (.tar.gz)
    echo ">> Installing Nuclei..."
    wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.tar.gz
    tar -xzf nuclei_3.2.9_linux_amd64.tar.gz && chmod +x nuclei

    # Cleanup
    rm -f *.tar.gz
    echo ">> [COMPLETE] ARMORY VERIFIED: $(ls /tmp/bin | tr '\n' ' ')"
    exit 0

# --- ACTION: STRIKE ---
elif [ "$ACTION" == "strike" ]; then
    # ... (Keep the rest of your strike code the same)
    if [[ ! -f "/tmp/bin/subfinder" ]]; then
        echo "[ERROR] Armory Empty. Please click 'PRIME ELITE TOOLS' in the sidebar."
        exit 1
    fi
    
    echo "--- PHASE 1: CEREBRO (RECON) ---"
    /tmp/bin/subfinder -d "$TARGET" -silent | /tmp/bin/httpx -silent
    
    # ... etc
fi
