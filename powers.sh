#!/bin/bash
export PATH=$PATH:/tmp/bin

# Identity
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# --- TELEMETRY: GATE CHECK ---
echo ">> [1/5] VERIFYING SCOPE PERIMETERS..."
if [[ ! -z "$IN_SCOPE" && "$2" != *"$IN_SCOPE"* ]]; then
    echo ">> [FATAL] TARGET OUTSIDE INCLUSION ZONE."
    exit 1
fi
if [[ ! -z "$OUT_SCOPE" && "$2" == *"$OUT_SCOPE"* ]]; then
    echo ">> [FATAL] TARGET MATCHES EXCLUSION ZONE."
    exit 1
fi

echo ">> [2/5] ROTATING USER-AGENT TO $UA"
sleep 1

case "$1" in
    passive)
        echo ">> [3/5] COMMENCING PASSIVE RECONNAISSANCE..."
        subfinder -d "$2" -silent
        echo ">> [4/5] PARSING SUBDOMAIN RESULTS..."
        ;;
    active)
        echo ">> [3/5] VALIDATING HOST RESPONSIVENESS..."
        subfinder -d "$2" -silent | httpx -silent -H "User-Agent: $UA" -sc -title
        echo ">> [MIMIC] STAGGERING REQUESTS FOR STEALTH..."
        sleep 3
        echo ">> [4/5] MAPPING ACTIVE ASSETS..."
        ;;
    vuln_hunt)
        echo ">> [3/5] UPDATING VULNERABILITY TEMPLATES..."
        nuclei -ut -silent
        echo ">> [MIMIC] INTRODUCING JITTER DELAY..."
        sleep 4
        echo ">> [4/5] ANALYZING ENDPOINTS FOR WEAKNESS..."
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity critical,high -header "User-Agent: $UA" -rl 5
        ;;
esac

echo ">> [5/5] MISSION SUCCESS. SYNCING DATA TO VAULT."
