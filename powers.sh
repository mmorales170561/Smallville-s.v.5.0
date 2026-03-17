#!/bin/bash
BIN_DIR="/tmp/bin"
mkdir -p $BIN_DIR
export PATH=$PATH:$BIN_DIR

prime_tools() {
    echo ">> [ARMORY] SYNCING WEAPONS TO CORE..."
    # Tool List: Name | URL
    tools=("subfinder" "httpx" "nuclei" "naabu" "gau" "subjack" "mantra")
    urls=(
        "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip"
        "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip"
        "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip"
        "https://github.com/projectdiscovery/naabu/releases/download/v2.3.1/naabu_2.3.1_linux_amd64.zip"
        "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz"
        "https://github.com/haccer/subjack/releases/download/v1.1/subjack_linux_64-bit.tar.gz"
        "https://github.com/MrEmpy/mantra/releases/download/v1.2/mantra_linux_amd64.zip"
    )

    for i in "${!tools[@]}"; do
        if [ ! -f "$BIN_DIR/${tools[$i]}" ]; then
            echo ">> [FETCHING] ${tools[$i]}..."
            local ext="zip"; [[ ${urls[$i]} == *".tar.gz" ]] && ext="tar.gz"
            local pkg="/tmp/${tools[$i]}.$ext"
            wget -q ${urls[$i]} -O "$pkg"
            python3 -c "import shutil; shutil.unpack_archive('$pkg', '$BIN_DIR')"
            rm "$pkg"
        fi
    done
    
    # Ensure all are executable
    chmod +x $BIN_DIR/*
    echo ">> [SUCCESS] ALL WEAPONS ONLINE."
}

case "$1" in
    prime) prime_tools ;;
    strike)
        # --- 1. SCOPE PREP ---
        FULL_LIST=$( (echo "$2"; echo "$IN_SCOPE" | tr ',' '\n' | tr ' ' '\n') | sort -u | grep -v "^$" )

        # --- 2. PHASE 1-3 (Omitted for brevity, keep your existing code here) ---

        # --- 3. PHASE 4: THE RED KRYPTONITE BEAM (EXTENDED) ---
        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        LIVE_HOSTS=$(echo "$FULL_LIST" | $BIN_DIR/httpx -silent)

        # A. VULNERABILITY SCAN (Nuclei)
        VULN_DATA=$(echo "$LIVE_HOSTS" | $BIN_DIR/nuclei -silent -ni -severity critical)

        # B. SUBDOMAIN TAKEOVER CHECK (Subjack)
        # Uses a fingerprint file - we'll create a dummy one if it doesn't exist
        touch /tmp/fingerprints.json
        TAKEOVER_DATA=$(echo "$FULL_LIST" | $BIN_DIR/subjack -w /dev/stdin -t 10 -timeout 30 -o /dev/stdout -ssl)

        # C. JS SECRET MINING (Mantra)
        JS_SECRETS=$(echo "$LIVE_HOSTS" | $BIN_DIR/mantra -silent)

        # --- 4. DATA CONSOLIDATION & LOGGING ---
        # Combine all findings into a single POC string for the H1 Report
        TOTAL_POC=$(echo -e "VULNS:\n$VULN_DATA\n\nTAKEOVERS:\n$TAKEOVER_DATA\n\nJS_SECRETS:\n$JS_SECRETS")
        NUM_VULNS=$(echo "$TOTAL_POC" | grep -c -E "\[|Vulnerable")

        python3 -c "
import sqlite3, datetime
conn = sqlite3.connect('red_kryptonite_ledger.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT, ports INTEGER, vulns INTEGER, poc TEXT)')
c.execute(\"INSERT INTO ledger (timestamp, target, intel, ports, vulns, poc) VALUES (?, ?, ?, ?, ?, ?)\", 
          (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '$2', 'Deep Strike Complete', 0, $NUM_VULNS, '$TOTAL_POC'))
conn.commit()
conn.close()
"
        echo ">> [COMPLETE] INTELLIGENCE UPLOADED."
        ;;
esac
