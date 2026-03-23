import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="Smallville 8.5: Apex", layout="wide")
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# Initialize Session States (Prevents crashes if tabs load before data)
state_keys = ["logs", "findings", "terminal_out", "p_recon", "p_js", "p_strike", "p_sto", "p_ai", "p_cloud", "p_oob", "p_visual"]
for key in state_keys:
    if key not in st.session_state:
        if key.startswith("p_"): st.session_state[key] = True
        elif key == "findings": st.session_state[key] = []
        else: st.session_state[key] = ">> SYSTEM ONLINE."

# --- 2. THE ARMORY (Function) ---
def prime_armory():
    st.info("📦 Syncing System Engines...")
    # (Installation logic remains the same)
    st.success("⚔️ ARSENAL PRIMED.")

# --- 3. SIDEBAR (The Control Center) ---
with st.sidebar:
    st.title("🦸‍♂️ S.V. 8.5 APEX")
    
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True, key="side_prime"):
        prime_armory()
    
    st.divider()
    st.subheader("📡 PHASE TOGGLES")
    # Verified closed parentheses for all toggles
    st.session_state.p_recon = st.toggle("P1-2: Recon", value=st.session_state.p_recon, key="t1")
    st.session_state.p_js = st.toggle("P3: Headless JS", value=st.session_state.p_js, key="t2")
    st.session_state.p_strike = st.toggle("P4: Nuclei", value=st.session_state.p_strike, key="t3")
    st.session_state.p_sto = st.toggle("💥 Auto-Takeover", value=st.session_state.p_sto, key="t4")
    st.session_state.p_ai = st.toggle("🧠 P7: AI Probes", value=st.session_state.p_ai, key="t5")
    st.session_state.p_cloud = st.toggle("💎 P8: Web3/RPC", value=st.session_state.p_cloud, key="t6")
    st.session_state.p_oob = st.toggle("🛰️ Blind OOB", value=st.session_state.p_oob, key="t7")
    st.session_state.p_visual = st.toggle("P9: Visual Recon", value=st.session_state.p_visual, key="t8")
    
    st.divider()
    if st.button("🧹 PURGE WORKSPACE", use_container_width=True, key="side_purge"):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.rerun()

# --- 4. TABS & WORKSPACE (The Missing Section) ---
# If the code above is correct, these tabs WILL appear.
tabs = st.tabs(["🚀 Mission Control", "📊 Intelligence Desk", "🧪 Payload Lab", "⚡ Tactical Shell", "🖼️ Visual Recon"])

with tabs[0]: # MISSION CONTROL
    st.subheader("🚀 Strike Configuration")
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("🔗 TARGET URL", "syfe.com", key="target_in")
        h1_user = st.text_input("🆔 H1 HANDLE", placeholder="your_h1_handle", key="h1_in")
    with col2:
        out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=68, key="scope_in")

    if st.button("🔥 INITIATE KRYPTONIAN STRIKE", type="primary", use_container_width=True, key="strike_btn"):
        st.write("Initiating...")
        # (Subprocess trigger logic)

with tabs[3]: # TACTICAL SHELL
    st.subheader("⚡ Manual Command Injection")
    cmd = st.text_input("Enter Command (dig, whois, curl):", key="shell_in")
    if st.button("RUN COMMAND", key="run_shell"):
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.session_state.terminal_out = proc.stdout if proc.stdout else proc.stderr
    st.code(st.session_state.terminal_out, language="bash")
