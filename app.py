import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime

# --- 1. PATH & STATE SETUP ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'target' not in st.session_state: st.session_state['target'] = ""
if 'auth' not in st.session_state: st.session_state['auth'] = False

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 400px; overflow-y: auto;
    }
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

# --- 4. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "🖼️ GALLERY"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        # Store input directly into session state to avoid NameErrors
        st.session_state['target'] = st.text_input("🎯 ROOT TARGET", value=st.session_state['target'])
        in_scope = st.text_area("✓ IN-SCOPE")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if st.session_state['target']:
                terminal = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({"IN_SCOPE": str(in_scope)})
                
                # Using st.session_state['target'] here ensures it's never undefined
                p = subprocess.Popen(["bash", "powers.sh", "strike", st.session_state['target']], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env)
                
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()
                st.rerun()
            else:
                st.error("TARGET REQUIRED.")

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)
    except:
        st.info("Awaiting first mission logs...")

with t3:
    st.subheader("🖼️ RECON GALLERY")
    st.info("Gallery will populate from the database once a strike is logged.")
