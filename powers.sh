#!/bin/bash
# powers.sh

observer() {
    echo ">> [SYS_LOG] INITIALIZING SUBDOMAIN_SCAN..."
    echo ">> [SYS_LOG] FILTERING BY IN_SCOPE..."
    subfinder -d "$1" -silent | grep -vE "${OUT_SCOPE//, /|}"
    echo ">> [SYS_LOG] SCAN_SUCCESS."
}

kingpin() {
    echo ">> [SYS_LOG] SCANNING_FOR_KINGPIN_ASSETS..."
    subfinder -d "$1" -silent | httpx -silent
}

automated_hunt() {
    echo ">> [SYS_LOG] ENGAGING NUCLEI_HUNT..."
    subfinder -d "$1" -silent | nuclei -silent
}
