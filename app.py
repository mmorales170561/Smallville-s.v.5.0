import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# --- 2026 PATH INJECTION ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

# --- THEME: KRYPTONIAN TERMINAL ---
st.set_page_config(page_title="Operation: Red Kryptonite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; 
        border: 1px solid #ff0000; 
        padding: 20px; 
        color: #ff0000;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        height: 500px;
        overflow-y: auto;
    }
    .stButton>button { background-color: #ff0000; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ARSENAL ---
with st.sidebar:
    st.markdown("### 🛠️ KRYPTONIAN ARMORY")
    if st.button("PRIME ELITE WEAPONS"):
        with st.spinner("Syncing..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.success("Armory Status: ELITE")
    
    st.markdown("---")
    wayback = st.toggle("WAYBACK LENS", value=True)
    secrets = st.toggle("SECRET SNIPER", value=False)
    visual = st.toggle("VISUAL RECON", value=False)
    ports = st.toggle("GRAPPLING HOOK", value=True)

# --- MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
target = st.text_input("🎯 TARGET")

if st.button("FIRE RED KRYPTONITE GUN"):
    if target:
        terminal = st.empty()
        # Initialize env with toggles
        strike_env = os.environ.copy()
        strike_env.update({
            "WAYBACK": "1" if wayback else "0",
            "SECRETS": "1" if secrets else "0",
            "VISUAL": "1" if visual else "0",
            "PORTS": "1" if ports else "0"
        })
        
        p = subprocess.Popen(["bash", "powers.sh", "strike", target], 
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env)
        
        output = ""
        for line in iter(p.stdout.readline, ''):
            output += line
            terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
        p.wait()
