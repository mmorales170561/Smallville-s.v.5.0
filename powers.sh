#!/bin/bash
BIN_DIR="/tmp/smallville_bin"
export PATH="$BIN_DIR:$PATH"
ACTION="$1"; TARGET="$2"; MISSION="$3"

# --- 1. ENVIRONMENT & STEALTH ---
if [ "$RUN_STEALTH" == "1" ]; then
    RL="-rl 5 -c 2"
else
    RL="-c 20"
fi

if [ "$ACTION" == "strike" ]; then
    # ... (Previous Phase 0-5 Logic) ...

    # --- P6: OLYMPUS (Heavy Fuzzing) ---
    if [ "$RUN_P6" == "1" ]; then
        echo ">> [PHASE 6] OLYMPUS: Executing Heavy Strike on $TARGET..."
        
        # Check for target list (from P2) or single target
        [[ -s /tmp/alive.txt ]] && T_SRC="/tmp/alive.txt" || T_SRC="$TARGET"
        
        echo ">> [!] Commencing Param-Fuzzing & Vulnerability Scan..."
        
        # 1. Direct Nuclei Fuzzing (Uses very little disk space)
        # Specifically targeting XSS, SQLi, and SSRF templates
        cat "$T_SRC" | nuclei $RL -silent -tags fuzz,sqli,xss,ssrf -severity critical,high
        
        # 2. Sensitive File Discovery (The "Heavy" part)
        echo ">> [!] Scanning for Hidden Configs & Backdoors..."
        cat "$T_SRC" | nuclei $RL -silent -id backup-files,config-files,exposed-git,exposed-env
    fi

    echo "----------------------------------------"
    echo ">> [SUCCESS] MISSION COMPLETE."
    # Cleanup to save your 2GB limit
    rm -f /tmp/*.txt
fi
