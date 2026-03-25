import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. HUD CONFIG (NO-FAIL SETTINGS) ---
st.set_page_config(page_title="RUBY-OPERATOR v5.8", layout="wide")
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

# --- 2. GLOBAL STATE ---
if 'target' not in st.session_state: st.session_state.target = "example.com"
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM REBOOTED. STANDING BY."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"
if 'battery_type' not in st.session_state: st.session_state.battery_type = "Web2"

# --- 3. THE REGISTRY ---
ARSENAL = {
    "Web2": ["subfinder", "amass", "httpx", "waybackurls", "gau", "ffuf", "katana", "dalfox"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "gitleaks", "sqlmap", "commix"]
}

# Verified Links
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip",
    "amass": "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/refs/heads/master.zip",
    "commix": "https://github.com/commixproject/commix/archive/refs/heads/master.zip"
}

# --- 4. CORE FUNCTIONS ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py":
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: return False
    url = TOOL_URLS[tool_name]
    try:
        r = requests.get(url, stream=True, timeout=20)
        pkg_path = f"/tmp/{tool_name}_pkg"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        try:
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        except:
            try:
                with tarfile.open(pkg_path, "r:*") as t: t.extractall(path=BIN_DIR)
            except: return False
        os.remove(pkg_path)
        return True
    except: return False

# --- 5. SIDEBAR (CORRECTED LINE 103) ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", ["Web2", "Web3", "AI Agent"])
    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        with st.status("Fabricating...", expanded=True) as s:
            for t in ARSENAL[st.session_state.battery_type]:
                fabricate_core(t)
            s.update(label="Ready.", state="complete")
        st.rerun()

# --- 6. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 5.8")
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD"])

with t1:
    st.session_state.target = st.text_input("🎯 TARGET", st.session_state.target)
    if st.button("🔥 FIRE"):
        st.session_state.last_log = f"STRIKE INITIATED ON {st.session_state.target}"

with t2:
    for cat, tools in ARSENAL.items():
        st.subheader(cat)
        for t in tools:
            ready = find_exe(t) is not None
            st.write(f"{'✅' if ready else '❌'} {t.upper()}")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
