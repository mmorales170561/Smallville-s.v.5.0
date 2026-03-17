import streamlit as st
import subprocess
import os
import time
from datetime import datetime

# --- 1. CLOUD ENVIRONMENT ---
BIN_PATH = "/tmp/bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

# Ensure PATH includes our tool directory
if BIN_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = BIN_PATH + os.pathsep + os.environ["PATH"]

# Persistent Session State
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

# --- 3. ARMORY CHECK ---
def get_tool_count():
    if os.path.exists(BIN_PATH):
        return len([f for f in os.listdir(BIN_PATH) if os.path.isfile(os.path.join(BIN_PATH, f))])
    return 0

tool_count = get_tool_count()
ready = tool_count >= 3 # subfinder, nuclei, httpx

# --- 4. SIDEBAR (RESTORED) ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if ready:
        st.markdown(f'<div class="status-panel online"><b>SYSTEMS ONLINE</b><br>{tool_count} TOOLS LOADED</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-panel offline"><b>SYSTEMS OFFLINE</b><br>{tool_count}/3 LOADED</div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Downloading Armory..."):
            subprocess.run(["chmod", "+x", SCRIPT])
            subprocess.run(["sed", "-i", "s/\\r$//", SCRIPT])
            subprocess.run(["bash", SCRIPT, "prime"])
            st.rerun()

    st.divider()
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: HOOK", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD (RESTORED) ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER"])

with t1:
    col_in, col_term = st.columns([1, 2.2])
    
    with col_in:
        st.subheader("Mission Brief")
        tn = st.text_input("🎯 TARGET NAME", placeholder="e.g. LexCorp")
        ru = st.text_input("🔗 ROOT DOMAIN", placeholder="example.com")
        is_scope = st.text_area("✓ IN-SCOPE", height=100)
        os_scope = st.text_area("✗ OUT-OF-SCOPE", height=100)
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("ARMORY EMPTY. RUN PRIME FIRST.")
            elif tn and ru:
                st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
                term_display = st.empty()
                
                # Setup Environment Variables for Bash
                env = os.environ.copy()
                env.update({
                    "RUN_P1": "1" if p1 else "0",
                    "RUN_P4": "1" if p4 else "0",
                    "IN_SCOPE": str(is_scope)
                })

                # Execute and Stream
                proc = subprocess.Popen(
                    ["bash", SCRIPT, "strike", str(ru), str(tn)],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, env=env, bufsize=1
                )

                while True:
                    line = proc.stdout.readline()
                    if not line and proc.poll() is not None: break
                    if line:
                        st.session_state['terminal_logs'] += line
                        term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
                
                proc.wait()
                st.success(f"Mission {tn} Complete.")
            else:
                st.warning("Target details required.")

    with col_term:
        st.subheader("Live Tactical Feed")
        st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    st.info("Results are stored in the mission database.")
