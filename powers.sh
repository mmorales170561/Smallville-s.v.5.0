#!/bin/bash
BIN_DIR="/tmp/bin"
mkdir -p $BIN_DIR
export PATH=$PATH:$BIN_DIR

# --- PRIME LOGIC ---
prime_tools() {
    echo ">> [ARMORY] SCANNING FOR WEAPONS..."
    # ... (Keep your existing prime_tools logic here)
}

case "$1" in
    prime) prime_tools ;;
    strike)
        # Prepare filter: Convert comma-separated list into grep pattern
        # e.g., "dev.com, test.com" -> "dev.com\|test.com"
        FILTER_PATTERN=$(echo "$OUT_SCOPE" | sed 's/, /\\|/g' | sed 's/,/\\|/g')

        echo ">> [PHASE 1] SCARLET CEREBRO: MAPPING..."
        if [ -z "$FILTER_PATTERN" ]; then
            $BIN_DIR/subfinder -d "$2" -silent | $BIN_DIR/httpx -silent -title
        else
            echo ">> [FILTER ACTIVE] IGNORING: $OUT_SCOPE"
            $BIN_DIR/subfinder -d "$2" -silent | grep -v "$FILTER_PATTERN" | $BIN_DIR/httpx -silent -title
        fi
        
        if [[ "$WAYBACK" == "1" ]]; then
            echo ">> [PHASE 2] SHADOW ARCHIVE..."
            touch ~/.gau.toml 2>/dev/null
            if [ -z "$FILTER_PATTERN" ]; then
                $BIN_DIR/gau --subs --threads 10 "$2" | head -n 20
            else
                $BIN_DIR/gau --subs --threads 10 "$2" | grep -v "$FILTER_PATTERN" | head -n 20
            fi
        fi

        # ... (Keep existing Naabu/Ports logic here)

        echo ">> [PHASE 4] FIRING RED KRYPTONITE BEAM..."
        if [ -z "$FILTER_PATTERN" ]; then
            $BIN_DIR/subfinder -d "$2" -silent | $BIN_DIR/httpx -silent | $BIN_DIR/nuclei -silent -ni -severity critical
        else
            $BIN_DIR/subfinder -d "$2" -silent | grep -v "$FILTER_PATTERN" | $BIN_DIR/httpx -silent | $BIN_DIR/nuclei -silent -ni -severity critical
        fi
        ;;
esac
