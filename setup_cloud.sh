#!/bin/bash
# Install Go to /tmp
wget -q https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
tar -C /tmp -xzf go1.22.0.linux-amd64.tar.gz
export PATH=$PATH:/tmp/go/bin

# Set Go bin to a writeable location
mkdir -p /tmp/bin
export GOBIN=/tmp/bin

# Install Tools
/tmp/go/bin/go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
/tmp/go/bin/go install github.com/projectdiscovery/httpx/cmd/httpx@latest
/tmp/go/bin/go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
