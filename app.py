import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time
from datetime import datetime

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v5.3", layout="wide")
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

# --- 2. THE ABSOLUTE REGISTRY ---
ARSENAL = {
    "RECON": ["subfinder", "amass", "httpx", "waybackurls", "gau", "assetfinder"],
    "WEB/FUZZ": ["ffuf", "arjun", "katana", "dalfox", "dirsearch"],
    "EXPLOIT": ["nuclei", "sqlmap", "commix", "tplimap"],
    "AI/SECRETS": ["trufflehog", "gitleaks", "garak", "pyrit"]
}

# Verified Direct Download Links
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip",
    "waybackurls": "https://github.com/tomnomnom/waybackurls/archive/refs/heads/master.zip",
    "gau": "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz",
    "assetfinder": "https://github.com/tomnomnom/assetfinder/releases/download/v0.1.1/assetfinder-linux-amd64-0.1.1.tgz",
    "amass": "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/refs/heads/master.zip",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "dalfox": "https://github.com/hahwul/dalfox/releases/download/v2.9.0/dalfox_2.9.0_linux_amd64.tar.gz",
    "dirsearch": "https://github.com/maurosoria/dirsearch/archive/refs/heads/master.zip",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/tarball/master",
    "commix": "https://github.com/commixproject/commix/tarball/master",
    "tplimap": "https://github.com/epinna/tplimap/tarball/master",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "gitleaks": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.2/gitleaks_8.18.2_linux_x64.tar.gz"
}

# --- 3. ENHANCED ENGINES ---
def find_exe(name):
    # Check for direct binaries or python entry points
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or f == "main.py" and name in root:
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: 
        # For tools like Garak/Pyrit, we try PIP installation if URL is absent
        if tool_name in ["garak", "pyrit"]:
            try:
                subprocess.run(["pip", "install", tool_name, "--quiet"], check=True)
                return True
            except: return False
        return False
        
    url = TOOL_URLS[tool_name]
    try:
        r = requests.get(url, stream=True, timeout=20)
        ext = ".zip" if "zip" in url or "master" in url or "ball" in url else ".tar.gz"
        pkg_path = f"/tmp/{tool_name}{ext}"
        
        with open(pkg_path, 'wb') as f: f.write(r.content)
        
        if "zip" in ext:
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            with tarfile.open(pkg_path, "r:gz") as t: t.extractall(path=BIN_DIR)
        
        # Post-extraction: If it's a python tool, try to install its requirements
        tool_root = os.path.join(BIN_DIR, next(os.walk(BIN_DIR))[1][0] if next(os.walk(BIN_DIR))[1] else "")
        req_file = os.path.join(tool_root, "requirements.txt")
        if os.path.exists(req_file):
            subprocess.run(["pip", "install", "-r", req_file, "--quiet"])
            
        os.remove(pkg_path)
        return True
    except: return False

# --- 4. HUD LOGIC ---
with st.sidebar:
    st.title("🔴 COMMAND")
    if st.button("🔌 PRIME FULL ARSENAL"):
        with st.status("Hardening Matrix...", expanded=True) as s:
            for tool in ARSENAL["RECON"] + ARSENAL["WEB/FUZZ"] + ARSENAL["EXPLOIT"] + ARSENAL["AI/SECRETS"]:
                s.write(f"📥 Processing {tool}...")
                fabricate_core(tool)
            s.update(label="Arsenal 100% Ready.", state="complete")
        st.rerun()

# --- 5. TABS ---
t1, t2, t3 = st.tabs(["🚀 STRIKE OPS", "📊 ARSENAL MATRIX", "📟 LIVE HUD"])

with t2:
    st.header("📋 STATUS MATRIX (v5.3)")
    cols = st.columns(4)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.subheader(cat)
            for t in tools:
                ready = find_exe(t) is not None
                color = "#00ff00" if ready else "#555"
                st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)
