import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil

# --- 1. GLOBAL TOOL URLS (Defined at top to prevent syntax errors) ---
ADERYN_URL = "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
TRUFFLE_URL = "https://github.com/trufflesecurity/trufflehog/releases/download/v3.94.0/trufflehog_3.94.0_linux_amd64.tar.gz"

# --- 2. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.9", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 3. PERSISTENCE ---
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM STABILIZED."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

# --- 4. CORE ENGINES ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.selectbox("BATTERY", ["Web2", "Web3", "AI Agent"], key='battery')
    st.divider()
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 6. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.9")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    tools = ["subfinder", "httpx", "katana", "nuclei", "aderyn", "arjun", "trufflehog", "sqlmap"]
    cols = st.columns(4)
    for i, name in enumerate(
