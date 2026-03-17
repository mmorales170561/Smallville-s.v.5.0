import streamlit as st
import subprocess
import os
import time

# --- AUTH & SUPERMAN "DAILY PLANET" THEME ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

st.set_page_config(page_title="DAILY_PLANET_ARCHIVE", layout="wide")

st.markdown("""
    <style>
    /* Superman Newspaper Background */
    .stApp { 
        background: linear-gradient(rgba(0, 51, 102, 0.8), rgba(0, 51, 102, 0.8)), 
                    url('http://googleusercontent.com/image_collection/image_retrieval/8297550412283012736_0');
        background-size: cover;
        background-attachment: fixed;
        color: #FFFF00;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Styled Action Comics Header */
    .action-header {
        font-family: 'Courier New', monospace;
        font-weight: 900;
        font-size: 1.2vw;
        line-height: 1.1;
        white-space: pre;
        background: linear-gradient(to right, #0000FF, #FF0000, #FFFF00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
    }

    /* Form Styling */
    h1, h2, h3 { 
        color: #FF0000 !important; 
        text-transform: uppercase;
        border-bottom: 2px solid #FFFF00;
    }

    input, textarea { 
        background-color: rgba(0, 34, 68, 0.9) !important; 
        color: #FFFF00 !important; 
        border: 2px solid #FF0000 !important;
    }

    label, p {
        color: #FFFF00 !important;
        font-weight: bold !important;
    }

    .stButton>button { 
        background-color: #FF0000; 
        color: #FFFF00; 
        border: 2px solid #FFFF00;
        font-weight: bold;
        box-shadow: 4px 4px #000;
    }

    pre { 
        background-color: rgba(0, 0, 0, 0.85) !important; 
        color: #33ff33 !important; 
        border: 1px solid #FF0000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# The New Styled Banner (HTML Gradient Version)
BANNER_HTML = """
<div class="action-header">
    ___  ____________________  _   __  __________  __  __________________
   /   |/ ____/_  __/  _/ __ \/ | / / / ____/ __ \/  |/  /  _/ ____/ ___/
  / /| / /     / /  / // / / /  |/ / / /   / / / / /|_/ // // /    \__ \ 
 / ___ / /___ / / _/ // /_/ / /|  / / /___/ /_/ / /  / // // /___ ___/ / 
/_/  |_\____//_/ /___/\____/_/ |_/  \____/\____/_/  /_/___/\____//____/ 
</div>
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
    st.markdown(BANNER_HTML, unsafe_allow_html=True)
    st.markdown("### 🛑 ACCESS RESTRICTED: DAILY PLANET PERSONNEL ONLY")
    pwd = st.text_input("PASSWORD:", type="password")
    if pwd == "superman":
        st.session_state['auth'] = True
        st.rerun()
    st.stop()

# --- THE MAIN TERMINAL ---
provision_tools()
st.markdown(BANNER_HTML, unsafe_allow_html=True)
st.title("🗞️ DAILY PLANET: THE WATCHTOWER")

c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST")
    in_scope = st.text_area(">> SET_IN_SCOPE")
with c2:
    out_scope = st.text_area(">> SET_OUT_SCOPE")

ability_label = st.selectbox(">> SELECT_POWER", ["Observer", "Kingpin", "Automated Hunt"])
mapping = {"Observer": "observer", "Kingpin": "kingpin", "Automated Hunt": "automated_hunt"}
ability = mapping[ability_label]

if st.button(">> INITIALIZE MISSION"):
    if not target:
        st.error(">> ERR: NO TARGET SPECIFIED")
    else:
        console = st.empty()
        full_log = ""
        with st.spinner(f">> BUSY: {ability_label.upper()} ENGAGED..."):
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
                    st.success(">> MISSION ACCOMPLISHED.")
                    st.download_button("📥 DOWNLOAD INTEL", full_log, f"DailyPlanet_{target}.txt")
            except Exception as e:
                st.error(f">> FATAL ERROR: {str(e)}")
