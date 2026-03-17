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

# --- AUTHORIZATION GATE ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h2 style='text-align:center; color:#ff0000;'>KRYPTONIAN ACCESS</h2>", unsafe_allow_html=True)
        user = st.text_input("ID", key="user_id")
        pwd = st.text_input("CRYPT", type="password", key="user_pwd")
        if st.button("AUTHORIZE"):
            if user == "clark_kent" and pwd == "superman":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED.")
    st.stop()

# --- SIDEBAR: THE ARSENAL ---
with st.sidebar:
    st.markdown("### 🛠️ KRYPTONIAN ARMORY")
    # Updated text to "Reloading..." as requested
    if st.button("PRIME ELITE WEAPONS"):
        with st.spinner("RELOADING..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.success("Armory Status: ELITE")
    
    st.markdown("---")
    st.markdown("### 🕵️ MODULAR TOGGLES")
    wayback = st.toggle("WAYBACK LENS", value=True)
    secrets = st.toggle("SECRET SNIPER", value=False)
    visual = st.toggle("VISUAL RECON", value=False)
    ports = st.toggle("GRAPPLING HOOK", value=True)

# --- MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")

t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ TARGET LEDGER", "🖼️ RECON GALLERY"])

with t1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Mission Brief")
        target = st.text_input("🎯 TARGET", placeholder="example.com")
        
        default_scope = ".".join(target.split(".")[-2:]) if target and "." in target else ""
        in_scope = st.text_input("✓ IN-SCOPE", value=default_scope)
        # Added Out-of-Scope Field
        out_scope = st.text_input("✗ OUT-OF-SCOPE", placeholder="dev.target.com, staging.target.com")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if target and in_scope:
                terminal = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope),
                    "OUT_SCOPE": str(out_scope), # Passing filter list to bash
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
            else:
                st.error("CRITICAL: TARGET AND SCOPE REQUIRED.")
