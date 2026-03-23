import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="Smallville 8.5: Apex", layout="wide")
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# Initialize Toggles & Session States
for key in ["logs", "findings", "terminal_out", "p_recon", "p_js", "p_strike", "p_sto", "p_cloud", "p_ai", "p_visual", "p_oob"]:
    if key not in st.session_state:
        if "p_" in key: st.session_state[key] = True
        elif key == "findings": st.session_state[key] = []
        else: st.session_state[key] = ">> SYSTEM READY."

# --- 2. ARMORY ENGINE (Chromium + Binaries) ---
def prime_armory():
    with st.sidebar:
        st.info("📦 Syncing System Dependencies...")
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "chromium", "chromium-driver", "dnsutils"], check=True)
            st.success("✅ System Engines Ready.")
        except: st.warning("⚠️ Sudo check failed. Ensure Chromium is installed manually.")

        if not os.path.exists(BIN_PATH): os.makedirs(BIN_PATH)
        tools = {
            "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
            "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
            "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
            "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
        }
        for tool, url in tools.items():
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            for f in z.namelist():
                if f.endswith(tool) and not f.endswith(('.md', '.txt')):
                    with open(f"{BIN_PATH}/{tool}", "wb") as b: b.write(z.read(f))
            os.chmod(f"{BIN_PATH}/{tool}", 0o755)
        st.success("⚔️ ARSENAL PRIMED.")

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🦸‍♂️ S.V. 8.5 APEX")
    
    # Line 71: Ensure this is indented exactly 4 spaces from 'with'
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True, key="sidebar_prime_btn"):
        prime_armory()
    
    st.divider()
    st.subheader("📡 PHASE TOGGLES")
    
    # All these must match the indentation of the 'if' above
    st.session_state.p_recon = st.toggle("P1-2: Recon", value=True, key="t1")
    st.session_state.p_js = st.toggle("P3: Headless JS", value=True, key="t2")
    st.session_state.p_strike = st.toggle("P4: Nuclei", value=True, key="t3")
    st.session_state.p_sto = st.toggle("💥 Auto-Takeover", value=True, key="t4")
    st.session_state.p_ai = st.toggle("🧠 P7: AI Probes", value=True, key="t5")
    st.session_state.p_cloud = st.toggle("💎 P8: Web3/RPC", value=True, key="t6")
    st.session_state.p_oob = st.toggle("🛰️ Blind OOB", value=True, key="t7")
    st.session_state.p_visual = st.toggle("P9: Visual Recon", value=True, key="t8")
    
    st.divider()
    if st.button("🧹 PURGE WORKSPACE", use_container_width=True, key="sidebar_purge"):
        if os.path.exists(BIN_PATH):
            shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.rerun()

# --- 4. MAIN TABS ---
tabs = st.tabs(["🚀 Mission Control", "📊 Intelligence Desk", "🧪 Payload Lab", "⚡ Tactical Shell", "🖼️ Visual Recon"])

with tabs[0]: # MISSION CONTROL
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("🔗 TARGET URL", "syfe.com")
   # --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🦸‍♂️ S.V. 8.5 APEX")
   if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True, key="sidebar_prime_btn"):
    prime_armory()
    
    st.divider()
    st.subheader("📡 PHASE TOGGLES")
    
    # Indented 4 spaces to stay inside the 'with' block
    st.session_state.p_recon = st.toggle("P1-2: Recon/Shadow", value=st.session_state.p_recon)
    st.session_state.p_js = st.toggle("P3: Headless JS/Secrets", value=st.session_state.p_js)
    st.session_state.p_strike = st.toggle("P4: Nuclei/Exposures", value=st.session_state.p_strike)
    st.session_state.p_sto = st.toggle("💥 Auto-Takeover Exploit", value=st.session_state.p_sto)
    st.session_state.p_ai = st.toggle("🧠 P7: AI Agent Probes", value=st.session_state.p_ai)
    st.session_state.p_cloud = st.toggle("💎 P8: Web3 RPC/Bridge", value=st.session_state.p_cloud)
    st.session_state.p_oob = st.toggle("🛰️ Blind OOB (Interactsh)", value=st.session_state.p_oob)
    st.session_state.p_visual = st.toggle("P9: Visual Recon", value=st.session_state.p_visual)
    
    st.divider()
    if st.button("🧹 PURGE WORKSPACE", use_container_width=True):
        if os.path.exists(BIN_PATH):
            shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.rerun()
