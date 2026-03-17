import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. ENVIRONMENT ---
BIN_PATH = "/tmp/bin"
if BIN_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = BIN_PATH + os.pathsep + os.environ["PATH"]

if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"
if 'terminal_output' not in st.session_state: st.session_state['terminal_output'] = "Awaiting Command..."

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 550px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 10px #ff0000;
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 2px solid #333; }
    .online { background-color: rgba(0, 255, 65, 0.1); border-color: #00ff41 !important; color: #00ff41; }
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
        st.markdown(f'<div class="status-panel online"><b>SYSTEMS ONLINE</b><br>{tool_count} TOOLS</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-panel" style="color:#ffea00; border-color:#ffea00;"><b>OFFLINE</b><br>{tool_count}/4 LOADED</div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📦 Downloading..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
            st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()

    st.divider()
    p1, p2 = st.toggle("P1: CEREBRO", True), st.toggle("P2: SHADOW", True)
    p3, p4 = st.toggle("P3: HOOK", True), st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    c1, c2 = st.columns([1, 2.2])
    with c1:
        st.subheader("Mission Brief")
        tn = st.text_input("🎯 TARGET NAME", key="tn")
        ru = st.text_input("🔗 ROOT DOMAIN", key="ru")
        is_scope = st.text_area("✓ IN-SCOPE", key="is", height=100)
        os_scope = st.text_area("✗ OUT-OF-SCOPE", key="os", height=100)
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("SYSTEMS OFFLINE")
            elif tn and ru:
                st.session_state['terminal_output'] = "--- INITIALIZING STRIKE SEQUENCE ---\n"
                prog = st.progress(0)
                term_placeholder = st.empty()
                
                # Injecting Path for Cloud binaries
                env = os.environ.copy()
                env["PATH"] = f"{BIN_PATH}:{env.get('PATH', '')}"
                env.update({"IN_SCOPE": str(is_scope), "OUT_SCOPE": str(os_scope)})
                
                # Use Popen with stderr redirection to catch EVERY error
                proc = subprocess.Popen(["bash", "powers.sh", "strike", str(ru), str(tn)], 
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
                
                # Capture the stream
                while True:
                    line = proc.stdout.readline()
                    if not line and proc.poll() is not None:
                        break
                    if line:
                        st.session_state['terminal_output'] += line
                        # Update terminal in real-time
                        term_placeholder.markdown(f'<div class="terminal-box">{st.session_state["terminal_output"]}</div>', unsafe_allow_html=True)
                
                proc.wait()
                prog.progress(100)
                st.success(f"Mission {tn} Complete.")

    with c2:
        st.subheader("Live Tactical Feed")
        # Ensure the terminal stays visible even after the script finishes
        st.markdown(f'<div class="terminal-box">{st.session_state["terminal_output"]}</div>', unsafe_allow_html=True)

# --- 6. LEDGER ---
with t2:
    st.subheader("🗄️ MISSION LEDGER")
    st.info("Results are stored in red_kryptonite_ledger.db")
