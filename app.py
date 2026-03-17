import streamlit as st
import subprocess
import os
import time
from datetime import datetime

# --- 1. ENVIRONMENT & PATHS ---
BIN_PATH = "/tmp/bin"
CWD = os.getcwd()
if BIN_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = BIN_PATH + os.pathsep + os.environ["PATH"]

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
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.4);
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 2px solid #333; }
    .online { background-color: rgba(0, 255, 65, 0.1); border-color: #00ff41 !important; color: #00ff41; box-shadow: 0 0 10px #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border-color: #ff0000 !important; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. STATUS ---
tool_count = 0
if os.path.exists(BIN_PATH):
    tool_count = len([f for f in os.listdir(BIN_PATH) if os.path.isfile(os.path.join(BIN_PATH, f))])
ready = tool_count >= 4

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if ready:
        st.markdown(f'<div class="status-panel online"><b>SYSTEMS ONLINE</b><br>{tool_count} TOOLS LOADED</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-panel offline"><b>SYSTEMS OFFLINE</b><br>{tool_count}/4 LOADED</div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Priming..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            subprocess.run(["bash", os.path.join(CWD, "powers.sh"), "prime"], capture_output=True)
            st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()

    st.divider()
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: HOOK", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", key="tn")
    ru = st.text_input("🔗 ROOT DOMAIN", key="ru")
    is_scope = st.text_area("✓ IN-SCOPE", key="is", height=80)
    os_scope = st.text_area("✗ OUT-OF-SCOPE", key="os", height=80)
    
    if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
        script_path = os.path.join(CWD, "powers.sh")
        
        if not os.path.exists(script_path):
            st.error("FATAL: powers.sh not found.")
        elif not tn or not ru:
            st.warning("Target details required.")
        else:
            # Clear logs and prepare display
            st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            st.session_state['terminal_logs'] += f"Executing: bash {script_path} strike {ru} {tn}\n"
            
            with col_term:
                term_display = st.empty()
                term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
            
            # Setup Environment
            env = os.environ.copy()
            env["PATH"] = f"{BIN_PATH}:{env.get('PATH', '')}"
            env.update({
                "IN_SCOPE": str(is_scope), "OUT_SCOPE": str(os_scope),
                "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0"
            })

            # Start the Strike with 'unbuffered' output
            proc = subprocess.Popen(
                ["bash", script_path, "strike", str(ru), str(tn)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                cwd=CWD,
                bufsize=1 # Line-buffered
            )

            # --- THE HEART OF THE STREAM ---
            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None:
                    break
                if line:
                    st.session_state['terminal_logs'] += line
                    # Real-time UI update
                    term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
            
            proc.wait()
            st.success(f"Mission {tn} Complete.")

with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
