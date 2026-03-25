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
    code { color: #00ff00 !important; background-color: #111 !important; }
    .terminal { background-color: #050505; color: #00ff00; padding: 15px; border: 1px solid #333; font-family: monospace; height: 250px; overflow-y: scroll; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY (Fabrication Engine) ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)

def fabricate_tool(tool_name, url, is_zip=False):
    """Hardened downloader for volatile environments."""
    try:
        with st.spinner(f"🧬 Fabricating {tool_name}..."):
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, stream=True, timeout=20)
            if r.status_code != 200:
                st.error(f"❌ Misfire: {tool_name} (Status {r.status_code})")
                return

            pkg = f"/tmp/{tool_name}_pkg"
            with open(pkg, 'wb') as f:
                f.write(r.content)
            
            if is_zip:
                with zipfile.ZipFile(pkg, 'r') as z:
                    z.extractall(BIN_DIR)
            else:
                with tarfile.open(pkg, "r:gz") as t:
                    t.extractall(path=BIN_DIR)
            
            # Recursive permission grant
            for root, dirs, files in os.walk(BIN_DIR):
                for f in files:
                    if f == tool_name or (f.startswith(tool_name) and "." not in f):
                        os.chmod(os.path.join(root, f), 0o755)
            st.success(f"🔋 {tool_name} Ready.")
    except Exception as e:
        st.error(f"⚠️ Fabrication Error: {str(e)}")

# --- 3. SIDEBAR: OPERATOR CONSOLE ---
with st.sidebar:
    st.title("🔴 RUBY-OPERATOR")
    st.caption("v2.6 Cloud-Native Strike Kit")
    
    battery = st.selectbox("TACTICAL BATTERY", ["Ghost (Recon)", "DeFi (Web3)"])
    
    if st.button("🔌 PRIME ARMORY"):
        if battery == "Ghost (Recon)":
            fabricate_tool("subfinder", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", is_zip=True)
            fabricate_tool("httpx", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", is_zip=True)
        elif battery == "DeFi (Web3)":
            fabricate_tool("aderyn", "https://github.com/Cyfrin/aderyn/releases/latest/download/aderyn-x86_64-unknown-linux-gnu.tar.gz")
            
    st.divider()
    if st.button("🔍 DIAGNOSTICS"):
        st.info(f"Path: {BIN_DIR}")
        if os.path.exists(BIN_DIR):
            st.write(os.listdir(BIN_DIR))
            
    if st.button("💀 BURN INSTANCE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        st.rerun()

# --- 4. THE MISSION CONTROL ---
tabs = st.tabs(["🚀 STRIKE OPS", "📊 INTELLIGENCE", "🧪 PAYLOAD LAB"])

with tabs[0]:
    st.header("🔫 THE RED KRYPTONITE GUN")
    t_url
