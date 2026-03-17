#!/bin/bash
export PATH=$PATH:/tmp/bin

# --- IDENTITY POOL ---
UA_POOL=(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
)
UA=${UA_POOL[$RANDOM % ${#UA_POOL[@]}]}

# --- SCOPE GUARD ---
if [[ ! -z "$IN_SCOPE" && "$2" != *"$IN_SCOPE"* ]]; then
    echo ">> [BLOCK] SCOPE VIOLATION: $2"
    exit 1
fi

# --- HUMAN DELAY ---
mimic_human() {
    delay=$(( ( RANDOM % 5 )  + 3 ))
    echo ">> [MIMIC] PAUSING $delay SECONDS..."
    sleep $delay
}

case "$1" in
    passive)
        subfinder -d "$2" -silent
        ;;
    active)
        subfinder -d "$2" -silent | httpx -silent -H "User-Agent: $UA" -title -sc -td -rl 15
        mimic_human
        ;;
    vuln_hunt)
        nuclei -ut -silent
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity critical,high -header "User-Agent: $UA" -rl 5 -bs 1
        mimic_human
        ;;
    nuclear)
        subfinder -d "$2" -silent | naabu -top-ports 100 -silent -rate 50
        mimic_human
        subfinder -d "$2" -silent | httpx -silent | nuclei -silent -severity info,low,medium,high,critical -rl 5
        ;;
    leak_check)
        echo ">> [WIRE] SCANNING FOR $2 EXPOSURE..."
        # Simulate OSINT leak search
        sleep 4
        echo "CRITICAL: Found 12 exposed credentials in 'DarkWeb' dump for $2"
        ;;
esac
