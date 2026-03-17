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
        # --- SELF-FIX LIBPCAP ---
        if [ ! -f "/usr/lib/libpcap.so.0.8" ] && [ -f "/usr/lib/x86_64-linux-gnu/libpcap.so.1.10.3" ]; then
             ln -s /usr/lib/x86_64-linux-gnu/libpcap.so.1.10.3 /tmp/bin/libpcap.so.0.8 2>/dev/null
             export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/bin
        fi

        echo ">> [PHASE 1] SCARLET CEREBRO: MAPPING..."
        $BIN_DIR/subfinder -d "$2" -silent | $BIN_DIR/httpx -silent -title
        
        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE..."
            touch ~/.gau.toml 2>/dev/null
            $BIN_DIR/gau --subs --threads 10 "$2" | head -n 20
        fi

        if [[ "$PORTS" == "1" ]]; then
            echo ">> [PHASE 3] GRAPPLING HOOK..."
            $BIN_DIR/naabu -host "$2" -top-ports 100 -silent 2>/dev/null || echo ">> [!] Naabu requires libpcap installation."
        fi

        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        # -ni hides the update/version checks
        $BIN_DIR/subfinder -d "$2" -silent | $BIN_DIR/httpx -silent | $BIN_DIR/nuclei -silent -ni -severity critical
        ;;
esac
