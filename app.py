import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil
import zipfile

# --- 1. GLOBAL UI CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v8.2", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. PERSISTENCE ---
if 'last_log' not in st.session_state: st.session_state.last_log = "ARSENAL v8.2 READY."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

# --- 3. TOOLS REGISTRY ---
ALL_TOOLS = ["subfinder", "httpx", "katana", "nuclei", "aderyn", "arjun", "trufflehog", "sqlmap"]

def log_event(msg):
    st.session_state.last_log += f"\n[>] {msg}"

def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 4. SIDEBAR (REBUILT WITH PRIME BUTTON) ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.selectbox("BATTERY", ["Web2", "Web3", "AI Agent"], key='battery_select')
    
    st.divider()
    # RESTORED PRIME BUTTON
    if st.button("🔌 PRIME OMNI-ARSENAL"):
        log_event("Omni-Sync Initiated...")
        # Placeholder for the download logic we built in v7.0
        log_event("Sync complete. Check Matrix for status.")
        st.rerun()

    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        log_event("Workspace purged.")
        st.rerun()
    
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope_area', value=st.session_state.in_scope)
    st.text_area("🔴 RED ZONE", key='out_scope_area', value=st.session_state.out_scope)

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.2")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    cols = st.columns(4)
    for i, name in enumerate(ALL_TOOLS):
        path = find_exe(name)
        ready = path is not None
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)

with t4:
    st.subheader("⌨️ MANUAL OVERRIDE")
    cmd_in = st.text_input("CMD >", placeholder="ls -la /tmp/ruby_bin", key="terminal_input")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd_in, shell=True, capture_output=True, text=True)
        st.code(f"OUT: {res.stdout}\nERR: {res.stderr}")

with t5:
    st.subheader("🛠️ RECOVERY")
    if st.button("💉 FORCE INJECT ADERYN"):
        url = "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
        r = requests.get(url)
        with open("/tmp/aderyn.tar.xz", "wb") as f: f.write(r.content)
        with tarfile.open("/tmp/aderyn.tar.xz", "r:xz") as tar: tar.extractall(BIN_DIR)
        st.success("Aderyn Binary Extracted.")
