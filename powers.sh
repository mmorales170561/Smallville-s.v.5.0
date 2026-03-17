#!/bin/bash

# --- CONFIG ---
export PATH="/home/adminuser/go/bin:/tmp/bin:$PATH"
ACTION="$1"
TARGET="$2"
MISSION="$3"

# --- ACTION: PRIME ---
if [ "$ACTION" == "prime" ]; then
    echo ">> [INIT] ARMING SYSTEMS VIA GO-PROXY..."
    
    # 1. Check if Go is available (Streamlit usually has it)
    if ! command -v go &> /dev/null; then
        echo ">> [ERROR] Go compiler not found. Falling back to Pip..."
        # Alternative: Some tools have python wrappers
        pip install --upgrade nuclei-python-wrapper httpx-py &> /dev/null
    fi

    # 2. Install Tools using 'go install'
    echo ">> Installing Subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    
    echo ">> Installing HTTPX..."
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

    echo ">> Installing Nuclei..."
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

    # 3. Move binaries to our accessible path
    mkdir -p /tmp/bin
    cp ~/go/bin/* /tmp/bin/ 2>/dev/null || true
    chmod +x /tmp/bin/*
    
    echo ">> [COMPLETE] ARMORY VERIFIED: $(ls /tmp/bin | grep -E 'subfinder|httpx|nuclei' | tr '\n' ' ')"
    exit 0

# --- ACTION: STRIKE ---
elif [ "$ACTION" == "strike" ]; then
    # Use the first available path
    SUB=$(command -v subfinder || echo "/tmp/bin/subfinder")
    HTP=$(command -v httpx || echo "/tmp/bin/httpx")
    NUC=$(command -v nuclei || echo "/tmp/bin/nuclei")

    echo ">> [INIT] MISSION: $MISSION"
    
    if [ "$RUN_P1" == "1" ]; then
        echo "--- PHASE 1: CEREBRO ---"
        $SUB -d "$TARGET" -silent | $HTP -silent
    fi

    if [ "$RUN_P4" == "1" ]; then
        echo "--- PHASE 4: STRIKE ---"
        echo "$TARGET" | $NUC -silent -severity critical,high
    fi

    echo ">> [COMPLETE] SUCCESS."
    exit 0
fi
