#!/bin/bash
export PATH=$PATH:/tmp/bin

observer() {
    subfinder -d "$1" -silent | grep -vE "${OUT_SCOPE//, /|}"
}

kingpin() {
    subfinder -d "$1" -silent | httpx -silent
}

automated_hunt() {
    subfinder -d "$1" -silent | nuclei -silent
}
