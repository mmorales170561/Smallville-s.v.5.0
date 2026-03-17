import requests
import zipfile
import io

# Add this inside the Sidebar "PRIME ELITE TOOLS" button logic:
if st.button("PRIME ELITE TOOLS", width="stretch"):
    with st.spinner("📥 Bypassing Firewall..."):
        os.makedirs(BIN_PATH, exist_ok=True)
        
        # Mapping of tools to their direct download URLs
        tools = {
            "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
            "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
            "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip"
        }
        
        for name, url in tools.items():
            st.write(f"Installing {name}...")
            r = requests.get(url)
            if r.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(BIN_PATH)
                st.write(f"✅ {name} extracted.")
            else:
                st.error(f"❌ Failed to download {name}. Code: {r.status_code}")
        
        # Force permissions
        subprocess.run(f"chmod +x {BIN_PATH}/*", shell=True)
        st.success("Armory Primed via Python Stream!")
        st.rerun()
