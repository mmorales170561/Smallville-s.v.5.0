import streamlit as st
import subprocess
import os
import time

# --- AUTH & TERMINAL THEME ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

st.set_page_config(page_title="ACTION_COMICS_TERMINAL", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #33ff33; font-family: 'Courier New', monospace; }
    input, textarea { background-color: #000 !important; color: #33ff33 !important; border: 1px solid #33ff33 !important; }
    pre { color: #33ff33 !important; font-size: 10px !important; line-height: 1.1 !important; }
    .stButton>button { background-color: transparent; color: #33ff33; border: 1px solid #33ff33; width: 100%; border-radius: 0; }
    .stButton>button:hover { background-color: #33ff33; color: #000; }
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
        with st.status(">> [SYSTEM] INSTALLING KRYPTONIAN_TOOLSET..."):
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
    pwd = st.text_input("Password:", type="password")
    if pwd == "superman":
        st.session_state['auth'] = True
        st.rerun()
    st.stop()

# --- THE DAILY PLANET DESK (RESTORED) ---
provision_tools()
st.code(BANNER)
st.write(">> WELCOME, AGENT_KENT. DAILY PLANET RECONNAISSANCE SUITE IS ONLINE.")

# 1. Targeting & Scope Inputs
c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST (e.g., example.com)")
    in_scope = st.text_area(">> SET_IN_SCOPE")
with c2:
    out_scope = st.text_area(">> SET_OUT_SCOPE")

# 2. Module Selection
ability_label = st.selectbox(">> SELECT_POWER", ["Observer", "Kingpin", "Automated Hunt"])
mapping = {
    "Observer": "observer",
    "Kingpin": "kingpin",
    "Automated Hunt": "automated_hunt"
}
ability = mapping[ability_label]

# 3. Execution & Live Console
if st.button(">> EXECUTE_WATCHTOWER_HUNT"):
    if not target:
        st.error(">> [ERR] NO_TARGET_SPECIFIED")
    else:
        # Create an empty container for real-time log streaming
        console = st.empty()
        full_log = ""
        
        with st.spinner(f">> [BUSY] {ability_label.upper()} ENGAGED..."):
            try:
                # Set Environment
                env = os.environ.copy()
                env["PATH"] = f"/tmp/bin:{env.get('PATH', '')}"
                env["OUT_SCOPE"] = out_scope
                env["IN_SCOPE"] = in_scope

                # Execute using Popen for live streaming
                process = subprocess.Popen(
                    ["bash", "powers.sh", ability, target],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    env=env
                )

                # Stream the output line by line to the console
                for line in iter(process.stdout.readline, ''):
                    full_log += line
                    console.code(full_log)
                
                process.wait()
                
                if full_log.strip():
                    st.success(">> [SUCCESS] SCAN COMPLETE.")
                    st.download_button("📥 DOWNLOAD_DAILY_PLANET_REPORT", full_log, f"Report_{target}.txt")
                else:
                    st.warning(">> [WARN] NO DATA RETURNED. CHECK TARGET OR SCOPE.")

            except Exception as e:
                st.error(f">> [CRITICAL_FAILURE]: {str(e)}")
