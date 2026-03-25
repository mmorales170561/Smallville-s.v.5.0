import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.3", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. THE RE-VERIFIED REGISTRY ---
ARSENAL = {
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

# Switched to Raw Master Zips for Python tools
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/v0.1.0/aderyn-x86_64-unknown-linux-gnu.tar.gz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/master.zip",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/master.zip",
    "commix": "https://github.com/commixproject/commix/archive/master.zip"
}

# --- 3. CORE ENGINES ---
def find_exe(name):
    """Recursive scan for tool entry points."""
    for root, _, files in os.walk(BIN_DIR):
        # Specific mapping for tools that use entry scripts
        prospects = [name, f"{name}.py", "sqlmap.py", "commix.py", "arjun.py", "aderyn"]
        for f in files:
            if f in prospects and (name in f or name in root.lower()):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    """Aggressive fetch and unpack."""
    if tool_name not in TOOL_URLS: return False
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(TOOL_URLS[tool_name], headers=headers, stream=True, timeout=30)
        r.raise_for_status()
        pkg_path = f"/tmp/{tool_name}_download"
        with open(pkg_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Determine extraction method
        if zipfile.is_zipfile(pkg_path):
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            with tarfile.open(pkg_path, "r:*") as t: t.extractall(path=BIN_DIR)
        
        os.remove(pkg_path)
        return True
    except Exception as e:
        st.error(f"Failed {tool_name}: {e}")
        return False

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", list(ARSENAL.keys()))
    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        with st.status("Reconstructing Matrix...", expanded=True) as s:
            for t in ARSENAL[st.session_state.battery_type]:
                s.write(f"🧬 Injecting {t.upper()}...")
                fabricate_core(t)
            s.update(label="Arsenal Synchronized.", state="complete")
        st.rerun()
    if st.button("💀 BURN WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.3")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🔍 DEBUG"])

with t1:
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    st.write("---")
    selected = []
    current_tools = ARSENAL[st.session_state.battery_type]
    cols = st.columns(2)
    for i, tool in enumerate(current_tools):
        ready = find_exe(tool) is not None
        with cols[i % 2]:
            if st.checkbox(f"{tool.upper()}", value=ready, key=f"s_{tool}"):
                selected.append(tool)
    if st.button("🔥 FIRE"):
        st.session_state.last_log = f"Launched {len(selected)} tools at {st.session_state.target}"

with t2:
    for cat, tools in ARSENAL.items():
        st.subheader(cat)
        for t in tools:
            ready = find_exe(t) is not None
            color = "#00ff00" if ready else "#555"
            st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)

with t4:
    if st.button("🔎 DEEP SCAN"):
        files = []
        for root, _, filenames in os.walk(BIN_DIR):
            for f in filenames: files.append(os.path.join(root, f))
        st.code("\n".join(files) if files else "Workspace Empty.")
