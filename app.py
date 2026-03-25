import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil

# --- 1. STABLE HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR ", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. THE VAULT (PERSISTENCE) ---
state_keys = {'last_log': 'SYSTEM RECOVERY COMPLETE.', 'in_scope': 'example.com', 'out_scope': '.gov, .mil', 'target': '', 'battery': 'Web2'}
for k, v in state_keys.items():
    if k not in st.session_state: st.session_state[k] = v

# --- 3. CORE ENGINES ---
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
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.8")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    tools = ["subfinder", "httpx", "katana", "nuclei", "aderyn", "arjun", "trufflehog", "sqlmap"]
    cols = st.columns(4)
    for i, name in enumerate(tools):
        ready = find_exe(name) is not None
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    st.subheader("⌨️ MANUAL OVERRIDE")
    cmd_in = st.text_input("CMD >", placeholder="ls -la /tmp/ruby_bin", key="manual_cmd")
    if st.button("🚀 EXECUTE"):
        try:
            res = subprocess.run(cmd_in, shell=True, capture_output=True, text=True)
            st.code(f"OUT: {res.stdout}\nERR: {res.stderr}")
        except Exception as e:
            st.error(f"Execution Error: {e}")

with t5:
    st.subheader("🛠️ RECOVERY CONSOLE")
    if st.button("💉 FORCE INJECT ADERYN"):
        try:
            url = "
