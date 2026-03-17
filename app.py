import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# --- 1. CLOUD PATH SETUP ---
# We define the current working directory explicitly
CWD = os.getcwd()
BIN_PATH = "/tmp/bin"

if 'terminal_output' not in st.session_state: 
    st.session_state['terminal_output'] = "READY FOR MISSION..."

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 14px;
        border-radius: 5px; box-shadow: 0 0 15px rgba(255,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    # Quick tool check
    ready = os.path.exists(BIN_PATH) and len(os.listdir(BIN_PATH)) >= 4
    
    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Priming..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            # Use absolute path for the script
            script = os.path.join(CWD, "powers.sh")
            subprocess.run(["/bin/bash", script, "prime"], capture_output=True)
            st.rerun()

    st.divider()
    p1, p4 = st.toggle("P1: CEREBRO", True), st.toggle("P4: STRIKE", True)

# --- 4. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", key="tn")
    ru = st.text_input("🔗 ROOT DOMAIN", key="ru")
    is_scope = st.text_area("✓ IN-SCOPE", key="is")
    
    if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
        if tn and ru:
            # RESET TERMINAL FOR NEW MISSION
            st.session_state['terminal_output'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            term_placeholder = st.empty()
            
            # 1. SETUP CLOUD ENVIRONMENT
            env = os.environ.copy()
            env["PATH"] = f"{BIN_PATH}:{env.get('PATH', '')}"
            env["IN_SCOPE"] = str(is_scope)
            
            # 2. DEFINE ABSOLUTE COMMAND
            script_path = os.path.join(CWD, "powers.sh")
            cmd = ["/bin/bash", script_path, "strike", str(ru), str(tn)]
            
            # 3. EXECUTE WITH ACTIVE POLLING
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                env=env,
                cwd=CWD,      # Force execution in the app root
                bufsize=1     # Line buffered for real-time scrolling
            )
            
            # 4. MONITOR STREAM
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    st.session_state['terminal_output'] += line
                    # Update the UI every time a line comes in
                    term_placeholder.markdown(f'<div class="terminal-box">{st.session_state["terminal_output"]}</div>', unsafe_allow_html=True)
            
            process.wait()
            st.success(f"Mission {tn} Complete.")
        else:
            st.warning("Target details required.")

with col_term:
    st.subheader("Live Tactical Feed")
    # This keeps the terminal visible even after the process finishes
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_output"]}</div>', unsafe_allow_html=True)
