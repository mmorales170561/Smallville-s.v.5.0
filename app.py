import streamlit as st
import subprocess, os, requests, zipfile, tarfile, io, shutil
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

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
        box-shadow: inset 0 0 15px rgba(255,0,0,0.3);
    }
    .stats-card { background: #111; border: 1px solid #444; padding: 10px; border-radius: 5px; text-align: center; }
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
    
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        # (Downloader logic remains the same as v108)
        pass 

    st.divider()
    st.subheader("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO", True); p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True); p4 = st.toggle("P4: STRIKE", True)
    p5 = st.toggle("P5: ARCHITECT", False); p6 = st.toggle("P6: OLYMPUS", True)
    
    st.divider()
    force_root = st.toggle("🚀 FORCE ROOT SCAN", False)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1, 2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 MISSION NAME", f"S.V_{datetime.now().strftime('%H%M')}")
    ru = st.text_input("🔗 ROOT URL / TARGETS", "x.com")
    
    # Vulnerability Counter Dashboard
    c1, c2, c3 = st.columns(3)
    c1.metric("CRIT", len([x for x in st.session_state.vuln_data if "critical" in x.lower()]))
    c2.metric("HIGH", len([x for x in st.session_state.vuln_data if "high" in x.lower()]))
    c3.metric("MED", len([x for x in st.session_state.vuln_data if "medium" in x.lower()]))

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION START: {tn} ---\n"
        st.session_state.vuln_data = []
        
        env = os.environ.copy()
        env.update({
            "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "FORCE_ROOT": "1" if force_root else "0",
            "RUN_STEALTH": "1" if stealth else "0",
        })
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        with col_term:
            term_placeholder = st.empty()
            proc = subprocess.Popen(["bash", SCRIPT_PATH, "strike", ru, tn], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
            for line in iter(proc.stdout.readline, ""):
                st.session_state.logs += line
                term_placeholder.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)
                if any(lvl in line.lower() for lvl in ["[critical]", "[high]", "[medium]"]):
                    st.session_state.vuln_data.append(line.strip())
            proc.wait()

with col_term:
    if 'term_placeholder' not in locals():
        st.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)
