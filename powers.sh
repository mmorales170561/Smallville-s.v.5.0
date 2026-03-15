#!/bin/bash

# --- METROPOLIS PATHING ---
# Ensures the terminal can find tools installed in the temporary directory
export PATH=$PATH:/tmp/bin
export GO111MODULE=on

# --- MODULE: OBSERVER ---
# Passive reconnaissance to find subdomains while respecting scope
observer() {
    local target=$1
    echo ">> [OBSERVER] SCANNING DIGITAL HORIZON FOR: $target"
    
    if [ -z "$OUT_SCOPE" ]; then
        subfinder -d "$target" -silent
    else
        # Filter out domains listed in the OUT_SCOPE variable
        subfinder -d "$target" -silent | grep -vE "${OUT_SCOPE//, /|}"
    fi
    
    echo ">> [OBSERVER] PASSIVE SCAN COMPLETE."
}

# --- MODULE: KINGPIN ---
# Identifies live web assets and filters for high-value targets
kingpin() {
    local target=$1
    echo ">> [KINGPIN] PEERING THROUGH SURFACE FOR LIVE ASSETS..."
    
    if [ -z "$OUT_SCOPE" ]; then
        subfinder -d "$target" -silent | httpx -silent -title -sc -td
    else
        subfinder -d "$target" -silent | grep -vE "${OUT_SCOPE//, /|}" | httpx -silent -title -sc -td
    fi
    
    echo ">> [KINGPIN] LIVE ASSETS MAPPED."
}

# --- MODULE: AUTOMATED HUNT ---
# Full-scale automated vulnerability scan using Nuclei
automated_hunt() {
    local target=$1
    echo ">> [PHANTOM_ZONE] ENGAGING FULL-STEALTH AUTOMATED HUNT..."
    
    if [ -z "$OUT_SCOPE" ]; then
        subfinder -d "$target" -silent | httpx -silent | nuclei -silent -severity critical,high,medium
    else
        subfinder -d "$target" -silent | grep -vE "${OUT_SCOPE//, /|}" | httpx -silent | nuclei -silent -severity critical,high,medium
    fi
    
    echo ">> [PHANTOM_ZONE] HUNT CONCLUDED. CHECK LOGS FOR FINDINGS."
}

# --- SYSTEM CHECK ---
# A utility function to verify tool health
sys_check() {
    echo ">> [CHECK] VERIFYING KRYPTONIAN TOOLSET..."
    command -v subfinder >/dev/null 2>&1 && echo ">> subfinder: READY" || echo ">> subfinder: MISSING"
    command -v httpx >/dev/null 2>&1 && echo ">> httpx: READY" || echo ">> httpx: MISSING"
    command -v nuclei >/dev/null 2>&1 && echo ">> nuclei: READY" || echo ">> nuclei: MISSING"
}
