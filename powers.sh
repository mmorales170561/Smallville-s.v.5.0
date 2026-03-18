# --- 1. SHADOW STEP STEALTH ---
if [ "$RUN_STEALTH" == "1" ]; then
    # -rl 1 (1 request per second) is the "Golden Rule" for hardened WAFs
    # -mhe 3 (Max Host Errors) prevents Nuclei from quitting too early
    RL="-rl 1 -c 1 -mhe 100 -timeout 10 -H 'User-Agent: $UA'"
    K_RL="-c 1 -d 2 -rl 1" 
else
    RL="-c 20 -H 'User-Agent: $UA'"
    K_RL="-c 5"
fi

# --- 2. PHASE 2: RESCUE INJECTION ---
if [ "$RUN_P2" == "1" ]; then
    echo ">> [PHASE 2] SHADOW: Resolving Targets..."
    [[ -s /tmp/subs.txt ]] && SRC="/tmp/subs.txt" || SRC="/tmp/target_list.txt"
    
    # We add -retries 3 to give the network more chances
    cat "$SRC" | $HTTPX -silent -sc -td -ip $WAF_HEADERS -retries 3 -timeout 10 > /tmp/alive.txt
    
    if [ ! -s /tmp/alive.txt ]; then
        echo "   [!] WAF Blackhole detected. Injecting Shadow Targets..."
        while read -r line; do
            # Add ONLY https for modern sites like Bose to avoid 80->443 redirect loops
            echo "https://$line" >> /tmp/alive.txt
        done < /tmp/target_list.txt
    fi
    echo "   [✓] $(wc -l < /tmp/alive.txt) targets ready."
fi
