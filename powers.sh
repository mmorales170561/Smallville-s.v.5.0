#!/bin/bash
# powers.sh - THE DAILY PLANET RECONNAISSANCE ENGINE

# 1. SETUP: Ensure our environment can see the tools in the /tmp/bin folder
export PATH=$PATH:/tmp/bin
export GO111MODULE=on

# 2. MODULE: OBSERVER (Passive Discovery)
observer() {
    local target=$1
    echo ">> [SYS_LOG] INITIALIZING PASSIVE RECONNAISSANCE ON: $target"
    
    if [ -z "$OUT_SCOPE" ]; then
        subfinder -d "$target" -silent
    else
        subfinder -d "$target" -silent | grep -vE "${OUT_SCOPE//, /|}"
    fi
    echo ">> [SYS_LOG] PASSIVE SCAN COMPLETE."
}

# 3. MODULE: KINGPIN (Live Asset Mapping)
kingpin() {
    local target=$1
    echo ">> [SYS_LOG] MAPPING LIVE ATTACK SURFACE FOR: $target"
    
    if [ -z "$OUT_SCOPE" ]; then
        subfinder -d "$target" -silent | httpx -silent -title -sc -td
    else
        subfinder -d "$target" -silent | grep -vE "${OUT_SCOPE//, /|}" | httpx -silent -title -sc -td
    fi
    echo ">> [SYS_LOG] ASSET MAPPING CONCLUDED."
}

# 4. MODULE: AUTOMATED HUNT (Vulnerability Assessment)
automated_hunt() {
    local target=$1
    echo ">> [SYS_LOG] ENGAGING WATCHTOWER VULNERABILITY SCAN..."
    
    # Ensure templates are ready for the hunt
    nuclei -ut -silent
    
    # Executing the full chain
    if [ -z "$OUT_SCOPE" ]; then
        subfinder -d "$target" -silent | httpx -silent | nuclei -silent -severity info,low,medium,high,critical
    else
        subfinder -d "$target" -silent | grep -vE "${OUT_SCOPE//, /|}" | httpx -silent | nuclei -silent -severity info,low,medium,high,critical
    fi
    echo ">> [SYS_LOG] HUNT CONCLUDED."
}

# 5. DIAGNOSTIC: TOOL CHECK
# Use this to verify if LexCorp has interfered with your installations
sys_check() {
    echo ">> [SYS_DIAGNOSTIC] VERIFYING KRYPTONIAN ASSETS..."
    command -v subfinder >/dev/null 2>&1 && echo ">> subfinder: READY" || echo ">> subfinder: MISSING"
    command -v httpx >/dev/null 2>&1 && echo ">> httpx: READY" || echo ">> httpx: MISSING"
    command -v nuclei >/dev/null 2>&1 && echo ">> nuclei: READY" || echo ">> nuclei: MISSING"
}

# Handle command-line arguments
# Usage: ./powers.sh [module_name] [target_domain]
case "$1" in
    observer) observer "$2" ;;
    kingpin) kingpin "$2" ;;
    automated_hunt) automated_hunt "$2" ;;
    sys_check) sys_check ;;
    *) echo ">> [ERR] UNKNOWN MODULE" ;;
esac
