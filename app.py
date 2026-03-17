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
# Ensure the OS knows about our tools
if BIN_PATH not in os.environ["PATH"]:
    os.environ["PATH"] = BIN_PATH + os.pathsep + os.environ["PATH"]

if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto; font-size: 13px;
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; transition: 0.3s; }
    .online { background-color: rgba(0, 255, 65, 0.2); border: 2px solid #00ff41; color: #00ff41; box-shadow: 0 0 15px #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; color: #ff0000; }
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
        st.markdown(f'<div class="status-panel online"><b>SYSTEMS ONLINE</b><br><small>{tool_count} TOOLS LOADED</small></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-panel offline"><b>SYSTEMS OFFLINE</b><br><code>{tool_count}/4 LOADED</code></div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Priming..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
            st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()

    st.divider()
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: HOOK", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    c1, c2 = st.columns([1, 2.2])
    with c1:
        st.subheader("Mission Brief")
        target_name = st.text_input("🎯 TARGET NAME", key="tn")
        root_url = st.text_input("🔗 ROOT DOMAIN", key="ru")
        in_scope = st.text_area("✓ IN-SCOPE", key="is", height=100)
        out_scope = st.text_area("✗ OUT-OF-SCOPE", key="os", height=100)
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("SYSTEMS OFFLINE - RUN PRIME FIRST")
            elif target_name and root_url:
                term = st.empty()
                prog = st.progress(0, text="Initializing...")
                
                # --- THE PATH FIX ---
                # We inject the /tmp/bin path into the command environment
                strike_env = os.environ.copy()
                strike_env["PATH"] = f"{BIN_PATH}:{strike_env.get('PATH', '')}"
                strike_env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope),
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0"
                })
                
                # Use absolute path to bash for stability
                cmd = ["/bin/bash", "powers.sh", "strike", str(root_url), str(target_name)]
                
                # Using Popen to stream live output
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_log = ""
                for line in iter(process.stdout.readline, ''):
                    full_log += line
                    # Progress Updates
                    if "PHASE 1" in line: prog.progress(25, text="Phase 1: Recon")
                    elif "PHASE 2" in line: prog.progress(50, text="Phase 2: Discovery")
                    elif "PHASE 3" in line: prog.progress(75, text="Phase 3: Fuzzing")
                    elif "PHASE 4" in line: prog.progress(90, text="Phase 4: Striking")
                    
                    # Live Terminal Update
                    term.markdown(f'<div class="terminal-box">{full_log}</div>', unsafe_allow_html=True)
                
                process.wait()
                prog.progress(100, text="Mission Complete.")
                st.success("Target Engaged.")
