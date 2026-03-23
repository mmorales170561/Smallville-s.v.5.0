import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. CORE CONFIG & PATHS ---
st.set_page_config(page_title="Smallville 8.5: Apex", layout="wide")
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# Initialize Session States
state_keys = ["logs", "findings", "terminal_out", "p_recon", "p_js", "p_strike", "p_sto", "p_ai", "p_cloud", "p_oob", "p_visual"]
for key in state_keys:
    if key not in st.session_state:
        if key.startswith("p_"): st.session_state[key] = True
        elif key == "findings": st.session_state[key] = []
        else: st.session_state[key] = ">> SYSTEM ONLINE."

# --- 2. THE ARMORY (Installation Logic) ---
def prime_armory():
    st.info("📦 Syncing System Engines...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "chromium", "chromium-driver", "dnsutils"], check=True)
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
    except Exception as e:
        st.error(f"Installation Error: {e}")

# --- 3. SIDEBAR (The Control Center) ---
with st.sidebar:
    st.title("🦸‍♂️ S.V. 8.5 APEX")
    
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True, key="side_prime"):
        prime_armory()
    
    st.divider()
    st.subheader("📡 PHASE TOGGLES")
    st.session_state.p_recon = st.toggle("P1-2: Recon", value=st.session_state.p_recon, key="t1")
    st.session_state.p_js = st.toggle("P3: Headless JS", value=st.session_state.p_js, key="t2")
    st.session_state.p_strike = st.toggle("P4: Nuclei", value=st.session_state.p_strike, key="t3")
    st.session_state.p_sto = st.toggle("💥 Auto-Takeover", value=st.session_state.p_sto, key="t4")
    st.session_state.p_ai = st.toggle("🧠 P7: AI Probes", value=st.session_state.p_ai, key="t5")
    st.session_state.p_cloud = st.toggle("💎 P8: Web3/RPC", value=st.session_state.p_cloud, key="t6")
    # Corrected Toggle Block
    st.session_state.p_oob = st.toggle("🛰️ Blind OOB", value=st.session_state.p_oob, key="t7")
    st.session_state.p_visual = st.toggle("P9: Visual Recon", value=st.session_state.p_visual, key="t8")
    
    st.divider()
    if st.button("🧹 PURGE WORKSPACE", use_container_width=True, key="side_purge"):
        if os.path.exists(BIN_PATH):
            shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.rerun()
