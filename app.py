import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time
import platform

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.2", layout="wide")
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

# --- 2. GLOBAL STATE ---
DEFAULTS = {
    'target': "example.com",
    'last_log': f"SYSTEM ONLINE | PY {platform.python_version()}",
    'in_scope': "example.com",
    'out_scope': ".gov, .mil",
    'battery_type': "Web2"
}
for k, v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

# --- 3. UPDATED REGISTRY ---
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

# --- 4. CORE ENGINES ---
def find_exe(name):
    """Recursive search for binary or entry script."""
    for root, _, files in os.walk(BIN_DIR):
        for target in [name, f"{name}.py", "main.py"]:
            if target in files:
                # Specialized logic for Arjun/Sqlmap folders
                if target == "main.py" and name not in root.lower(): continue
                p = os.path.join(root, target)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: return False
    try:
        r = requests.get(TOOL_URLS[tool_name], stream=True, timeout=25)
        r.raise_for_status()
        pkg_path = f"/tmp/{tool_name}_pkg"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        
        if zipfile.is_zipfile(pkg_path):
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            with tarfile.open(pkg_path, "r:*") as t: t.extractall(path=BIN_DIR)
        os.remove(pkg_path)
        return True
    except Exception as e:
        st.session_state.last_log += f"\n[!] Error {tool_name}: {str(e)}"
        return False

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", list(ARSENAL.keys()))
    st.divider()
    st.subheader("🛡️ ROE SETTINGS")
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE", st.session_state.in_scope)
    st.session_state.out_scope = st.text_area("🔴 RED ZONE", st.session_state.out_scope)
    
    if st.button("🔌 PRIME ARSENAL"):
        with st.status("Syncing Matrix...", expanded=True) as s:
            for t in ARSENAL[st.session_state.battery_type]:
                s.write(f"🧬 Fabricating {t.upper()}...")
                fabricate_core(t)
            s.update(label="Matrix Synchronized.", state="complete")
        st.rerun()

    if st.button("💀 BURN WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 6. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.2")
auth = any(allowed.strip().lower() in st.session_state.target.lower() for allowed in st.session_state.in_scope.split(",") if allowed.strip())
forbidden = any(red.strip().lower() in st.session_state.target.lower() for red in st.session_state.out_scope.split(",") if red.strip())

t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🔍 DEBUG"])

with t1:
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    if forbidden: st.error("🛑 TARGET IN RED ZONE")
    elif auth:
        st.success("✅ AUTHORIZED")
        cols = st.columns(2)
        for i, tool in enumerate(ARSENAL[st.session_state.battery_type]):
            ready = find_exe(tool) is not None
            with cols[i % 2]:
                st.checkbox(f"{tool.upper()}", value=ready, key=f"strike_{tool}")
        if st.button("🔥 EXECUTE STRIKE"):
            st.session_state.last_log = f"Strike initiated on {st.session_state.target}."
    else: st.warning("⚠️ OUT OF SCOPE")

with t2:
    for cat, tools in ARSENAL.items():
        st.subheader(cat)
        for t in tools:
            ready = find_exe(t) is not None
            st.markdown(f"<span style='color:{'#00ff00' if ready else '#555'}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)

with t4:
    st.subheader("📁 SYSTEM FILE TREE")
    if st.button("🔎 SCAN /tmp/ruby_bin"):
        files = []
        for root, _, filenames in os.walk(BIN_DIR):
            for f in filenames:
                files.append(os.path.join(root, f))
        st.code("\n".join(files) if files else "Directory Empty.")
