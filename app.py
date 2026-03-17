import streamlit as st
import subprocess
import os
import requests
import zipfile
import io
from datetime import datetime

# --- 1. INITIALIZE (MUST BE FIRST) ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

# Initialize session states
if 'terminal_logs' not in st.session_state: 
    st.session_state['terminal_logs'] = "READY FOR ENGAGEMENT..."
if 'vuln_counts' not in st.session_state:
    st.session_state['vuln_counts'] = {"critical": 0, "high": 0, "medium": 0}

# --- 3. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 13px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5); border-radius: 5px;
    }
    .vuln-stat { padding: 8px; border-radius: 5px; text-align: center; font-weight: bold; border: 1px solid #444; }
    .crit { color: #ff0000; border-color: #ff0000; background: rgba(255,0,0,0.1); }
    .high { color: #ffae00; border-color: #ffae00; background: rgba(255,174,0,0.1); }
    .med { color: #ffff00; border-color: #ffff00; background: rgba(255,255,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (CONSOLIDATED) ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        with st.spinner("Unlocking Armory..."):
            # Your prime_armory() logic here
            st.success("Armory Primed.")
            st.rerun()

    st.divider()
    st.subheader("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: KATANA", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
    p5 = st.toggle("P5: ARCHITECT", value=True)
    p6 = st.toggle("P6: OLYMPUS", value=True)
    
    st.divider()
    stealth = st.toggle("🕵️ STEALTH MODE", value=False)
    
    if st.button("🗑️ PURGE WORKSPACE", use_container_width=True):
        st.session_state['terminal_logs'] = "READY..."
        st.session_state['vuln_counts'] = {"critical": 0, "high": 0, "medium": 0}
        st.rerun()

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", placeholder="Project X")
    ru = st.text_input("🔗 ROOT URL", placeholder="example.com")
    gh_repo = st.text_input("🐙 GITHUB REPO URL")
    
    c_scope1, c_scope2 = st.columns(2)
    with c_scope1:
        is_scope = st.text_area("✓ IN-SCOPE", height=80)
    with c_scope2:
        os_scope = st.text_area("✗ OUT-SCOPE", height=80)
    
    st.write("**Vulnerability Tracker:**")
    v = st.session_state['vuln_counts']
    v1, v2, v3 = st.columns(3)
    v1.markdown(f'<div class="vuln-stat crit">{v["critical"]}<br><small>CRIT</small></div>', unsafe_allow_html=True)
    v2.markdown(f'<div class="vuln-stat high">{v["high"]}<br><small>HIGH</small></div>', unsafe_allow_html=True)
    v3.markdown(f'<div class="vuln-stat med">{v["medium"]}<br><small>MED</small></div>', unsafe_allow_html=True)

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if tn and ru:
            st.session_state['terminal_logs'] = f"--- MISSION START: {tn} ---\n"
            term_placeholder = st.empty()
            
            # Logic to execute powers.sh...
            # (Ensure you pass in_scope and os_scope in the env)
            
with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
