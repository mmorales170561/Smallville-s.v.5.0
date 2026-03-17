import streamlit as st
import subprocess
import os
import requests
import zipfile
import io

# --- 1. CONFIG ---
BIN_PATH = "/tmp/bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

if 'terminal_logs' not in st.session_state: 
    st.session_state['terminal_logs'] = "READY FOR MISSION..."

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY CHECK ---
def check_ready():
    if not os.path.exists(BIN_PATH): return False
    tools = ["subfinder", "httpx", "nuclei"]
    return all(os.path.isfile(os.path.join(BIN_PATH, t)) for t in tools)

ready = check_ready()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # THE DOWNLOADER BLOCK
    if st.button("PRIME ELITE TOOLS", use_container_width=True):
        with st.spinner("📥 Bypassing Firewall..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            tools = {
                "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
                "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
                "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip"
            }
            for name, url in tools.items():
                r = requests.get(url)
                if r.status_code == 200:
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    z.extractall(BIN_PATH)
                    st.write(f"✅ {name} extracted.")
                else:
                    st.error(f"❌ {name} failed: {r.status_code}")
            
            subprocess.run(f"chmod +x {BIN_PATH}/*", shell=True)
            st.success("Armory Ready!")
            st.rerun()

    st.divider()
    p1 = st.toggle("P1: CEREBRO", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME")
    ru = st.text_input("🔗 ROOT DOMAIN")
    
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if not check_ready():
            st.error("ARMORY EMPTY. PRIME FIRST.")
        elif tn and ru:
            st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            term_display = st.empty()
            
            env = os.environ.copy()
            env.update({"RUN_P1": "1" if p1 else "0", "RUN_P4": "1" if p4 else "0"})
            
            proc = subprocess.Popen(["bash", SCRIPT, "strike", ru, tn], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                    text=True, env=env)
            
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None: break
                if line:
                    st.session_state['terminal_logs'] += line
                    term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
            st.success("Mission Complete.")

with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
