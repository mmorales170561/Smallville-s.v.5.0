import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 500px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- THE 6.0 REGISTRY (STABLE LINKS) ---
ARSENAL = {
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/v0.1.0/aderyn-x86_64-unknown-linux-gnu.tar.gz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/refs/heads/master.zip",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/refs/heads/master.zip",
    "commix": "https://github.com/commixproject/commix/archive/refs/heads/master.zip"
}

# --- ENHANCED SEARCH ENGINE ---
def find_exe(name):
    """Recursively search for binary or python entry point."""
    for root, dirs, files in os.walk(BIN_DIR):
        # Look for exact match or .py match
        for target in [name, f"{name}.py", "main.py"]:
            if target in files:
                # Avoid picking 'main.py' from the wrong tool
                if target == "main.py" and name not in root.lower():
                    continue
                p = os.path.join(root, target)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: return False
    url = TOOL_URLS[tool_name]
    try:
        r = requests.get(url, stream=True, timeout=20)
        r.raise_for_status()
        pkg_path = f"/tmp/{tool_name}_pkg"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        
        # Determine extraction type by header
        is_zip = zipfile.is_zipfile(pkg_path)
        if is_zip:
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            with tarfile.open(pkg_path, "r:*") as t: t.extractall(path=BIN_DIR)
            
        os.remove(pkg_path)
        return True
    except Exception as e:
        st.error(f"Fabrication Failed: {tool_name} -> {e}")
        return False

# --- UI LOGIC ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", list(ARSENAL.keys()))
    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        with st.status("Deep-Scanning GitHub...", expanded=True) as s:
            for t in ARSENAL[st.session_state.battery_type]:
                s.write(f"🧬 Fabricating {t.upper()}...")
                fabricate_core(t)
            s.update(label="Matrix Synchronized.", state="complete")
        st.rerun()

    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.0")
t1, t2 = st.tabs(["🚀 STRIKE", "📊 MATRIX"])

with t2:
    cols = st.columns(3)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.subheader(cat)
            for t in tools:
                ready = find_exe(t) is not None
                color = "#00ff00" if ready else "#555"
                st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)
