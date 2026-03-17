import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# --- 1. CLOUD ENVIRONMENT ---
BIN_PATH = "/tmp/bin"
CWD = os.getcwd()
if BIN_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = BIN_PATH + os.pathsep + os.environ["PATH"]

# Persistent logs so they don't vanish on rerun
if 'terminal_logs' not in st.session_state: 
    st.session_state['terminal_logs'] = "READY FOR ENGAGEMENT..."
if 'last_prime' not in st.session_state: 
    st.session_state['last_prime'] = "NEVER"

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 15px rgba(255,0,0,0.5);
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 2px solid #333; }
    .online { background-color: rgba(0, 255, 65, 0.1); border-color: #00ff41 !important; color: #00ff41; box-shadow: 0 0 10px #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border-color: #ff0000 !important; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. STATUS CHECK ---
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
            subprocess.run(["/bin/bash", os.path.join(CWD, "powers.sh"), "prime"], capture_output=True)
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
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_in, col_term = st.columns([1, 2.2])
    with col_in:
        st.subheader("Mission Brief")
        target_name = st.text_input("🎯 TARGET NAME", key="tn")
        root_url = st.text_input("🔗 ROOT DOMAIN", key="ru")
        in_scope = st.text_area("✓ IN-SCOPE ASSETS", key="is", height=100)
        out_scope = st.text_area("✗ OUT-OF-SCOPE", key="os", height=100)
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("ARMORY OFFLINE")
            elif target_name and root_url:
                # 1. Reset Session Logs
                st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {target_name} ---\n"
                
                # 2. Setup Environment
                env = os.environ.copy()
                env["PATH"] = f"{BIN_PATH}:{env.get('PATH', '')}"
                env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope),
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0"
                })

                # 3. Create the Terminal Placeholder
                # We update the col_term column specifically
                with col_term:
                    term_display = st.empty()
                
                # 4. Start Process
                script_path = os.path.join(CWD, "powers.sh")
                proc = subprocess.Popen(
                    ["/bin/bash", script_path, "strike", str(root_url), str(target_name)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env,
                    cwd=CWD,
                    bufsize=1
                )

                # 5. The Active Stream Loop
                while True:
                    line = proc.stdout.readline()
                    if not line and proc.poll() is not None:
                        break
                    if line:
                        st.session_state['terminal_logs'] += line
                        # This 'term_display' is what makes it scroll step-by-step
                        term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
                
                proc.wait()
                st.success(f"Mission {target_name} Complete.")

    with col_term:
        st.subheader("Live Tactical Feed")
        # Shows the persistent logs when not actively scanning
        st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)

# --- 6. ARCHIVE & LEDGER ---
with t2:
    st.subheader("🗄️ MISSION LEDGER")
    # SQL Table Logic...
