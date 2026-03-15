#!/bin/bash

# ENSURE SYSTEM PATH INCLUDES OUR TOOLS
export PATH=$PATH:/tmp/bin

observer() {
    echo ">> [SYS_LOG] INITIALIZING SUBDOMAIN_SCAN..."
    subfinder -d "$1" -silent | grep -vE "${OUT_SCOPE//, /|}"
}

kingpin() {
    echo ">> [SYS_LOG] SCANNING_FOR_KINGPIN_ASSETS..."
    subfinder -d "$1" -silent | httpx -silent
}

automated_hunt() {
    echo ">> [SYS_LOG] ENGAGING NUCLEI_HUNT..."
    subfinder -d "$1" -silent | nuclei -silent
}
