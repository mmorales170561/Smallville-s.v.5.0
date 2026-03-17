#!/bin/bash
BIN_DIR="/tmp/bin"
mkdir -p $BIN_DIR
export PATH=$PATH:$BIN_DIR

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
            
            # Use Python's built-in extractor instead of 'unzip'
            python3 -c "import shutil; shutil.unpack_archive('$pkg', '$BIN_DIR')"
            
            rm "$pkg"
        fi
    done
    chmod +x $BIN_DIR/*
    echo ">> [ARMORY] ALL SYSTEMS OPERATIONAL."
}

case "$1" in
    prime) prime_tools ;;
    strike)
        # Call the priming check silently
        if [[ ! -f "$BIN_DIR/subfinder" ]]; then prime_tools > /dev/null; fi
        
        echo ">> [1/4] SCARLET CEREBRO: MAPPING..."
        subfinder -d "$2" -silent | httpx -silent -title
        
        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [2/4] SHADOW ARCHIVE: GAUGING DATA..."
            echo "$2" | gau --subs --threads 10 | head -n 20
        fi

        echo ">> [4/4] FIRING RED KRYPTONITE BEAM..."
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity critical -rl 7
        ;;
esac
