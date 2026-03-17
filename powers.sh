#!/bin/bash
BIN_DIR="/tmp/bin"
export PATH=$PATH:$BIN_DIR

case "$1" in
    prime)
        # (Prime logic here)
        ;;
    strike)
        # SCOPE CLEANING (Omitted for brevity - keep your existing code)
        
        # PHASE 3: GRAPPLING HOOK (FIXED)
        if [ "$RUN_P3" == "1" ]; then
            echo ">> [PHASE 3] GRAPPLING HOOK ($PORT_PROFILE)..."
            
            case "$PORT_PROFILE" in
                "Top 20 (Ghost)")
                    PORTS="80,443,8080,8443,21,22,25,53,110,143,445,3306,3389,5900,6379,9000,9090,9200,9443,10000"
                    ;;
                "Top 100 (Standard)")
                    PORTS="top-100" # Naabu supports top-100/top-1000 directly
                    ;;
                "Top 1000 (Full)")
                    PORTS="top-1000"
                    ;;
            esac

            # Use -tp for top-100/1000, but -p for manual lists
            if [[ "$PORTS" == "top-"* ]]; then
                echo "$FINAL_LIST" | $BIN_DIR/naabu -tp ${PORTS#top-} -silent -rate 1000
            else
                echo "$FINAL_LIST" | $BIN_DIR/naabu -p $PORTS -silent -rate 1000
            fi
        fi

        # ... (Rest of your phases) ...
        ;;
esac
