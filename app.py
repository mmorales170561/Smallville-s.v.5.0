import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.5", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. TOOLS & LINKS ---
ARSENAL = {
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/refs/heads/master.zip",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.94.0/trufflehog_3.94.0_linux_amd64.tar.gz",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/refs/heads/master.zip",
    "commix": "https://github.com/commixproject/commix/archive/refs/heads/master.zip"
}

# --- 3. THE FINDER ENGINE ---
def find_exe(name):
    """Deep scan for the tool. Returns the absolute path."""
    for root, dirs, files in os.walk(BIN_DIR):
        # Look for the binary or the main python script
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py") or (name == "commix" and f == "commix.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: return False
    try:
        r = requests.get(TOOL_URLS[tool_name], stream=True, timeout=30)
        pkg_path = f"/tmp/{tool_name}_download"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        
        # Extraction with error catching
        if zipfile.is_zipfile(pkg_path):
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            try:
                with tarfile.open(pkg_path, "r:*") as t: t.extractall(path=BIN_DIR)
            except: return False
            
        os.remove(pkg_path)
        return True
    except: return False

# --- 4. UI ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", list(ARSENAL.keys()))
    if st.button("🔌 PRIME ARSENAL"):
        with st.status("Injecting Tools...", expanded=True) as s:
            for t in ARSENAL[st.session_state.battery_type]:
                s.write(f"🧬 Fabricating {t}...")
                fabricate_core(t)
            s.update(label="Sync Complete.", state="complete")
        st.rerun()
    if st.button("💀 BURN WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

st.title("🏹 SMALLVILLE S.V. 6.5")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🔍 DEBUG"])

with t2: # Matrix Status
    for cat, tools in ARSENAL.items():
        st.subheader(cat)
        for t in tools:
            exe_path = find_exe(t)
            ready = exe_path is not None
            color = "#00ff00" if ready else "#555"
            st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)
            if ready: st.caption(f"Path: {exe_path}")

with t4: # Debugger
    if st.button("🔎 DEEP SCAN"):
        all_files = []
        for r, d, f in os.walk(BIN_DIR):
            for file in f: all_files.append(os.path.join(r, file))
        st.code("\n".join(all_files) if all_files else "Workspace Empty.")
