import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.2", layout="wide")
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
ARSENAL = {
    "Web2 (Recon)": ["subfinder", "httpx", "katana", "nuclei"],
    "Web3 (Blockchain)": ["aderyn", "arjun"],
    "AI Agents (Automated)": ["trufflehog", "sqlmap"]
}

# --- 3. PERSISTENCE ---
state_keys = {'last_log': 'SYSTEM ONLINE.', 'in_scope': 'example.com', 'out_scope': '.gov, .mil', 'target': ''}
for k, v in state_keys.items():
    if k not in st.session_state: st.session_state[k] = v

def find_exe(name):
    """Deep scan for binaries or python entry points."""
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
    st.session_state.current_battery = st.selectbox("SELECT BATTERY", list(ARSENAL.keys()))
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    
    if st.button("🔌 PRIME OMNI-ARSENAL"):
        st.session_state.last_log += "\n[>] Initiating Omni-Sync..."
        # Simplified placeholder for the auto-prime logic
        st.rerun()

    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.2")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("FULL ASSET DISPOSAL")
    for category, tools in ARSENAL.items():
        with st.expander(f"📂 {category}", expanded=True):
            cols = st.columns(len(tools))
            for i, name in enumerate(tools):
                ready = find_exe(name) is not None
                cols[i].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    st.subheader("⌨️ MANUAL COMMAND DECK")
    cmd = st.text_input("ENTER OVERRIDE (e.g., pip install sqlmap --target /tmp/ruby_bin)", "")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.code(f"STDOUT:\n{res.stdout}\n\nSTDERR:\n{res.stderr}")

with t5:
    st.subheader("📁 DIRECTORY FORENSICS")
    if st.button("🔎 SCAN /tmp/ruby_bin"):
        files = []
        for r, d, f in os.walk(BIN_DIR):
            for file in f: files.append(os.path.join(r, file))
        st.code("\n".join(files) if files else "Directory is empty.")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
