import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.4", layout="wide")
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

# --- 2. THE HARDENED REGISTRY (2026 LINKS) ---
ARSENAL = {
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

# Switched to direct TAGGED release links to avoid master-branch redirects
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/refs/tags/2.2.7.zip",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.94.0/trufflehog_3.94.0_linux_amd64.tar.gz",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/archive/refs/tags/1.10.3.zip",
    "commix": "https://github.com/commixproject/commix/archive/refs/tags/v4.1.zip"
}

# --- 3. CORE ENGINES ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        prospects = [name, f"{name}.py", "sqlmap.py", "commix.py", "arjun.py", "aderyn"]
        for f in files:
            if f in prospects and (name in f or name in root.lower()):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: return False
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(TOOL_URLS[tool_name], headers=headers, stream=True, timeout=30)
        r.raise_for_status()
        pkg_path = f"/tmp/{tool_name}_pkg"
        with open(pkg_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        
        if zipfile.is_zipfile(pkg_path):
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            # Handle .tar.gz and .tar.xz
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
    st.subheader("🛡️ ROE PROTECTION")
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE", st.session_state.get('in_scope', 'example.com'))
    st.session_state.out_scope = st.text_area("🔴 RED ZONE", st.session_state.get('out_scope', '.gov, .mil'))

    if st.button("🔌 PRIME ARSENAL"):
        with st.status("Injecting Binaries...", expanded=True) as s:
            for t in ARSENAL[st.session_state.battery_type]:
                s.write(f"🧬 Fabricating {t.upper()}...")
                fabricate_core(t)
            s.update(label="Matrix Synchronized.", state="complete")
        st.rerun()

    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.4")
target = st.session_state.get('target', 'example.com')
auth = any(green.strip().lower() in target.lower() for green in st.session_state.in_scope.split(",") if green.strip())
forbidden = any(red.strip().lower() in target.lower() for red in st.session_state.out_scope.split(",") if red.strip())

t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🔍 DEBUG"])

with t1:
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", target)
    if forbidden: st.error("🛑 RED ZONE DETECTED - INTERLOCK ENGAGED")
    elif auth:
        st.success("✅ AUTHORIZED")
        cols = st.columns(2)
        for i, tool in enumerate(ARSENAL[st.session_state.battery_type]):
            ready = find_exe(tool) is not None
            with cols[i % 2]:
                st.checkbox(f"{tool.upper()}", value=ready, key=f"strike_{tool}")
        if st.button("🔥 EXECUTE"):
            st.session_state.last_log = f"Launched attack on {st.session_state.target}"
    else: st.warning("⚠️ OUT OF SCOPE")

with t2:
    for cat, tools in ARSENAL.items():
        st.subheader(cat)
        for t in tools:
            ready = find_exe(t) is not None
            color = "#00ff00" if ready else "#555"
            st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.get("last_log", "SYSTEM READY.")}</div>', unsafe_allow_html=True)

with t4:
    if st.button("🔎 SYSTEM SCAN"):
        files = [os.path.join(r, f) for r, d, fs in os.walk(BIN_DIR) for f in fs]
        st.code("\n".join(files) if files else "Empty.")
