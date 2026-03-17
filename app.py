import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. CLOUD ENVIRONMENT SETUP ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"
if 'prime_logs' not in st.session_state: st.session_state['prime_logs'] = ""

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 400px; overflow-y: auto; font-size: 12px;
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .status-online { background-color: rgba(0,255,65,0.15); border: 2px solid #00ff41; color: #00ff41; }
    .status-offline { background-color: rgba(255,234,0,0.05); border: 1px solid #ffea00; color: #ffea00; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    tools = ["nuclei", "naabu", "subfinder", "httpx"]
    ready = all([os.path.exists(f"/tmp/bin/{t}") for t in tools])
    
    if ready:
        st.markdown(f'<div class="status-panel status-online"><b>SYSTEMS ONLINE</b><br><small>{st.session_state["last_prime"]}</small></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-panel status-offline"><b>SYSTEMS OFFLINE</b><br><code>RE-PRIME REQUIRED</code></div>', unsafe_allow_html=True)

    # --- UPDATED PRIME LOGIC ---
    if st.button("PRIME ELITE TOOLS", width="stretch"):
        log_placeholder = st.empty()
        st.session_state['prime_logs'] = "Initializing Prime Sequence...\n"
        
        # We run this as a stream so we can see the 'curls' and 'unpacks' happening
        script_path = os.path.join(os.getcwd(), "powers.sh")
        p = subprocess.Popen(["bash", script_path, "prime"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        for line in iter(p.stdout.readline, ''):
            st.session_state['prime_logs'] += line
            log_placeholder.markdown(f'<div class="terminal-box">{st.session_state["prime_logs"]}</div>', unsafe_allow_html=True)
        
        p.wait()
        if p.returncode == 0:
            st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
            st.success("Armory Primed Successfully.")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Prime sequence failed. Check logs above.")

    st.divider()
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: HOOK", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 4. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_in, col_term = st.columns([1, 2.2])
    with col_in:
        st.subheader("Mission Brief")
        tn = st.text_input("🎯 TARGET NAME", key="tn")
        ru = st.text_input("🔗 ROOT DOMAIN", key="ru")
        is_scope = st.text_area("✓ IN-SCOPE", key="is")
        os_scope = st.text_area("✗ OUT-OF-SCOPE", key="os")
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.warning("Prime tools first.")
            elif tn and ru:
                term = st.empty()
                script_path = os.path.join(os.getcwd(), "powers.sh")
                env = os.environ.copy()
                env.update({"IN_SCOPE": str(is_scope), "OUT_SCOPE": str(os_scope)})
                
                proc = subprocess.Popen(["bash", script_path, "strike", str(ru), str(tn)], 
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                
                output = ""
                for line in iter(proc.stdout.readline, ''):
                    output += line
                    term.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                proc.wait()

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    # Table logic here...
