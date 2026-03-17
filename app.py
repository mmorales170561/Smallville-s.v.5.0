import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# --- 1. ENVIRONMENT & PERSISTENCE ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'last_duration' not in st.session_state: st.session_state['last_duration'] = "0s"

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto;
    }
    .status-light { padding: 5px; border-radius: 5px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .timer-card { background-color: #111; border: 1px solid #ff0000; padding: 10px; color: #ff0000; text-align: center; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# --- 3. AUTH GATE ---
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("KRYPTONIAN ACCESS")
        u = st.text_input("ID")
        p = st.text_input("CRYPT", type="password")
        if st.button("AUTHORIZE"):
            if u == "clark_kent" and p == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- 4. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    tools_ready = os.path.exists("/tmp/bin/naabu")
    st.markdown(f'<div class="status-light" style="background-color: {"#00ff41" if tools_ready else "#ffea00"}; color: black;">SYSTEMS {"ONLINE" if tools_ready else "OFFLINE"}</div>', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS"):
        with st.spinner("FETCHING..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.rerun()
    
    st.divider()
    st.header("⏱️ MISSION LOG")
    st.markdown(f'<div class="timer-card">LAST STRIKE: {st.session_state["last_duration"]}</div>', unsafe_allow_html=True)

    st.divider()
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("PHASE 1: CEREBRO", value=True)
    p2 = st.toggle("PHASE 2: SHADOW", value=False)
    p3 = st.toggle("PHASE 3: HOOK", value=True)
    
    # NEW: Port Profile Selection
    port_profile = st.selectbox("PORT PROFILE", ["Top 20 (Ghost)", "Top 100 (Standard)", "Top 1000 (Full)"])
    
    p4 = st.toggle("PHASE 4: STRIKE", value=True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "🖼️ GALLERY"])

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
                    "PORT_PROFILE": port_profile
                })
                
                p = subprocess.Popen(["bash", "powers.sh", "strike", root_url, target_name], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env)
                
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()
                
                duration = round(time.time() - start_time, 2)
                st.session_state['last_duration'] = f"{duration}s"
                st.rerun()
            else:
                st.error("NAME AND DOMAIN REQUIRED.")

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    # (Database display logic remains the same)
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("Awaiting Recon Data...")
