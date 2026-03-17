import streamlit as st
import subprocess
import os
import requests
import zipfile
import io
import stat
from datetime import datetime

# --- 1. CONFIG & STABLE PATHS ---
BIN_PATH = "/tmp/smallville_bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

# Ensure session state exists before rendering UI
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
    .online { background-color: rgba(0, 255, 65, 0.1); border-color: #00ff41 !important; color: #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border-color: #ff0000 !important; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY STATUS CHECK (Safe Mode) ---
def get_armory_status():
    try:
        if not os.path.exists(BIN_PATH): return False
        tools = ["subfinder", "httpx", "nuclei"]
        return all(os.path.isfile(os.path.join(BIN_PATH, t)) for t in tools)
    except:
        return False

is_ready = get_armory_status()

# --- 4. SIDEBAR (LOGS & CONTROLS) ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if is_ready:
        st.markdown('<div class="status-panel online"><b>SYSTEMS ONLINE</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-panel offline"><b>SYSTEMS OFFLINE</b></div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", use_container_width=True):
        with st.spinner("🔓 Unlocking Armory..."):
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
    st.download_button(
        label="📥 DOWNLOAD LOGS",
        data=st.session_state['terminal_logs'],
        file_name=f"log_{datetime.now().strftime('%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    if st.button("🗑️ PURGE FEED", use_container_width=True):
        st.session_state['terminal_logs'] = "READY..."
        st.rerun()

# --- 5. MAIN HUD (MISSION BRIEF & FEED) ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    # Using specific keys to prevent state loss
    tn = st.text_input("🎯 TARGET NAME", key="target_name_input")
    ru = st.text_input("🔗 ROOT DOMAIN", key="root_domain_input")
    is_scope = st.text_area("✓ IN-SCOPE", height=80, key="in_scope_input")
    
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if not is_ready:
            st.error("ARMORY OFFLINE. CLICK PRIME.")
        elif tn and ru:
            st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            term_display = st.empty()
            
            # Safe Environment Copy
            env = os.environ.copy()
            current_path = env.get('PATH', '')
            env["PATH"] = f"{BIN_PATH}:{current_path}"
            env.update({
                "RUN_P1": "1" if p1 else "0",
                "RUN_P2": "1" if p2 else "0",
                "RUN_P3": "1" if p3 else "0",
                "RUN_P4": "1" if p4 else "0"
            })
            
            # Check if powers.sh exists before firing
            if os.path.exists(SCRIPT):
                subprocess.run(["chmod", "+x", SCRIPT])
                proc = subprocess.Popen(["bash", SCRIPT, "strike", ru, tn], 
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                        text=True, env=env)
                
                while True:
                    line = proc.stdout.readline()
                    if not line and proc.poll() is not None: break
                    if line:
                        st.session_state['terminal_logs'] += line
                        term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
                st.success("Target Engaged.")
            else:
                st.error("powers.sh missing from source.")

with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
