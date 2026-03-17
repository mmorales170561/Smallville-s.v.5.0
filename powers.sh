#!/bin/bash
export PATH=$PATH:/tmp/bin

# Identity Rotation
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# --- SCOPE PROTECTION ---
if [[ ! -z "$IN_SCOPE" && "$2" != *"$IN_SCOPE"* ]]; then
    echo ">> [BLOCK] SCOPE VIOLATION"
    exit 1
fi

mimic_human() {
    delay=$(( ( RANDOM % 3 )  + 2 ))
    echo ">> [MIMIC] STAGGERING TIMING..."
    sleep $delay
}

case "$1" in
    passive)
        echo ">> [MIMIC] PHASE 1: PASSIVE RECON"
        subfinder -d "$2" -silent
        ;;
    active)
        echo ">> [MIMIC] PHASE 1: VALIDATION"
        subfinder -d "$2" -silent | httpx -silent -H "User-Agent: $UA" -sc -title
        mimic_human
        echo ">> [MIMIC] PHASE 2: ACTIVE MAPPING"
        ;;
    vuln_hunt)
        echo ">> [MIMIC] PHASE 1: UPDATING TEMPLATES"
        nuclei -ut -silent
        mimic_human
        echo ">> [MIMIC] PHASE 2: SCANNING"
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity critical,high -header "User-Agent: $UA" -rl 5
        ;;
esac
