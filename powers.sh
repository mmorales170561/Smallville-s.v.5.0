#!/bin/bash

# --- THE PRIME FUNCTION ---
if [ "$1" == "prime" ]; then
    echo "--- INITIALIZING ARMORY ---"
    
    # 1. Create the bin directory if it doesn't exist
    mkdir -p /tmp/bin
    cd /tmp/bin || exit

    # 2. Download and unpack (Example for Nuclei)
    # Using your Python one-liner trick to avoid 'unzip' dependency
    if [ ! -f "nuclei" ]; then
        curl -sL https://github.com/projectdiscovery/nuclei/releases/download/v3.1.8/nuclei_3.1.8_linux_amd64.zip -o nuclei.zip
        python3 -c "import shutil; shutil.unpack_archive('nuclei.zip', '.')"
        rm nuclei.zip
    fi

    # 3. Repeat for other tools (subfinder, naabu, etc.)
    
    # 4. Final Permission Strike
    chmod +x /tmp/bin/*
    echo "--- ARMORY ONLINE ---"
fi
