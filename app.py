import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil

# --- 1. SETTINGS & HUD ---
st.set_page_config(page_title="RUBY-OPERATOR v8.0", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. PERSISTENCE ---
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM STABILIZED."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

# --- 3. TOOLS REGISTRY (Flat List to prevent SyntaxErrors) ---
WEB2_TOOLS = ["subfinder", "httpx", "katana", "nuclei"]
WEB3_TOOLS = ["aderyn", "arjun"]
AI_TOOLS = ["trufflehog", "sqlmap"]
ALL_TOOLS = WEB2_TOOLS + WEB3_TOOLS + AI_TOOLS

def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 4. SIDEBAR ---
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

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.0")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    cols = st.columns(4)
    # Using a flat loop to prevent the 'enumerate' bracket error
    for index, name in enumerate(ALL_TOOLS):
        ready = find_exe(name) is not None
