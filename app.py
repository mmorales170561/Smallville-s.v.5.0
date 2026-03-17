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
        white-space: pre-wrap; height: 580px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5); border-radius: 5px;
    }
    .status-panel { padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #333; margin-bottom: 10px; }
    .online { color: #00ff41; border-color: #00ff41; background: rgba(0,255,65,0.1); }
    .offline { color: #ff0000; border-color: #ff0000; background: rgba(255,0,0,0.1); }
    .tool-tag { font-size: 10px; padding: 2px 5px; border-radius: 3px; margin-right: 5px; border: 1px solid #444; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY STATUS CHECK ---
def get_tools():
    found = []
    for t in ["subfinder", "httpx", "nuclei"]:
        if os.path.exists(os.path.join(BIN_PATH, t)):
            found.append(t)
    return found

installed_tools = get_tools()
is_ready = len(installed_tools) >= 3

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if is_ready:
        st.markdown('<div class="status-panel online"><b>SYSTEMS ONLINE</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-panel offline"><b>SYSTEMS OFFLINE</b></div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", use_container_width=True):
        with st.spinner("🔓 Unlocking Armory..."):
            os.makedirs(BIN_PATH, mode=0o777, exist_ok=True)
            urls = {
                "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
                "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
                "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip"
            }
            for name, url in urls.items():
                try:
                    r = requests.get(url, timeout=30)
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    for m in z.namelist():
                        z.extract(m, BIN_PATH)
                        os.chmod(os.path.join(BIN_PATH, m), 0o777)
                except: pass
            st.rerun()

    st.divider()
    st.subheader("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: HOOK", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
    p5 = st.toggle("P5: ARCHITECT (Repo Scan)", value=False)
    
    st.divider()
    st.subheader("📁 MISSION ARCHIVE")
    st.download_button("📥 DOWNLOAD LOGS", data=st.session_state['terminal_logs'], 
                       file_name=f"log_{datetime.now().strftime('%H%M%S')}.txt", use_container_width=True)
    if st.button("🗑️ PURGE FEED", use_container_width=True):
        st.session_state['terminal_logs'] = "READY..."
        st.rerun()

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", placeholder="LexCorp", key="tn_val")
    ru = st.text_input("🔗 ROOT URL", placeholder="lexcorp.com", key="ru_val")
    gh_repo = st.text_input("🐙 GITHUB REPO URL", placeholder="https://github.com/user/ai-agent", key="gh_val")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        is_scope = st.text_area("✓ IN-SCOPE", height=80, placeholder="*.target.com", key="is_val")
    with col_s2:
        os_scope = st.text_area("✗ OUT-SCOPE", height=80, placeholder="dev.target.com", key="os_val")
    
    # Weapon Status HUD
    st.markdown("---")
    st.write("**Weapon Status:**")
    status_html = ""
    for tool in ["subfinder", "httpx", "nuclei"]:
        color = "#00ff41" if tool in installed_tools else "#ff0000"
        status_html += f'<span class="tool-tag" style="color:{color}; border-color:{color};">{tool.upper()}</span>'
    st.markdown(status_html, unsafe_allow_html=True)

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if not is_ready:
            st.error("SYSTEMS OFFLINE. PRIME ARMORY.")
        elif tn and (ru or gh_repo):
            st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            term_display = st.empty()
            
            env = os.environ.copy()
            env.update({
                "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
                "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                "RUN_P5": "1" if p5 else "0", "GH_REPO": str(gh_repo)
            })
            
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
            st.success("Strike Complete.")
        else:
            st.warning("Enter Target and either a URL or GitHub Repo.")

with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
