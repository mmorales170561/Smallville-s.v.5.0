# --- UPDATE THE INSTALLER ---
@st.cache_resource
def provision_tools():
    if not os.path.exists("/tmp/bin/nuclei"): # Check for Nuclei specifically
        with st.status(">> [SYSTEM] INSTALLING KRYPTONIAN_TOOLSET..."):
            install_cmd = """
            mkdir -p /tmp/bin
            wget -q -O /tmp/go.tar.gz https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
            tar -C /tmp -xzf /tmp/go.tar.gz
            export PATH=$PATH:/tmp/go/bin
            export GOBIN=/tmp/bin
            /tmp/go/bin/go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
            /tmp/go/bin/go install github.com/projectdiscovery/httpx/cmd/httpx@latest
            /tmp/go/bin/go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
            """
            subprocess.run(install_cmd, shell=True, executable='/bin/bash')
    return True

# --- UPDATE THE SELECTBOX ---
ability = st.selectbox(">> MODULE", ["Observer", "Kingpin", "Automated Hunt"])

# --- UPDATE THE MAPPING ---
mapping = {
    "Observer": "observer", 
    "Kingpin": "kingpin", 
    "Automated Hunt": "automated_hunt"
}
