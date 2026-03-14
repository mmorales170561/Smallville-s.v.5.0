#!/bin/bash
# powers.sh

observer() {
    echo ">> [INFO] INITIALIZING SUBDOMAIN DISCOVERY..."
    subfinder -d "$1" -silent | grep -vE "${OUT_SCOPE//, /|}"
    echo ">> [SUCCESS] SCAN COMPLETE."
}

kingpin() {
    echo ">> [INFO] MAPPING ATTACK SURFACE..."
    subfinder -d "$1" -silent | httpx -silent
    echo ">> [SUCCESS] SURFACE MAPPED."
}

automated_hunt() {
    echo ">> [INFO] ENGAGING PHANTOM_ZONE SCAN..."
    subfinder -d "$1" -silent | nuclei -silent
    echo ">> [SUCCESS] HUNT CONCLUDED."
}
