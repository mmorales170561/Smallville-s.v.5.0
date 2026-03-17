import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. ENVIRONMENT ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"

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
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS ledger 
                    (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT, 
                     report TEXT, crit_count INTEGER, high_count INTEGER)''')
    conn.commit()
    conn.close()

def parse_vulns(text):
    crit = len(re.findall(r"\[critical\]", text, re.IGNORECASE))
    high = len(re.findall(r"\[high\]", text, re.IGNORECASE))
    return crit, high

init_db()

# --- 4. SIDEBAR ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    tools = ["nuclei", "naabu", "subfinder", "httpx"]
    ready = all([os.path.exists(f"/tmp/bin/{t}") for t in tools])
    
    if ready:
        st.markdown(f'''<div class="status-panel" style="background-color: rgba(0,255,65,0.1); border-color: #00ff41;">
            <h3 style="color: #00ff41; margin:0;">SYSTEMS ONLINE</h3>
            <small style="color: #888;">Armory Primed: {st.session_state["last_prime"]}</small>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div class="status-panel" style="background-color: rgba(255,234,0,0.1); border-color: #ffea00;">
            <h3 style="color: #ffea00; margin:0;">SYSTEMS OFFLINE</h3>
            <code style="color: #ffea00;">RE-PRIME REQUIRED</code>
        </div>''', unsafe_allow_html=True)

    # UPDATED: width='stretch' replaces use_container_width=True
    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📦 Fetching Tech..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
            st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()

    st.divider()
    debug_mode = st.toggle("DEBUG MODE", value=False)
    st.header("⚡ PHASE TOGGLES")
    p1, p2 = st.toggle("P1: CEREBRO", True), st.toggle("P2: SHADOW", True)
    p3, p4 = st.toggle("P3: HOOK", True), st.toggle("P4: STRIKE", True)
    port_profile = st.selectbox("PORT PROFILE", ["Top 20 (Ghost)", "Top 100", "Top 1000"])

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_input, col_term = st.columns([1, 2.2])
    with col_input:
        st.subheader("Mission Brief")
        target_name = st.text_input("🎯 TARGET NAME", key="tname")
        root_url = st.text_input("🔗 ROOT DOMAIN", key="rurl")
        in_scope = st.text_area("✓ IN-SCOPE ASSETS", key="iscope")
        out_scope = st.text_area("✗ OUT-OF-SCOPE", key="oscope")
        
        # UPDATED: width='stretch'
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.warning("Armory is empty. Prime tools in sidebar first.")
            elif root_url and target_name:
                prog = st.progress(0, text="Sequence Initialized...")
                term_display = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope), 
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                    "DEBUG": "1" if debug_mode else "0", "PORT_PROFILE": port_profile
                })
                
                cmd = ["bash", "powers.sh", "strike", str(root_url), str(target_name)]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_rep = ""
                for line in iter(p.stdout.readline, ''):
                    full_rep += line
                    if "PHASE 1" in line: prog.progress(25, text="Phase 1: Cerebro...")
                    elif "PHASE 2" in line: prog.progress(50, text="Phase 2: Shadow...")
                    elif "PHASE 3" in line: prog.progress(75, text="Phase 3: Hooking...")
                    elif "PHASE 4" in line: prog.progress(90,
