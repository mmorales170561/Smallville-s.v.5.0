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

if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto;
    }
    .status-panel { padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #333; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR DEBUG & ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # Check if tools actually exist in /tmp/bin
    essential = ["nuclei", "naabu", "subfinder"]
    ready = all([os.path.exists(f"/tmp/bin/{t}") for t in essential])
    
    if ready:
        st.success("SYSTEMS ONLINE")
    else:
        st.warning("SYSTEMS OFFLINE")

    # --- THE PRIME BUTTON ---
    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("Executing powers.sh..."):
            # We use shell=True here specifically for Chromebook Linux environments 
            # to ensure the bash profile is recognized.
            proc = subprocess.run("bash powers.sh prime", shell=True, capture_output=True, text=True)
            
            if proc.returncode == 0:
                st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
                st.success("Armory Primed!")
                st.rerun()
            else:
                # THIS IS THE DEBUG OUTPUT
                st.error("EXECUTION FAILED")
                st.code(f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")

    st.divider()
    
    # NEW: Manual Permission Fix
    if st.button("FIX PERMISSIONS", width="stretch"):
        subprocess.run("chmod +x powers.sh", shell=True)
        st.info("Ran chmod +x on powers.sh")

# --- 4. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_in, col_term = st.columns([1, 2.2])
    with col_in:
        st.subheader("Mission Brief")
        target = st.text_input("🎯 TARGET NAME", key="tn")
        url = st.text_input("🔗 ROOT DOMAIN", key="ru")
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.error("Tools not found. Click 'PRIME' first.")
            elif target and url:
                term = st.empty()
                cmd = f"bash powers.sh strike {url} {target}"
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    term.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()

# --- 5. LEDGER (Simplified for stability) ---
with t2:
    st.subheader("🗄️ MISSION LEDGER")
    if os.path.exists('red_kryptonite_ledger.db'):
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        st.dataframe(df, width="stretch")
        conn.close()
    else:
        st.info("No database found.")
