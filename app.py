import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.3", layout="wide")
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

# --- 2. REGISTRY ---
ARSENAL = {
    "Web2 (Recon)": ["subfinder", "httpx", "katana", "nuclei"],
    "Web3 (Blockchain)": ["aderyn", "arjun"],
    "AI Agents (Automated)": ["trufflehog", "sqlmap"]
}

# --- 3. CORE ENGINES ---
def run_shell(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return f"OUT: {result.stdout}\nERR: {result.stderr}"
    except Exception as e:
        return f"CRITICAL ERROR: {str(e)}"

def find_exe(name):
    """Deep scan for binaries or python entry points."""
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            # Match tool name, .py files, or specific entry points
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py") or (name == "arjun" and f == "arjun.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery = st.selectbox("BATTERY", list(ARSENAL.keys()))
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', value=st.session_state.get('in_scope', 'example.com'))
    st.text_area("🔴 RED ZONE", key='out_scope', value=st.session_state.get('out_scope', '.gov, .mil'))
    
    if st.button("🔌 PRIME ARSENAL"):
        # Automated prime logic...
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.3")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("FULL ASSET DISPOSAL")
    for cat, tools in ARSENAL.items():
        with st.expander(f"📂 {cat}", expanded=True):
            cols = st.columns(len(tools))
            for i, name in enumerate(tools):
                path = find_exe(name)
                ready = path is not None
                cols[i].write(f"{'✅' if ready else '❌'} {name.upper()}")
                if ready: cols[i].caption(f"Path Found")

with t4:
    st.subheader("⌨️ MANUAL OVERRIDE")
    cmd_in = st.text_input("CMD_DIR: /tmp/ruby_bin >")
    if st.button("🚀 EXECUTE"):
        st.code(run_shell(f"cd {BIN_DIR} && {cmd_in}"))

with t5:
    st.subheader("⚡ TACTICAL RECOVERY CONSOLE")
    st.info("Force-inject missing tools into the workspace.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💉 FORCE SQLMAP"):
            st.code(run_shell(f"git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git {BIN_DIR}/sqlmap_git"))
        if st.button("💉 FORCE ARJUN"):
            st.code(run_shell(f"pip install arjun --target {BIN_DIR}"))
    with col2:
        if st.button("💉 FORCE TRUFFLEHOG"):
            st.code(run_shell(f"wget https://github.com/trufflesecurity/trufflehog/releases/download/v3.94.0/trufflehog_3.94.0_linux_amd64.tar.gz -O {BIN_DIR}/th.tar.gz && tar -xzf {BIN_DIR}/th.tar.gz -C {BIN_DIR}"))
        if st.button("💉 FORCE ADERYN"):
            st.code(run_shell(f"pip install aderyn --target {BIN_DIR}"))

    st.divider()
    if st.button("🔎 DEEP SCAN WORKSPACE"):
        files = [os.path.join(r, f) for r, d, f in os.walk(BIN_DIR) for f in f]
        st.code("\n".join(files) if files else "Empty.")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.get("last_log", "SYSTEM ONLINE.")}</div>', unsafe_allow_html=True)
