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
    .stButton>button { background-color: #ff3131; color: #000; border: none; font-weight: bold; border-radius: 0px; width: 100%; }
    .stTextInput>div>div>input { background-color: #111; color: #ff3131; border: 1px solid #444; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000; gap: 10px; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #ff3131 !important; color: #ff3131 !important; }
    code { color: #00ff00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY (Binary Fabrication) ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)

def fabricate_tool(tool_name, url, is_zip=False):
    """Hardened downloader to bypass 404s and corrupted zips."""
    path = os.path.join(BIN_DIR, tool_name)
    if not os.path.exists(path):
        try:
            with st.spinner(f"🧬 Fabricating {tool_name}..."):
                # Use a browser-like User-Agent to prevent bot-blocking 403/404s
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=headers, stream=True, timeout=20)
                
                if r.status_code != 200:
                    st.error(f"❌ Misfire: {tool_name} returned {r.status_code}. Check link.")
                    return

                local_file = f"/tmp/{tool_name}_pkg"
                with open(local_file, 'wb') as f:
                    f.write(r.content)
                
                if is_zip:
                    with zipfile.ZipFile(local_file, 'r') as z:
                        z.extractall(BIN_DIR)
                else:
                    with tarfile.open(local_file, "r:gz") as t:
                        t.extractall(path=BIN_DIR)
                
                # Standardize binary location: find the file and move it to BIN_DIR root
                for root, dirs, files in os.walk(BIN_DIR):
                    for f in files:
                        if f == tool_name or f.startswith(tool_name):
                            full_p = os.path.join(root, f)
                            os.chmod(full_p, 0o755)
                            # Link to main bin path for easy calling
                            if full_p != path:
                                shutil.copy2(full_p, path)
                
                st.success(f"🔋 {tool_name} Online.")
        except Exception as e:
            st.error(f"⚠️ Fabrication Error: {str(e)}")

# --- 3. SIDEBAR: OPERATOR CONSOLE ---
with st.sidebar:
    st.title("🔴 RUBY-OPERATOR")
    st.caption("v2.6 Cloud-Native Offensive Framework")
    
    battery = st.selectbox("TACTICAL BATTERY", ["Ghost (Recon)", "DeFi (Web3)", "Modern (AI/ID)"])
    
    if st.button("🔌 PRIME ARMORY"):
        if battery == "Ghost (Recon)":
            # Updated Stable 2026 Links
            fabricate_tool("subfinder", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", is_zip=True)
            fabricate_tool("httpx", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", is_zip=True)
        elif battery == "DeFi (Web3)":
