import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil

# --- 1. HUD CONFIGURATION (SAFE MODE) ---
st.set_page_config(page_title="RUBY-OPERATOR v2.8", layout="wide")

# Simplified CSS to prevent "Blackout"
st.markdown("""
    <style>
    /* Dark background but keeps content visible */
    .stApp { background-color: #050505; color: #ff3131; }
    /* Ensure text is always bright neon */
    h1, h2, h3, p, span { color: #ff3131 !important; }
    /* Terminal styling */
    .terminal { 
        background-color: #000; 
        color: #00ff00; 
        padding: 15px; 
        border: 2px solid #ff3131; 
        font-family: 'Courier New', monospace; 
        height: 300px; 
        overflow-y: scroll; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY & SCOPE ENGINE ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# Initialize Session State
for key, val in {
    'last_log': "SYSTEM REBOOTED: SAFE MODE ACTIVE",
    'target': "example.com",
    'in_scope': "example.com",
    'out_scope': ".gov, .mil, localhost"
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 3. SIDEBAR: OPERATOR CONSOLE ---
with st.sidebar:
    st.title("🔴 OPERATOR")
    battery = st.selectbox("BATTERY", ["Ghost", "Strike", "Katana", "DeFi"])
    
    if st.button("🔌 PRIME"):
        st.info(f"Priming {battery}...")
        # (Tool fabrication logic stays here)
        
    st.divider()
    if st.button("💀 PURGE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        st.rerun()

# --- 4. THE MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.0")
tabs = st.tabs(["🛡️ ROE", "🚀 STRIKE", "📊 INTEL"])

with tabs[0]: 
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", st.session_state.in_scope)
    st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE", st.session_state.out_scope)

with tabs[1]:
    target = st.text_input("🎯 TARGET", st.session_state.target)
    # Basic firing button for testing visibility
    if st.button("🔥 TEST FIRE"):
        st.session_state.last_log = f"Test strike initiated on {target}..."

# --- 5. LIVE HUD ---
st.divider()
st.subheader("📟 TERMINAL")
st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
