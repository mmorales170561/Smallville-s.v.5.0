#!/bin/bash

# Observer: Passive Recon
observer() {
    echo "--- DAILY PLANET OBSERVER: SCANNING $1 ---"
    subfinder -d "$1" -silent
}

# Kingpin: High Value Targets
kingpin() {
    echo "--- DAILY PLANET KINGPIN: FILTERING $1 ---"
    # Example logic: just listing common files
    subfinder -d "$1" -silent | httpx -silent
}

# Automated Hunt: The full sweep
automated_hunt() {
    echo "--- DAILY PLANET AUTOMATED HUNT: $1 ---"
    subfinder -d "$1" -silent | httpx -silent | nuclei -silent
}
