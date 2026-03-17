import streamlit as st
import subprocess
import os
import requests
import zipfile
import io
import stat

# --- 1. CONFIG ---
# Moving to a deeper subfolder to avoid root /tmp permission locks
BIN_PATH = "/tmp/smallville_bin"
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if st.button("PRIME ELITE TOOLS", use_container_width=True):
        with st.spinner("🔓 Breaking Permission Locks..."):
            # Create directory with full permissions
            if not os.path.exists(BIN_PATH):
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
                        # Extracting one by one to handle permission errors per file
                        for member in z.namelist():
                            z.extract(member, BIN_PATH)
                            # Manually set executable permission for the binary
                            target_path = os.path.join(BIN_PATH, member)
                            os.chmod(target_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                        st.write(f"✅ {name} Armed")
                    else:
                        st.error(f"❌ {name} Download Failed")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            st.success("Armory Primed!")
            st.rerun()

    st.divider()
    p1 = st.toggle("P1: CEREBRO", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 4. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME")
    ru = st.text_input("🔗 ROOT DOMAIN")
    
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if tn and ru:
            st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            term_display = st.empty()
            
            env = os.environ.copy()
            # Pass the NEW BIN_PATH to the Bash script
            env.update({
                "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
                "RUN_P1": "1" if p1 else "0",
                "RUN_P4": "1" if p4 else "0"
            })
            
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
