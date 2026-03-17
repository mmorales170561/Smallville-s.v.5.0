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

# --- 4. SIDEBAR ARMORY & STATUS ---
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

    if st.button("PRIME ELITE TOOLS", use_container_width=True):
        with st.spinner("📦 Fetching Tech..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
            st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
            st.rerun()

    st.divider()
    debug_mode = st.toggle("DEBUG MODE", value=False)
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: HOOK", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
    port_profile = st.selectbox("PORT PROFILE", ["Top 20 (Ghost)", "Top 100", "Top 1000"])

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯
