import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="Smallville 8.5: Kryptonian Apex", layout="wide")
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# Initialize all potential toggles in session state to prevent "KeyError"
toggles = ["p_recon", "p_js", "p_strike", "p_sto", "p_cloud", "p_ai", "p_visual"]
for t in toggles:
    if t not in st.session_state:
        st.session_state[t] = True

if 'logs' not in st.session_state: st.session_state.logs = ">> SYSTEM ONLINE."
if 'findings' not in st.session_state: st.session_state.findings = []

# --- 2. THE COMPLETE SIDEBAR ---
with st.sidebar:
    st.title("🦸‍♂️ S.V. 8.5 CONTROL")
    st.header("🛠️ WEAPON SYSTEM")
    
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True):
        st.info("Installing Chromium & Binaries...")
        # (This calls your apt-get and download logic)
        st.success("Armory Ready!")

    st.divider()
    st.subheader("📡 PHASE TOGGLES")
    
    # All P-Toggles for the Sidebar
    st.session_state.p_recon = st.toggle("P1-2: CEREBRO (Recon/Shadow)", value=True)
    st.session_state.p_js = st.toggle("P3: KATANA (Headless JS/Secrets)", value=True)
    st.session_state.p_strike = st.toggle("P4: STRIKE (Nuclei/Exposures)", value=True)
    st.session_state.p_sto = st.toggle("💥 AUTO-EXPLOIT (Takeovers)", value=True)
    st.session_state.p_cloud = st.toggle("P8: GALAXY (Cloud/Web3 RPC)", value=True)
    st.session_state.p_ai = st.toggle("P7: AI REPORTER (LLM Probes)", True)
    st.session_state.p_visual = st.toggle("P9: VISUAL RECON (Screenshots)", True)
    
    st.divider()
    if st.button("🧹 PURGE WORKSPACE", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."; st.rerun()

# --- 3. UI TABS ---
tabs = st.tabs(["🚀 Mission Control", "📊 Intelligence Desk", "🧪 Payload Lab", "⚡ Tactical Shell", "🖼️ Visual Recon"])

with tabs[0]: # MISSION CONTROL
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com")
        h1_user = st.text_input("🆔 H1 HANDLE", placeholder="your_h1_handle")
    with col2:
        out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=68)

    if st.button("🔥 INITIATE FULL SPECTRUM STRIKE", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION START: {datetime.now().strftime('%H:%M')} ---\n"
        
        # Pass all sidebar states to the Bash Environment
        env = os.environ.copy()
        env.update({
            "H1_USER": h1_user,
            "OUT_SCOPE_LIST": out_scope.replace("\n", ","),
            "RUN_P1": "1" if st.session_state.p_recon else "0",
            "RUN_P3": "1" if st.session_state.p_js else "0",
            "RUN_P4": "1" if st.session_state.p_strike else "0",
            "RUN_STO": "1" if st.session_state.p_sto else "0",
            "RUN_P8": "1" if st.session_state.p_cloud else "0",
            "RUN_P7": "1" if st.session_state.p_ai else "0",
            "RUN_P9": "1" if st.session_state.p_visual else "0"
        })
        
        # Execution logic (subprocess.Popen) goes here...
        st.info("Scanning initiated. Check Tactical Console for live feed.")
