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
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 450px; overflow-y: auto; font-size: 13px;
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; transition: 0.3s; }
    .online { background-color: rgba(0, 255, 65, 0.2); border: 2px solid #00ff41; color: #00ff41; box-shadow: 0 0 15px #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. PERMISSIVE TOOL CHECK ---
# We count any files in the bin; if > 3, we consider the system "Primed"
tool_count = 0
if os.path.exists(BIN_PATH):
    tool_count = len([f for f in os.listdir(BIN_PATH) if os.path.isfile(os.path.join(BIN_PATH, f))])

ready = tool_count >= 4  # If 4 or more files exist, we are good to go.

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if ready:
        st.markdown(f'''<div class="status-panel online">
            <h3 style="margin:0;">SYSTEMS ONLINE</h3>
            <small><b>{tool_count} CORE TOOLS LOADED</b></small><br>
            <small>Last Prime: {st.session_state["last_prime"]}</small>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="status-panel offline">
            <h3 style="margin:0;">SYSTEMS OFFLINE</h3>
            <code>{tool_count}/4 TOOLS DETECTED</code>
        </div>''', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Priming Armory..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            res = subprocess.run(["bash", "powers.sh", "prime"], capture_output=True, text=True)
            if res.returncode == 0:
                st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
                st.rerun()
            else:
                st.error(f"Prime Error: {res.stderr}")

    st.divider()
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
        in_scope = st.text_area("✓ IN-SCOPE ASSETS", key="is", height=80)
        out_scope = st.text_area("✗ OUT-OF-SCOPE", key="os", height=80)
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("ARMORY OFFLINE")
            elif target_name and root_url:
                term_container = st.empty()
                env = os.environ.copy()
                env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope),
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0"
                })
                
                cmd = ["bash", "powers.sh", "strike", str(root_url), str(target_name)]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
                
                full_output = ""
                for line in iter(proc.stdout.readline, ''):
                    full_output += line
                    term_container.markdown(f'<div class="terminal-box">{full_output}</div>', unsafe_allow_html=True)
                proc.wait()

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    # DB logic...
