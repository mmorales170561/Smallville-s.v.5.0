import streamlit as st
import subprocess
import os
import requests
import zipfile
import io
from datetime import datetime

# --- 1. CONFIG ---
BIN_PATH = "/tmp/smallville_bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 13px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5); border-radius: 5px;
    }
    .status-panel { padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #333; margin-bottom: 10px; }
    .online { color: #00ff41; border-color: #00ff41; background: rgba(0,255,65,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY UPDATER ---
# Updated to March 2026 Stable Releases
URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.13.0/subfinder_2.13.0_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.9.0/httpx_1.9.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.7.1/nuclei_3.7.1_linux_amd64.zip",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.5.0/katana_1.5.0_linux_amd64.zip",
    "airix": "https://github.com/projectdiscovery/airix/releases/download/v0.0.3/airix_0.0.3_linux_amd64.zip"
}

def prime_armory():
    os.makedirs(BIN_PATH, exist_ok=True)
    for name, url in URLS.items():
        try:
            r = requests.get(url, timeout=30)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            for m in z.namelist():
                if m == name or m.endswith(f"/{name}"):
                    z.extract(m, BIN_PATH)
                    # Move to flat folder if nested
                    if "/" in m: os.rename(os.path.join(BIN_PATH, m), os.path.join(BIN_PATH, name))
            os.chmod(os.path.join(BIN_PATH, name), 0o777)
        except Exception as e: st.error(f"Failed to prime {name}: {e}")

# --- 4. HUD LOGIC ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        with st.spinner("Unlocking Armory..."):
            prime_armory()
            st.rerun()

    st.divider()
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: KATANA", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
    p6 = st.toggle("P6: OLYMPUS", value=True)
    st.divider()
    stealth = st.toggle("🕵️ STEALTH MODE", value=False)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    tn = st.text_input("🎯 TARGET NAME")
    ru = st.text_input("🔗 ROOT URL")
    
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if tn and ru:
            st.session_state['terminal_logs'] = f"--- MISSION START: {tn} ---\n"
            term_placeholder = st.empty() 
            
            env = os.environ.copy()
            env.update({
                "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
                "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                "RUN_P6": "1" if p6 else "0", "RUN_STEALTH": "1" if stealth else "0"
            })
            
            subprocess.run(["chmod", "+x", SCRIPT])
            proc = subprocess.Popen(["bash", SCRIPT, "strike", ru, tn], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
            
            for line in iter(proc.stdout.readline, ""):
                st.session_state['terminal_logs'] += line
                term_placeholder.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
            proc.wait()
