import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
from datetime import datetime

# --- 1. HUD CONFIGURATION ---
st.set_page_config(page_title="RUBY-OPERATOR v2.6", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff3131; }
    .stButton>button { background-color: #ff3131; color: #000; border: none; font-weight: bold; border-radius: 0px; }
    .stTextInput>div>div>input { background-color: #111; color: #ff3131; border: 1px solid #444; }
    .terminal { background-color: #050505; color: #00ff00; padding: 15px; border: 1px solid #333; font-family: monospace; height: 300px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)

# Initialize Session States
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM IDLE..."
if 'target' not in st.session_state: st.session_state.target = "example.com"

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
            st.success(f"🔋 {tool_name} Ready.")
    except Exception as e: st.error(f"⚠️ Error: {str(e)}")

# --- 3. SIDEBAR: OPERATOR CONSOLE ---
with st.sidebar:
    st.title("🔴 RUBY-OPERATOR")
    battery = st.selectbox("TACTICAL BATTERY", ["Ghost (Recon)", "DeFi (Web3)"])
    if st.button("🔌 PRIME ARMORY"):
        if battery == "Ghost (Recon)":
            fabricate_tool("subfinder", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", is_zip=True)
            fabricate_tool("httpx", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", is_zip=True)
    st.divider()
    if st.button("💀 BURN INSTANCE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        st.rerun()

# --- 4. THE MISSION CONTROL ---
tabs = st.tabs(["🚀 STRIKE OPS", "📊 INTELLIGENCE", "🧪 PAYLOAD LAB"])

with tabs[0]: # STRIKE OPS
    st.header("🔫 RED KRYPTONITE GUN")
    # Store target in session state to prevent 't_url' not defined errors
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    
    col1, col2 = st.columns(2)
    def get_bin(name):
        for r, _, f in os.walk(BIN_DIR):
            if name in f: return os.path.join(r, name)
        return None

    with col1:
        if st.button("🔥 FIRE: SUBFINDER"):
            cmd = get_bin("subfinder")
            if cmd:
                with st.spinner("Recon..."):
                    res = subprocess.run([cmd, "-d", st.session_state.target, "-silent"], capture_output=True, text=True)
                    st.session_state.last_log = res.stdout if res.stdout else "No subdomains found."
            else: st.error("Prime Armory First.")

    with col2:
        if st.button("🔥 FIRE: HTTPX PROBE"):
            cmd = get_bin("httpx")
            if cmd:
                with st.spinner("Probing..."):
                    res = subprocess.run(f"echo {st.session_state.target} | {cmd} -silent -sc -td", shell=True, capture_output=True, text=True)
                    st.session_state.last_log = res.stdout if res.stdout else "No HTTP response."
            else: st.error("Prime Armory First.")

# --- 5. LIVE HUD ---
st.divider()
st.subheader("📟 LIVE TERMINAL")
st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)

with tabs[2]: # PAYLOAD LAB
    st.header("🧪 FUZZING PROFILES")
    st.info("Generating Directory Fuzz List...")
    fuzz_list = [".env", ".git/config", "api/v1/user", "admin/login", "wp-config.php", "config.json"]
    st.code("\n".join(fuzz_list), language="bash")
    
    if st.button("💉 INJECT FUZZ LIST"):
        cmd = get_bin("httpx")
        if cmd:
            with st.spinner("Fuzzing..."):
                # Simulating a multi-path probe
                paths = ",".join(fuzz_list)
                res = subprocess.run(f"echo {st.session_state.target} | {cmd} -path {paths} -sc", shell=True, capture_output=True, text=True)
                st.session_state.last_log = res.stdout
        else: st.error("Prime Armory First.")
