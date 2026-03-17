import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# --- 2026 PATH & ENVIRONMENT ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

# --- THEME: KRYPTONIAN TERMINAL ---
st.set_page_config(page_title="Operation: Red Kryptonite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 550px; overflow-y: auto;
    }
    .stButton>button { background-color: #ff0000; color: black; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHORIZATION GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<h2 style='text-align:center; color:#ff0000;'>KRYPTONIAN ACCESS</h2>", unsafe_allow_html=True)
        u = st.text_input("ID")
        p = st.text_input("CRYPT", type="password")
        if st.button("AUTHORIZE"):
            if u == "clark_kent" and p == "superman":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED.")
    st.stop()

# --- SIDEBAR ARSENAL ---
with st.sidebar:
    st.markdown("### 🛠️ KRYPTONIAN ARMORY")
    if st.button("PRIME ELITE WEAPONS"):
        with st.spinner("RELOADING..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.success("Armory Status: ELITE")
    
    st.markdown("---")
    st.markdown("### 🕵️ MODULAR TOGGLES")
    p2 = st.toggle("PHASE 2: WAYBACK LENS", value=True)
    p25 = st.toggle("PHASE 2.5: SECRET SNIPER", value=True)
    p3 = st.toggle("PHASE 3: GRAPPLING HOOK", value=True)
    p35 = st.toggle("PHASE 3.5: VISUAL RECON", value=False)

# --- MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ LEDGER", "🖼️ GALLERY"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        target = st.text_input("🎯 ROOT TARGET (Seed)")
        in_scope = st.text_area("✓ IN-SCOPE (Manual List)")
        out_scope = st.text_input("✗ OUT-OF-SCOPE (Filters)")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if target or in_scope:
                terminal = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope),
                    "OUT_SCOPE": str(out_scope),
                    "WAYBACK": "1" if p2 else "0",
                    "SECRETS": "1" if p25 else "0",
                    "PORTS": "1" if p3 else "0",
                    "VISUAL": "1" if p35 else "0"
                })
                
                p = subprocess.Popen(["bash", "powers.sh", "strike", target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env)
                
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()
            else:
                st.error("MISSION ABORTED: TARGET/SCOPE REQUIRED.")
