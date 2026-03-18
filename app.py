import streamlit as st
import subprocess, os, requests, zipfile, tarfile, io, shutil
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.2", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'logs' not in st.session_state: st.session_state.logs = ">> SYSTEM READY."
if 'vuln_data' not in st.session_state: st.session_state.vuln_data = []

# --- 3. UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto; font-size: 11px;
        box-shadow: inset 0 0 15px rgba(255,0,0,0.3); border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("🔴 HARD RESET", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.session_state.vuln_data = []
        st.rerun()
    
    # Tool priming logic goes here (as provided in v112)
    st.divider()
    p1 = st.toggle("P1: CEREBRO", True); p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True); p4 = st.toggle("P4: STRIKE", True)
    p6 = st.toggle("P6: OLYMPUS", True)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: AEGIS-GATED HUD")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    st.subheader("📝 Mission Brief")
    mission_name = st.text_input("🎯 MISSION NAME", f"S.V_{datetime.now().strftime('%H%M')}")
    target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com, x.com")
    h1_user = st.text_input("🆔 H1 USERNAME", placeholder="super__man")
    
    with st.expander("🛡️ Rules of Engagement", expanded=True):
        in_scope = st.text_area("✓ IN-SCOPE", "syfe.com", height=60)
        out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=60)
    
    # AEGIS LOGIC: Check for overlaps
    overlap = any(domain.strip() in out_scope for domain in target_url.split(","))
    
    button_label = "⚠️ TARGETS IN OUT-SCOPE (FIRE ANYWAY?)" if overlap else "FIRE RED KRYPTONITE GUN"
    button_type = "secondary" if overlap else "primary"

    if st.button(button_label, type=button_type, use_container_width=True):
        st.session_state.logs = f"--- MISSION: {mission_name} START ---\n"
        
        env = os.environ.copy()
        env.update({
            "H1_USER": h1_user if h1_user else "Smallville-User",
            "OUT_SCOPE_LIST": out_scope.replace("\n", ","),
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P6": "1" if p6 else "0",
            "RUN_STEALTH": "1" if stealth else "0"
        })
        
        # Subprocess execution logic here...
