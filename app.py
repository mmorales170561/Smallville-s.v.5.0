import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. HUD CONFIGURATION (STABLE NEON) ---
st.set_page_config(page_title="RUBY-OPERATOR v2.9", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .stButton>button { background-color: #ff3131; color: #000; border: none; font-weight: bold; border-radius: 0px; width: 100%; margin-bottom: 5px; }
    .stTextInput>div>div>input { background-color: #111; color: #ff3131; border: 1px solid #444; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; font-family: monospace; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY & CORE ENGINE ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# Initialize Session States
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM READY..."
if 'target' not in st.session_state: st.session_state.target = "example.com"
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil, localhost"

def get_bin(name):
    for r, _, f in os.walk(BIN_DIR):
        if name in f: return os.path.join(r, name)
    return None

def is_authorized(target):
    target = target.lower().strip()
    if not target: return False, "🎯 Awaiting Target..."
    in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
    out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
    for forbidden in out_list:
        if forbidden in target: return False, f"🛑 FORBIDDEN: {forbidden}"
    for allowed in in_list:
        if allowed in target: return True, "✅ AUTHORIZED"
    return False, "⚠️ OUT OF SCOPE"

def fabricate_tool(tool_name, url, is_zip=False):
    try:
        with st.spinner(f"🧬 Fabricating {tool_name}..."):
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=20)
            if r.status_code != 200: return st.error(f"❌ 404: {tool_name}")
            pkg = f"/tmp/{tool_name}_pkg"
            with open(pkg, 'wb') as f: f.write(r.content)
            if is_zip:
                with zipfile.ZipFile(pkg, 'r') as z: z.extractall(BIN_DIR)
            else:
                with tarfile.open(pkg, "r:gz") as t: t.extractall(path=BIN_DIR)
            for root, _, files in os.walk(BIN_DIR):
                for f in files:
                    if f == tool_name or (f.startswith(tool_name) and "." not in f):
                        os.chmod(os.path.join(root, f), 0o755)
            st.success(f"🔋 {tool_name} Online.")
    except Exception as e: st.error(f"⚠️ Error: {str(e)}")

# --- 3. SIDEBAR: OPERATOR CONSOLE ---
with st.sidebar:
    st.title("🔴 OPERATOR")
    # Added 5th Option: Autonomous
    battery = st.selectbox("TACTICAL BATTERY", [
        "Ghost (Recon)", 
        "Strike (Nuclei)", 
        "Katana (JS Mining)", 
        "DeFi (Web3)", 
        "AUTO-STRIKE (Full Chain)"
    ])
    
    if st.button("🔌 PRIME ARMORY"):
        if battery == "Ghost (Recon)" or battery == "AUTO-STRIKE (Full Chain)":
            fabricate_tool("subfinder", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", is_zip=True)
            fabricate_tool("httpx", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", is_zip=True)
        if battery == "Strike (Nuclei)" or battery == "AUTO-STRIKE (Full Chain)":
            fabricate_tool("nuclei", "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip", is_zip=True)
        if battery == "Katana (JS Mining)":
            fabricate_tool("katana", "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip", is_zip=True)
        if battery == "DeFi (Web3)":
            fabricate_tool("aderyn", "https://github.com/Cyfrin/aderyn/releases/latest/download/aderyn-x86_64-unknown-linux-gnu.tar.gz")

    st.divider()
    # NEW: Workspace Purge Buttons
    if st.button("🗑️ CLEAR TERMINAL"):
        st.session_state.last_log = "TERMINAL PURGED..."
        st.rerun()
        
    if st.button("💀 BURN INSTANCE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        st.session_state.last_log = "MEMORY WIPED."
        st.rerun()

# --- 4. MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.0")
tabs = st.tabs(["🛡️ ROE", "🚀 STRIKE OPS", "📊 INTEL"])

with tabs[0]:
    st.header("📋 ENGAGEMENT RULES")
    c1, c2 = st.columns(2)
    with c1: st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", st.session_state.in_scope)
    with c2: st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE", st.session_state.out_scope)

with tabs[1]:
    st.header("🔫 RED KRYPTONITE GUN")
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    
    auth, msg = is_authorized(st.session_state.target)
    if auth:
        st.success(msg)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔥 START AUTO-STRIKE"):
                # Autonomous Chain Logic
                log = []
                sub_bin = get_bin("subfinder")
                htx_bin = get_bin("httpx")
                nuc_bin = get_bin("nuclei")
                
                if sub_bin and htx_bin and nuc_bin:
                    with st.status("🚀 Running Full Chain Automation...", expanded=True) as status:
                        st.write("📡 Running Subfinder...")
                        sub = subprocess.run([sub_bin, "-d", st.session_state.target, "-silent"], capture_output=True, text=True)
                        log.append(f"--- SUBDOMAINS ---\n{sub.stdout}")
                        
                        st.write("🔍 Running Httpx Probe...")
                        htx = subprocess.run(f"echo {st.session_state.target} | {htx_bin} -silent -sc -td", shell=True, capture_output=True, text=True)
                        log.append(f"--- HTTP PROBE ---\n{htx.stdout}")
                        
                        st.write("☢️ Running Nuclei Critical Scan...")
                        nuc = subprocess.run([nuc_bin, "-u", st.session_state.target, "-silent", "-severity", "critical,high"], capture_output=True, text=True)
                        log.append(f"--- NUCLEI VULNS ---\n{nuc.stdout if nuc.stdout else 'No Criticals found.'}")
                        
                        st.session_state.last_log = "\n\n".join(log)
                        status.update(label="Strike Complete!", state="complete")
                else: st.error("Missing tools. PRIME the AUTO-STRIKE battery first.")
    else:
        st.error(msg)

# --- 5. LIVE TERMINAL ---
st.divider()
st.subheader("📟 LIVE HUD")
st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
