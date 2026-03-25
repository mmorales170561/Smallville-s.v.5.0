import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import platform

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.6", layout="wide")
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
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

# --- 3. HELPER ENGINES ---
def run_cmd(cmd):
    try:
        # Run command and capture both output and error
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return f"{result.stdout}\n{result.stderr}"
    except Exception as e:
        return f"[!] EXECUTION ERROR: {str(e)}"

def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 4. MAIN UI ---
st.title("🏹 SMALLVILLE S.V. 6.6")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

with t2: # Matrix Status
    st.subheader("SYSTEM INTEGRITY")
    cols = st.columns(3)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.write(f"**{cat}**")
            for t in tools:
                ready = find_exe(t) is not None
                st.write(f"{'✅' if ready else '❌'} {t.upper()}")

with t4: # The Manual Installer / Terminal
    st.subheader("⌨️ MANUAL COMMAND DECK")
    st.info("Direct access to /tmp/ruby_bin. Use for manual installs.")
    
    cmd_input = st.text_input("ENTER COMMAND (e.g., pip install sqlmap --target /tmp/ruby_bin)", "")
    if st.button("🚀 EXECUTE"):
        with st.spinner("Executing..."):
            output = run_cmd(f"cd {BIN_DIR} && {cmd_input}")
            st.code(output)

    st.divider()
    st.subheader("📂 WORKSPACE EXPLORER")
    if st.button("🔎 RE-SCAN DIRECTORY"):
        files = []
        for r, d, f in os.walk(BIN_DIR):
            for file in f: files.append(os.path.join(r, file))
        st.code("\n".join(files) if files else "Workspace Empty.")

with t3: # HUD
    st.markdown('<div class="terminal">SYSTEM READY. WAITING FOR INPUT...</div>', unsafe_allow_html=True)
