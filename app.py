import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time
from datetime import datetime

# --- 1. SAFE PDF IMPORT ---
PDF_ENABLED = False
try:
    from fpdf import FPDF
    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False

# --- 2. GLOBAL STATE ---
INITIAL_STATE = {
    'target': "example.com",
    'last_log': "SYSTEM ONLINE. ARSENAL V5.5 READY.",
    'in_scope': "example.com",
    'out_scope': ".gov, .mil, localhost",
    'battery_type': "Web2"
}

for key, val in INITIAL_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 3. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v5.5", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 500px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    .stCheckbox { color: #00ff00 !important; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 4. THE COMPLETE 22+ TOOL REGISTRY ---
ARSENAL = {
    "Web2": ["subfinder", "amass", "httpx", "waybackurls", "gau", "assetfinder", "ffuf", "katana", "dalfox", "dirsearch"],
    "Web3": ["aderyn", "slither", "mythril", "arjun"],
    "AI Agent": ["trufflehog", "gitleaks", "garak", "pyrit", "sqlmap", "commix", "tplimap"]
}

TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip",
    "waybackurls": "https://github.com/tomnomnom/waybackurls/archive/refs/heads/master.zip",
    "gau": "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz",
    "assetfinder": "https://github.com/tomnomnom/assetfinder/releases/download/v0.1.1/assetfinder-linux-amd64-0.1.1.tgz",
    "amass": "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "dalfox": "https://github.com/hahwul/dalfox/releases/download/v2.9.0/dalfox_2.9.0_linux_amd64.tar.gz",
    "dirsearch": "https://github.com/maurosoria/dirsearch/archive/refs/heads/master.zip",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/tarball/master",
    "commix": "https://github.com/commixproject/commix/tarball/master",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "gitleaks": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.2/gitleaks_8.18.2_linux_x64.tar.gz",
    "arjun": "https://github.com/s0md3v/Arjun/archive/refs/heads/master.zip"
}

# --- 5. ENHANCED ENGINES ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py":
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS:
        if tool_name in ["garak", "pyrit", "slither", "mythril", "aderyn"]:
            try: subprocess.run(["pip", "install", tool_name, "--quiet"], check=True); return True
            except: return False
        return False
    url = TOOL_URLS[tool_name]
    try:
        r = requests.get(url, stream=True, timeout=20)
        ext = ".zip" if "zip" in url or "master" in url or "ball" in url else ".tar.gz"
        pkg_path = f"/tmp/{tool_name}{ext}"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        if "zip" in ext:
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            with tarfile.open(pkg_path, "r:gz") as t: t.extractall(path=BIN_DIR)
        os.remove(pkg_path)
        return True
    except: return False

def is_authorized(target):
    target = target.lower().strip()
    if not target: return False, "🎯 Awaiting Sector..."
    out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
    in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
    for f in out_list:
        if f in target: return False, f"🛑 FORBIDDEN: {f}"
    for a in in_list:
        if a in target: return True, "✅ AUTHORIZED"
    return False, "⚠️ OUT OF SCOPE"

# --- 6. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", ["Web2", "Web3", "AI Agent"])
    st.divider()
    st.subheader("🛡️ ROE SETTINGS")
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE", st.session_state.in_scope)
    st.session_state.out_scope = st.text_area("🔴 RED ZONE", st.session_state.out_scope)
    st.divider()
    if st.button("🔌 PRIME FULL ARSENAL"):
        with st.status("Hardening Matrix...", expanded=True) as s:
            all_tools = [t for cat in ARSENAL.values() for t in cat]
            for tool in set(all_tools):
                s.write(f"📦 Processing {tool}...")
                fabricate_core(tool); time.sleep(0.1)
            s.update(label="Arsenal 100% Ready.", state="complete")
        st.rerun()

# --- 7. MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.5")
auth, msg = is_authorized(st.session_state.target)
t1, t2, t3 = st.tabs(["🚀 STRIKE OPS", "📊 ARSENAL MATRIX", "📟 LIVE HUD"])

with t1: # STRIKE OPS
    st.header(f"🔫 {st.session_state.battery_type.upper()} ENGAGEMENT")
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    
    if auth:
        st.subheader("🛠️ SELECT YOUR ARSENAL")
        current_tools = ARSENAL[st.session_state.battery_type]
        selected_tools = []
        cols = st.columns(3)
        for i, tool in enumerate(current_tools):
            ready = find_exe(tool) is not None
            with cols[i % 3]:
                if st.checkbox(f"{'✅' if ready else '❌'} {tool.upper()}", value=ready, disabled=not ready, key=f"check_{tool}"):
                    selected_tools.append(tool)
        
        st.divider()
        if st.button("🔥 INITIATE STRIKE"):
            final_out = []
            with st.status(f"Executing {len(selected_tools)} Tool Strike...", expanded=True) as s:
                for tool in selected_tools:
                    exe = find_exe(tool)
                    s.write(f"🚀 Firing {tool.upper()}...")
                    cmd = [exe, "-u", st.session_state.target] if tool not in ["subfinder", "amass", "trufflehog"] else [exe, "-d", st.session_state.target]
                    if tool == "trufflehog": cmd = [exe, "git", st.session_state.target, "--only-verified"]
                    try:
                        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                        final_out.append(f"=== {tool.upper()} ===\n{res.stdout}")
                    except: final_out.append(f"❌ {tool.upper()} Failed or Timed Out.")
                st.session_state.last_log = "\n\n".join(final_out)
            st.rerun()
    else: st.error(msg)

with t2: # ARSENAL MATRIX
    st.header("📋 STATUS MATRIX")
    cols = st.columns(3)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.subheader(cat)
            for t in tools:
                ready = find_exe(t) is not None
                st.markdown(f"<span style='color:{'#00ff00' if ready else '#555'}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)

with t3: # LIVE HUD
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
