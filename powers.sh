#!/bin/bash
export PATH=$PATH:/tmp/bin

# Identity
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# --- DUAL-GATE ENFORCEMENT ---
# Check Inclusion
if [[ ! -z "$IN_SCOPE" && "$2" != *"$IN_SCOPE"* ]]; then
    echo ">> [BLOCK] SECURITY VIOLATION: Target outside inclusion zone."
    exit 1
fi

# Check Exclusion
if [[ ! -z "$OUT_SCOPE" && "$2" == *"$OUT_SCOPE"* ]]; then
    echo ">> [BLOCK] SECURITY VIOLATION: Target matches restricted exclusion zone."
    exit 1
fi

case "$1" in
    passive)
        subfinder -d "$2" -silent
        ;;
    active)
        subfinder -d "$2" -silent | httpx -silent -H "User-Agent: $UA" -sc -title
        ;;
    vuln_hunt)
        nuclei -ut -silent
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity critical,high -header "User-Agent: $UA" -rl 5
        ;;
esac
