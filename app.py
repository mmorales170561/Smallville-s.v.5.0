import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. CLOUD ENVIRONMENT SETUP ---
BIN_PATH = "/tmp/bin"
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
        white-space: pre-wrap; height: 450px; overflow-y: auto; font-size: 13px;
    }
    /* THE STATUS PANEL COLORS */
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; transition: 0.3s; }
    .online { background-color: rgba(0, 255, 65, 0.2); border: 2px solid #00ff41; color: #00ff41; box-shadow: 0 0 10px #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. TOOL CHECK LOGIC ---
essential_tools = ["nuclei", "naabu", "subfinder", "httpx"]
# Check if the folder exists and contains the files
ready = False
if os.path.exists(BIN_PATH):
    found_tools = os.listdir(BIN_PATH)
    ready = all(t in found_tools for t in essential_tools)

# --- 4. SIDEBAR ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # DYNAMIC STATUS PANEL
    if ready:
        st.markdown(f'''<div class="status-panel online">
            <h3 style="margin:0;">SYSTEMS ONLINE</h3>
            <small>Krypton Tech Active</small><br>
            <small>Last Prime: {st.session_state["last_prime"]}</small>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="status-panel offline">
            <h3 style="margin:0;">SYSTEMS OFFLINE</h3>
            <code>{len(os.listdir(BIN_PATH)) if os.path.exists(BIN_PATH) else 0}/4 TOOLS LOADED</code>
        </div>''', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Downloading binaries to /tmp/bin..."):
            script_path = os.path.join(os.getcwd(), "powers.sh")
            # Force creating the directory before running
            os.makedirs(BIN_PATH, exist_ok=True)
            
            # Run the prime script
            res = subprocess.run(["bash", script_path, "prime"], capture_output=True, text=True)
            
            if res.returncode == 0:
                st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
                st.toast("Armory Primed!", icon="🛡️")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Prime Failed")
                st.code(res.stderr)

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
        # RESTORED INPUTS
        target_name = st.text_input("🎯 TARGET NAME", key="tn", placeholder="Project Smallville")
        root_url = st.text_input("🔗 ROOT DOMAIN", key="ru", placeholder="example.com")
        
        # IN-SCOPE / OUT-OF-SCOPE
        in_scope = st.text_area("✓ IN-SCOPE ASSETS", key="is", help="One per line", height=100)
        out_scope = st.text_area("✗ OUT-OF-SCOPE", key="os", help="Exclusions", height=100)
        
        st.divider()
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("ARMORY OFFLINE: Please run Prime Elite Tools.")
            elif not target_name or not root_url:
                st.warning("Target Name and Root Domain are required.")
            else:
                term_container = st.empty()
                script_path = os.path.join(os.getcwd(), "powers.sh")
                
                # Setup Environment
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope),
                    "OUT_SCOPE": str(out_scope),
                    "RUN_P1": "1" if p1 else "0",
                    "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0",
                    "RUN_P4": "1" if p4 else "0"
                })
                
                cmd = ["bash", script_path, "strike", str(root_url), str(target_name)]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_output = ""
                for line in iter(proc.stdout.readline, ''):
                    full_output += line
                    term_container.markdown(f'<div class="terminal-box">{full_output}</div>', unsafe_allow_html=True)
                
                proc.wait()
                st.success("STRIKE COMPLETE")

# --- 6. MISSION LEDGER ---
with t2:
    st.subheader("🗄️ INTELLIGENCE LEDGER")
    if os.path.exists('red_kryptonite_ledger.db'):
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT id, timestamp, target, crit_count, high_count FROM ledger ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, width="stretch", hide_index=True)
    else:
        st.info("No mission data found. Fire the Red Kryptonite Gun to begin.")
