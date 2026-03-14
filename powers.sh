#!/bin/bash
# powers.sh - THE DAILY PLANET RECON LIBRARY

observer() {
    echo ">> [OBSERVER] SCANNING DIGITAL HORIZON FOR $1..."
    subfinder -d "$1" -silent | grep -vE "${OUT_SCOPE//, /|}"
}

kingpin() {
    echo ">> [KINGPIN] PEERING THROUGH SURFACE FOR HIGH-VALUE ASSETS..."
    subfinder -d "$1" -silent | httpx -silent
}

automated_hunt() {
    echo ">> [PHANTOM_ZONE] ENGAGING FULL-STELTH HUNT..."
    subfinder -d "$1" -silent | nuclei -silent
}
