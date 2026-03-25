import streamlit as st
import subprocess
import os
import requests
import zipfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.1", layout="wide")
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

# --- 2. OMNI-ARSENAL REGISTRY ---
# This is your full list of assets at your disposal
ARSENAL = {
    "Web2 (Recon)": {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip"
    },
    "Web3 (Blockchain)": {
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz",
        "arjun": "https://github.com/s0md3v/Arjun/archive/refs/tags/2.2.7.zip"
    },
    "AI Agents (Automated)": {
        "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.94.0/trufflehog_3.94.0_linux_amd64.tar.gz",
        "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/refs/tags/1.10.3.zip"
    }
}

# --- 3. PERSISTENCE ---
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM OMNI-BATTERY ONLINE."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

def log_event(msg):
    st.session_state.last_log += f"\n[>] {msg}"

def prime_all_batteries():
    with st.status("Syncing Global Armory...", expanded=True) as s:
        for category, tools in ARSENAL.items():
            for name, url in tools.items():
                s.write(f"🧬 Fabricating {name}...")
                try:
                    r = requests.get(url, timeout=10)
                    pkg = f"/tmp/{name}.pkg"
                    with open(pkg, "wb") as f: f.write(r.content)
                    # Simple extraction logic (needs adjustment for .tar.xz/.zip based on suffix)
                    # For demo purposes assuming standard zip handling
                    log_event(f"SUCCESS: {name} Primed.")
                except Exception as e:
                    log_event(f"FAIL: {name} -> {str(e)}")
        s.update(label="All Batteries Synchronized.", state="complete")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    # THE SWITCHER IS BACK
    st.session_state.current_battery = st.selectbox("SELECT BATTERY", list(ARSENAL.keys()))
    
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    
    st.divider()
    if st.button("🔌 PRIME OMNI-ARSENAL"):
        prime_all_batteries()
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.1")
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD"])

with t2:
    st.subheader("FULL ASSET DISPOSAL")
    for category, tools in ARSENAL.items():
        with st.expander(f"📂 {category}", expanded=True):
            cols = st.columns(len(tools))
            for i, (name, url) in enumerate(tools.items()):
                ready = os.path.exists(os.path.join(BIN_DIR, name))
                cols[i].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t1:
    st.subheader(f"ACTIVE: {st.session_state.current_battery}")
    st.text_input("TARGET SECTOR", key='target')
    # Strike logic here...

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
