#!/bin/bash

# --- CONFIG ---
export PATH="/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: PRIME ---
if [ "$ACTION" == "prime" ]; then
    echo ">> [INIT] ARMING SYSTEMS IN /tmp/bin (FORCE-CURL MODE)..."
    mkdir -p /tmp/bin
    cd /tmp/bin
    
    # 1. Download Subfinder
    echo ">> Installing Subfinder..."
    curl -sL "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.tar.gz" -o sub.tar.gz
    tar -xzf sub.tar.gz && chmod +x subfinder
    
    # 2. Download HTTPX
    echo ">> Installing HTTPX..."
    curl -sL "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.tar.gz" -o httpx.tar.gz
    tar -xzf httpx.tar.gz && chmod +x httpx

    # 3. Download Nuclei
    echo ">> Installing Nuclei..."
    curl -sL "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.tar.gz" -o nuclei.tar.gz
    tar -xzf nuclei.tar.gz && chmod +x nuclei

    # Cleanup
    rm -f *.tar.gz
    echo ">> [COMPLETE] ARMORY VERIFIED: $(ls /tmp/bin | grep -E 'subfinder|httpx|nuclei' | tr '\n' ' ')"
    exit 0

# --- ACTION: STRIKE ---
elif [ "$ACTION" == "strike" ]; then
    if [[ ! -f "/tmp/bin/subfinder" ]]; then
        echo "[ERROR] Armory Empty. Run PRIME first."
        exit 1
    fi
    
    # Force absolute paths for execution
    /tmp/bin/subfinder -d "$TARGET" -silent | /tmp/bin/httpx -silent
    echo "$TARGET" | /tmp/bin/nuclei -silent -severity critical,high
    
    echo ">> [COMPLETE] MISSION SUCCESSFUL."
    exit 0
fi
