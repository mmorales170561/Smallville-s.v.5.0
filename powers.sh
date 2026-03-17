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
        if ! command -v ${tools[$i]} &> /dev/null && [ ! -f "$BIN_DIR/${tools[$i]}" ]; then
            echo ">> [FETCHING] ${tools[$i]}..."
            
            # Determine extension
            ext="zip"
            if [[ ${urls[$i]} == *".tar.gz" ]]; then ext="tar.gz"; fi
            
            local pkg="/tmp/${tools[$i]}.$ext"
            wget -q ${urls[$i]} -O "$pkg"
            
            # Precise Extraction
            python3 -c "import shutil; shutil.unpack_archive('$pkg', '$BIN_DIR')"
            
            rm "$pkg"
        fi
    done
    
    chmod +x $BIN_DIR/*
    echo ">> [ARMORY] ALL WEAPON SYSTEMS PRIMED."
}

case "$1" in
    prime)
        prime_tools
        ;;
    strike)
        # Force re-check of binaries
        if [ ! -f "$BIN_DIR/subfinder" ]; then prime_tools; fi
        
        echo ">> [PHASE 1] SCARLET CEREBRO: MAPPING ASSETS..."
        $BIN_DIR/subfinder -d "$2" -silent | $BIN_DIR/httpx -silent -title
        
        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE: GAUGING DATA..."
            # gau is already working based on your logs
            $BIN_DIR/gau --subs --threads 10 "$2" | head -n 30
        fi

        if [[ "$PORTS" == "1" ]]; then
            echo ">> [PHASE 3] GRAPPLING HOOK: PROBING PORTS..."
            $BIN_DIR/naabu -host "$2" -top-ports 100 -silent
        fi

        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        $BIN_DIR/subfinder -d "$2" -silent | $BIN_DIR/httpx -silent | $BIN_DIR/nuclei -silent -severity critical -rl 7
        ;;
esac
