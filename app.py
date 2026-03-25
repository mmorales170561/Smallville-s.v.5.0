import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.9", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. THE VAULT (PERSISTENCE) ---
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM ONLINE."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

# --- 3. THE ARMORY (TOOLS) ---
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
}

def log_event(msg):
    st.session_state.last_log += f"\n[>] {msg}"

def prime_armory():
    for name, url in TOOL_URLS.items():
        log_event(f"Downloading {name}...")
        try:
            r = requests.get(url, timeout=15)
            pkg = f"/tmp/{name}.zip"
            with open(pkg, "wb") as f: f.write(r.content)
            with zipfile.ZipFile(pkg, 'r') as z: z.extractall(BIN_DIR)
            os.remove(pkg)
            log_event(f"SUCCESS: {name} installed to {BIN_DIR}")
        except Exception as e:
            log_event(f"ERROR: {name} failed -> {str(e)}")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.radio("ENVIRONMENT", ["Web2", "Web3", "AI Agent"], key='env')
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    
    if st.button("🔌 PRIME ARSENAL"):
        prime_armory()
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.9")
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    for t in TOOL_URLS.keys():
        ready = os.path.exists(os.path.join(BIN_DIR, t))
        st.write(f"{'✅' if ready else '❌'} {t.upper()}")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
