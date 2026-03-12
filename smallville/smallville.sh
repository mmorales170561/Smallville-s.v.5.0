#!/bin/bash
# 1. Flush the terminal buffer immediately to kill ghost input
stty -F /dev/tty flush 2>/dev/null

echo "--- Smallville System Online ---"

# 2. Flush before every single read
stty -F /dev/tty flush
read -p "Enter Target Domain: " target

stty -F /dev/tty flush
read -p "Enter In-Scope Regex: " inscope

stty -F /dev/tty flush
read -p "Enter Out-of-Scope Regex: " outscope

echo -e "\nSummary: Target=$target, In=$inscope, Out=$outscope"
stty -F /dev/tty flush
read -p "Confirm Execution (Y/n): " confirm

if [[ "$confirm" == "Y" || "$confirm" == "y" ]]; then
    echo "Starting process..."
else
    echo "Aborted."
fi
#!/bin/bash
# Bypass shell buffers by reading raw bytes from /dev/tty
get_manual_input() {
    # Read input until the user hits Enter (ASCII 10)
    # This reads 1 character at a time until newline is detected
    local line=""
    local char=""
    while true; do
        char=$(dd bs=1 count=1 2>/dev/null)
        if [[ "$char" == $'\x0a' ]]; then break; fi
        line="${line}${char}"
    done
    echo "$line"
}

clear
echo "--- SYSTEM OVERRIDE: RAW INPUT MODE ---"
echo -n "Enter Target Domain: "
target=$(get_manual_input)

echo -n "Enter In-Scope Regex: "
inscope=$(get_manual_input)

echo -n "Enter Out-of-Scope Regex: "
outscope=$(get_manual_input)

echo -e "\nMission Parameter Verification:"
echo "Target: $target | In: $inscope | Out: $outscope"
echo -n "Proceed? (Y/n): "
confirm=$(get_manual_input)

if [[ "$confirm" == "Y" || "$confirm" == "y" ]]; then
    echo "Launching scan..."
    # Your subfinder/httpx commands go here
else
    echo "Aborted."
fi