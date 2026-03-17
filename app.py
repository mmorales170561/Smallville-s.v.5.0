import streamlit as st
import subprocess
import os
import time

# --- AUTH & SUPERMAN THEME ENGINE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

st.set_page_config(page_title="METROPOLIS_WATCHTOWER", layout="wide")

# CSS for Superman Background and Phosphor UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                    url('https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
        color: #33ff33; 
        font-family: 'Courier New', monospace;
    }
    
    /* Shield-styled header */
    h1 {
        color: #ff0000 !important;
        text-shadow: 2px 2px #0000ff;
        text-transform: uppercase;
        border-bottom: 2px solid #ff0000;
    }

    /* Terminal Input Styling */
    input, textarea { 
        background-color: rgba(0, 0, 0, 0.7) !important; 
        color: #33ff33 !important; 
        border: 1px solid #ff0000 !important; 
    }

    /* Action Button - Superman Colors */
    .stButton>button { 
        background-color: #0000ff; 
        color: #ffffff; 
        border: 2px solid #ff0000; 
        font-weight: bold;
        width: 100%;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        color: #0000ff;
    }

    pre { 
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: #33ff33 !important; 
        border: 1px solid #0000ff !important;
    }
    </style>
""", unsafe_allow_html=True)

BANNER = r"""
    ___  ____________________  _   __  __________  __  __________________
   /   |/ ____/_  __/  _/ __ \/ | / / / ____/ __ \/  |/  /  _/ ____/ ___/
  / /| / /     / /  / // / / /  |/ / / /   / / / / /|_/ // // /    \__ \ 
 / ___ / /___ / / _/ // /_/ / /|  / / /___/ /_/ / /  / // // /___ ___/ / 
/_/  |_\____//_/ /___/\____/_/ |_/  \____/\____/_/  /_/___/\____//____/ 
"""

# --- AUTO-PROVISIONING ---
@st.cache_resource
def provision_tools():
    if not os.path.exists("/tmp/bin/subfinder"):
        with st.status(">> [SYSTEM] INITIALIZING KRYPTONIAN_TOOLSET..."):
            install_cmd = """
            mkdir -p /tmp/bin
            wget -q -O /tmp/go.tar.gz https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
            tar -C /tmp -xzf /tmp/go.tar.gz
            export PATH=$PATH:/tmp/go/bin
            export GOBIN=/tmp/bin
            /tmp/go/bin/go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
            /tmp/go/bin/go install github.com/projectdiscovery/httpx/cmd/httpx@latest
            /tmp/go/bin/go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
            """
            subprocess.run(install_cmd, shell=True, executable='/bin/bash')
    return True

# --- LOGIN GATE ---
if not st.session_state['auth']:
    st.code(BANNER)
    st.markdown("### 🔒 ACTION COMICS LOGIN")
    pwd = st.text_input("Enter Keyphrase (Password):", type="password")
    if pwd == "superman":
        st.session_state['auth'] = True
        st.rerun()
    st.stop()

# --- THE DAILY PLANET DESK ---
provision_tools()
st.title("🗞️ THE DAILY PLANET: WATCHTOWER")
st.code(BANNER)

# 1. Targeting & Scope
c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST")
    in_scope = st.text_area(">> SET_IN_SCOPE")
with c2:
    out_scope = st.text_area(">> SET_OUT_SCOPE")

# 2. Module Selection
ability_label = st.selectbox(">> SELECT_POWER", ["Observer", "Kingpin", "Automated Hunt"])
mapping = {"Observer": "observer", "Kingpin": "kingpin", "Automated Hunt": "automated_hunt"}
ability = mapping[ability_label]

# 3. Execution
if st.button(">> INITIALIZE_MISSION"):
    if not target:
        st.error(">> [ERR] NO_TARGET_SPECIFIED")
    else:
        console = st.empty()
        full_log = ""
        with st.spinner(f">> [BUSY] {ability_label.upper()} ENGAGED..."):
            try:
                env = os.environ.copy()
                env["PATH"] = f"/tmp/bin:{env.get('PATH', '')}"
                env["OUT_SCOPE"] = out_scope
                env["IN_SCOPE"] = in_scope

                process = subprocess.Popen(
                    ["bash", "powers.sh", ability, target],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env
                )

                for line in iter(process.stdout.readline, ''):
                    full_log += line
                    console.code(full_log)
                
                process.wait()
                
                if full_log.strip():
                    st.success(">> [SUCCESS] MISSION ACCOMPLISHED.")
                    st.download_button("📥 DOWNLOAD_INTEL", full_log, f"DailyPlanet_{target}.txt")
            except Exception as e:
                st.error(f">> [FATAL] LEX_CORP_INTERFERENCE: {str(e)}")
