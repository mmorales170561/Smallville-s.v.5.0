import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time
import platform
from datetime import datetime

# --- HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v5.7", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 500px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- THE HARDENED REGISTRY ---
ARSENAL = {
    "Web2": ["subfinder", "amass", "httpx", "waybackurls", "gau", "assetfinder", "ffuf", "katana", "dalfox", "dirsearch"],
    "Web3": ["aderyn", "slither", "arjun"],
    "AI Agent": ["trufflehog", "gitleaks", "garak", "sqlmap", "commix"]
}

# Updated to use direct archive links to prevent "Not a Zip" errors
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip",
    "waybackurls": "https://github.com/tomnomnom/waybackurls/archive/refs/heads/master.zip",
    "gau": "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz",
    "assetfinder": "https://github.com/tomnomnom/assetfinder/releases/download/v0.1.1/assetfinder-linux-amd64-0.1.1.tgz",
    "amass": "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "dalfox": "https://github.com/hahwul/dalfox/releases/download/v2.9.0/dalfox_2.9.0_linux_amd64.tar.gz",
    "dirsearch": "https://github.com/maurosoria/dirsearch/archive/refs/heads/master.zip",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/refs/heads/master.zip",
    "commix": "https://github.com/commixproject/commix/archive/refs/heads/master.zip",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "gitleaks": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.2/gitleaks_8.18.2_linux_x64.tar.gz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/refs/heads/master.zip",
    "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/v0.1.0/aderyn-x86_64-unknown-linux-gnu.tar.gz"
}

def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py":
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    """Smart unpacking: Detects Zip vs Tar regardless of extension."""
    if tool_name not in TOOL_URLS:
        if tool_name in ["garak", "slither"]:
            try:
                subprocess.run(["pip", "install", tool_name, "--prefer-binary", "--quiet"], check=True)
                return True
            except: return False
        return False
    
    url = TOOL_URLS[tool_name]
    try:
        r = requests.get(url, stream=True, timeout=25)
        pkg_path = f"/tmp/{tool_name}_pkg"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        
        # LOGIC GATE: Try Zip first, then Tar
        try:
            with zipfile.ZipFile(pkg_path, 'r') as z:
                z.extractall(BIN_DIR)
        except zipfile.BadZipFile:
            try:
                with tarfile.open(pkg_path, "r:*") as t:
                    t.extractall(path=BIN_DIR)
            except:
                return False
        
        os.remove(pkg_path)
        return True
    except Exception as e:
        return False

# --- MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.7")

# ... (Sidebar and Auth logic same as v5.6) ...

with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", ["Web2", "Web3", "
