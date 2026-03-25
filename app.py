import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.4", layout="wide")
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

# --- 2. THE FINDER ENGINE ---
def find_exe(name):
    """Recursively search for binary/script and fix permissions."""
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            # Match specific tool names or python entry points
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755) # Force executable permissions
                return p
    return shutil.which(name)

def run_shell(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
        return f"OUT: {result.stdout}\nERR: {result.stderr}"
    except Exception as e:
        return f"CRITICAL ERROR: {str(e)}"

# --- 3. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.4")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("FULL ASSET DISPOSAL")
    categories = {
        "Web2": ["subfinder", "httpx", "katana", "nuclei"],
        "Web3": ["aderyn", "arjun"],
        "AI Agent": ["trufflehog", "sqlmap"]
    }
    for cat, tools in categories.items():
        with st.expander(f"📂 {cat}", expanded=True):
            cols = st.columns(len(tools))
            for i, name in enumerate(tools):
                path = find_exe(name)
                ready = path is not None
                cols[i].write(f"{'✅' if ready else '❌'} {name.upper()}")
                if ready: cols[i].caption(f"Binary Linked")

with t5:
    st.subheader("⚡ TACTICAL RECOVERY CONSOLE")
    st.warning("Pip failed for Aderyn. Use 'BINARY INJECT' below instead.")
    
    col1, col2 = st.columns(2)
    with col1:
        # NEW BINARY INJECTION FOR ADERYN
        if st.button("💉 BINARY INJECT: ADERYN"):
            # This pulls the actual Linux binary, skips Python/Pip entirely
            cmd = (
                f"wget https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz -O {BIN_DIR}/aderyn.tar.xz && "
                f"tar -xvf {BIN_DIR}/aderyn.tar.xz -C {BIN_DIR} && "
                f"chmod +x {BIN_DIR}/aderyn"
            )
            st.code(run_shell(cmd))
            
        if st.button("💉 FORCE SQLMAP"):
            st.code(run_shell(f"git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git {BIN_DIR}/sqlmap_git"))

    with col2:
        if st.button("💉 FORCE TRUFFLEHOG"):
            cmd = (
                f"wget https://github.com/trufflesecurity/trufflehog/releases/download/v3.94.0/trufflehog_3.94.0_linux_amd64.tar.gz -O {BIN_DIR}/th.tar.gz && "
                f"tar -xzf {BIN_DIR}/th.tar.gz -C {BIN_DIR} && "
                f"chmod +x {BIN_DIR}/trufflehog"
            )
            st.code(run_shell(cmd))
            
        if st.button("💉 FORCE ARJUN"):
            # Trying git clone instead of pip for Arjun as well
            st.code(run_shell(f"git clone --depth 1 https://github.com/s0md3v/Arjun.git {BIN_DIR}/arjun_git"))

    st.divider()
    if st.button("🔎 DEEP SCAN WORKSPACE"):
        files = [os.path.join(r, f) for r, d, f in os.walk(BIN_DIR) for f in f]
        st.code("\n".join(files) if files else "Empty.")

with t4:
    st.subheader("⌨️ MANUAL OVERRIDE")
    cmd_in = st.text_input("CMD_DIR: /tmp/ruby_bin >")
    if st.button("🚀 EXECUTE"):
        st.code(run_shell(f"cd {BIN_DIR} && {cmd_in}"))
