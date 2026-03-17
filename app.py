import streamlit as st
import subprocess
import os
import requests
import zipfile
import io
import stat
from datetime import datetime

# --- 1. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

# Persistent state for logs
if 'terminal_logs' not in st.session_state: 
    st.session_state['terminal_logs'] = "READY FOR ENGAGEMENT..."

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 550px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5); border-radius: 5px;
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 2px solid #333; }
    .online { background-color: rgba(0, 255, 65, 0.1); border-color: #00ff41 !important; color: #00ff41; box-shadow: 0 0 10px #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border-color: #ff0000 !important; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY STATUS CHECK ---
def check_armory():
    try:
        if not os.path.exists(BIN_PATH): return False
        tools = ["subfinder", "httpx", "nuclei"]
        return all(os.path.isfile(os.path.join(BIN_PATH, t)) for t in tools)
    except: return False

is_ready = check_armory()

# --- 4. SIDEBAR (MISSION LOGS RESTORED) ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if is_ready:
        st.markdown('<div class="status-panel online"><b>SYSTEMS ONLINE</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-panel offline"><b>SYSTEMS OFFLINE</b></div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", use_container_width=True):
        with st.spinner("🔓 Breaking Permission Locks..."):
            os.makedirs(BIN_PATH, mode=0o777, exist_ok=True)
            tools = {
                "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
                "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
                "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip"
            }
            for name, url in tools.items():
                try:
                    r = requests.get(url, timeout=30)
                    if r.status_code == 200:
                        z = zipfile.ZipFile(io.BytesIO(r.content))
                        for member in z.namelist():
                            z.extract(member, BIN_PATH)
                            os.chmod(os.path.join(BIN_PATH, member), 0o777)
                        st.write(f"✅ {name} Armed")
                except: pass
            st.rerun()

    st.divider()
    st.subheader("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: HOOK", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
    
    st.divider()
    st.subheader("📁 MISSION ARCHIVE")
    
    # Download Log Button
    st.download_button(
        label="📥 DOWNLOAD LOGS (.TXT)",
        data=st.session_state['terminal_logs'],
        file_name=f"mission_log_{datetime.now().strftime('%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    if st.button("👁️ VIEW RAW DATA", use_container_width=True):
        st.info("Raw Log Preview Below Main Feed")
        st.code(st.session_state['terminal_logs'], language="text")

    if st.button("🗑️ PURGE FEED", use_container_width=True):
        st.session_state['terminal_logs'] = "FEED WIPED. READY FOR ENGAGEMENT..."
        st.rerun()

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
