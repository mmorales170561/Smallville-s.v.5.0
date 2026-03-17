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
        if [ ! -f "$BIN_DIR/${tools[$i]}" ]; then
            echo ">> [FETCHING] ${tools[$i]}..."
            ext="zip"; [[ ${urls[$i]} == *".tar.gz" ]] && ext="tar.gz"
            local pkg="/tmp/${tools[$i]}.$ext"
            wget -q ${urls[$i]} -O "$pkg"
            python3 -c "import shutil; shutil.unpack_archive('$pkg', '$BIN_DIR')"
            rm "$pkg"
        fi
    done
    chmod +x $BIN_DIR/*
}

case "$1" in
    prime) prime_tools ;;
    strike)
        # 1. SCOPE PREPARATION
        FILTER_PATTERN=$(echo "$OUT_SCOPE" | sed 's/, /\\|/g' | sed 's/,/\\|/g')
        # Combine Seed Target and In-Scope list
        FULL_LIST=$( (echo "$2"; echo "$IN_SCOPE" | tr ',' '\n' | tr ' ' '\n') | sort -u | grep -v "^$" )
        if [ -n "$FILTER_PATTERN" ]; then
            FULL_LIST=$(echo "$FULL_LIST" | grep -v "$FILTER_PATTERN")
        fi

        echo ">> [PHASE 1] SCARLET CEREBRO: MAPPING..."
        echo "$FULL_LIST" | $BIN_DIR/subfinder -silent | $BIN_DIR/httpx -silent -title

        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE: MINING HISTORY..."
            touch ~/.gau.toml 2>/dev/null
            echo "$FULL_LIST" | $BIN_DIR/gau --subs --threads 10 | head -n 25
        fi

        if [[ "$SECRETS" == "1" ]]; then
            echo ">> [PHASE 2.5] SECRET SNIPER: AUDITING..."
            echo "$FULL_LIST" | $BIN_DIR/httpx -path "/.env","/.git/config" -silent -mc 200 -nc
        fi

        if [[ "$PORTS" == "1" ]]; then
            echo ">> [PHASE 3] GRAPPLING HOOK: PROBING PORTS..."
            # Self-fixing link if Naabu still looks for libpcap in a specific spot
            export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu
            echo "$FULL_LIST" | $BIN_DIR/naabu -top-ports 100 -silent -rate 500
        fi

        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        # -ni (No Interaction) hides the 'outdated' version check prompts
        echo "$FULL_LIST" | $BIN_DIR/httpx -silent | $BIN_DIR/nuclei -silent -ni -severity critical,high
        
        echo ">> [COMPLETE] MISSION LOGGED."
        ;;
esac
