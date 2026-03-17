import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time

# --- 1. ENVIRONMENT ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'last_duration' not in st.session_state: st.session_state['last_duration'] = "0s"

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto;
    }
    .status-light { padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    tools_ready = os.path.exists("/tmp/bin/nuclei")
    st.markdown(f'<div class="status-light" style="background-color: {"#00ff41" if tools_ready else "#ffea00"}; color: black;">SYSTEMS {"ONLINE" if tools_ready else "OFFLINE"}</div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS"):
        subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.rerun()
    
    st.divider()
    st.header("⚙️ DEBUG & TUNING")
    # NEW: Debug Mode Toggle
    debug_mode = st.toggle("DEBUG MODE", value=False, help="Show raw tool errors in terminal")
    
    st.divider()
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("PHASE 1: CEREBRO", value=True)
    p2 = st.toggle("PHASE 2: SHADOW", value=True)
    p3 = st.toggle("PHASE 3: HOOK", value=True)
    p4 = st.toggle("PHASE 4: STRIKE", value=True)
    
    port_profile = st.selectbox("PORT PROFILE", ["Top 20 (Ghost)", "Top 100", "Top 1000"])

# --- 4. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        target_name = st.text_input("🎯 TARGET NAME")
        root_url = st.text_input("🔗 ROOT DOMAIN")
        in_scope = st.text_area("✓ IN-SCOPE")
        out_scope = st.text_area("✗ OUT-OF-SCOPE")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if root_url and target_name:
                start_time = time.time()
                terminal = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope),
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                    "DEBUG": "1" if debug_mode else "0",
                    "PORT_PROFILE": port_profile
                })
                
                # Executing with unbuffered output for real-time "Bit by Bit" viewing
                p = subprocess.Popen(["bash", "powers.sh", "strike", root_url, target_name], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()
                
                st.session_state['last_duration'] = f"{round(time.time() - start_time, 2)}s"
                st.rerun()
