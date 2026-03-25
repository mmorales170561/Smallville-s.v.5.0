import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.7", layout="wide")
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

# --- 2. GLOBAL STATE ---
if 'battery_type' not in st.session_state: st.session_state.battery_type = "Web2"
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM REBOOTED."

# --- 3. SIDEBAR (PLACED FIRST FOR STABILITY) ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", ["Web2", "Web3", "AI Agent"])
    
    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        st.toast("Fabricating tools in background...")
        # (Fabrication logic would go here or call a function)
        
    if st.button("💀 BURN WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 4. TOOL REGISTRY ---
ARSENAL = {
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

# --- 5. ENGINES ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 6. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.7")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    cols = st.columns(3)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.write(f"**{cat}**")
            for t in tools:
                ready = find_exe(t) is not None
                st.write(f"{'✅' if ready else '❌'} {t.upper()}")

with t4:
    st.subheader("⌨️ MANUAL COMMAND DECK")
    cmd_input = st.text_input("ENTER COMMAND", "")
    if st.button("🚀 EXECUTE"):
        result = subprocess.run(cmd_input, shell=True, capture_output=True, text=True)
        st.code(f"{result.stdout}\n{result.stderr}")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
