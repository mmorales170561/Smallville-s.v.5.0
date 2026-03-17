#!/bin/bash
BIN_DIR="/tmp/bin"
mkdir -p $BIN_DIR
export PATH=$PATH:$BIN_DIR
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Watchtower/9.0"

prime_tools() {
    echo ">> [ARMORY] SCANNING FOR WEAPONS..."
    
    tools=("subfinder" "httpx" "nuclei" "naabu" "gau")
    urls=(
        "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip"
        "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip"
        "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip"
        "https://github.com/projectdiscovery/naabu/releases/download/v2.3.1/naabu_2.3.1_linux_amd64.zip"
        "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz"
    )

    for i in "${!tools[@]}"; do
        if ! command -v ${tools[$i]} &> /dev/null; then
            echo ">> [FETCHING] ${tools[$i]}..."
            local pkg="/tmp/${tools[$i]}_pkg"
            wget -q ${urls[$i]} -O "$pkg"
            
            # Universal Extraction using Python's built-in modules
            # This bypasses the 'unzip command not found' error
            python3 -c "import shutil; shutil.unpack_archive('$pkg', '$BIN_DIR')"
            
            rm "$pkg"
        fi
    done
    
    chmod +x $BIN_DIR/*
    echo ">> [ARMORY] ALL WEAPON SYSTEMS PRIMED AND READY."
}

case "$1" in
    prime)
        prime_tools
        ;;
    strike)
        # Check if tools are missing before firing
        if [[ ! -f "$BIN_DIR/subfinder" ]]; then
            prime_tools
        fi
        
        echo ">> [PHASE 1] SCARLET CEREBRO: MAPPING ASSETS..."
        subfinder -d "$2" -silent | httpx -silent -title
        
        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE: GAUGING DATA..."
            echo "$2" | gau --subs --threads 10 | head -n 30
        fi

        if [[ "$PORTS" == "1" ]]; then
            echo ">> [PHASE 3] GRAPPLING HOOK: PROBING PORTS..."
            naabu -host "$2" -top-ports 100 -silent
        fi

        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        # Nuclei scan with scope protection
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity critical -header "User-Agent: $UA" -rl 7
        ;;
esac
echo ">> [COMPLETE] DATA SYNCED."
