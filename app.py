import streamlit as st
import subprocess, os, requests, zipfile, tarfile, io, shutil

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# --- 2. THE OMNI-EXTRACTOR ---
def prime_armory():
    URLS = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "airix": "https://github.com/projectdiscovery/airix/releases/download/v0.0.3/airix_0.0.3_linux_amd64.zip"
    }
    
    os.makedirs(BIN_PATH, exist_ok=True)
    status_area = st.sidebar.empty()
    
    for name, url in URLS.items():
        try:
            status_area.info(f"Downloading {name}...")
            response = requests.get(url, stream=True)
            file_data = io.BytesIO(response.content)
            
            # Check for ZIP
            if zipfile.is_zipfile(file_data):
                with zipfile.ZipFile(file_data) as z:
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(os.path.join(BIN_PATH, name), "wb") as b:
                                b.write(z.read(f))
            # Check for TAR.GZ
            else:
                file_data.seek(0)
                try:
                    with tarfile.open(fileobj=file_data, mode="r:gz") as t:
                        for member in t.getmembers():
                            if member.name.endswith(name):
                                # Extract binary only, ignore paths
                                content = t.extractfile(member).read()
                                with open(os.path.join(BIN_PATH, name), "wb") as b:
                                    b.write(content)
                except Exception as tar_err:
                    st.sidebar.error(f"Failed to untar {name}: {tar_err}")
            
            os.chmod(os.path.join(BIN_PATH, name), 0o755)
            st.sidebar.success(f"✓ {name} Ready")
            
        except Exception as e:
            st.sidebar.error(f"Err {name}: {e}")
    status_area.empty()

# --- 3. SIDEBAR HUD ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        prime_armory()
    
    if st.button("🔴 HARD RESET", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.rerun()

    st.divider()
    # (Rest of your toggles for P1-P6)

# --- 4. MAIN HUD ---
# (Rest of your HUD code including the FIRE GUN button logic)
