import streamlit as st
import subprocess
import os
import time

# --- AUTH & SUPERMAN "ACTION COMICS" THEME ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

st.set_page_config(page_title="ACTION_COMICS_TERMINAL", layout="wide")

st.markdown("""
    <style>
    /* Primary Superman Palette */
    .stApp { 
        background-color: #003366; /* Deep Blue */
        color: #FFFF00;            /* Bright Yellow */
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Shield Headers */
    h1, h2, h3 { 
        color: #FF0000 !important; /* Superman Red */
        text-transform: uppercase;
        border-bottom: 2px solid #FFFF00;
        text-shadow: 2px 2px #000;
    }

    /* Terminal Inputs */
    input, textarea { 
        background-color: #002244 !important; 
        color: #FFFF00 !important; 
        border: 2px solid #FF0000 !important;
        text-transform: uppercase;
    }
    
    /* Labels */
    label, p, .stMarkdown {
        color: #FFFF00 !important;
        font-weight: bold !important;
    }

    /* Action Buttons */
    .stButton>button { 
        background-color: #FF0000; 
        color: #FFFF00; 
        border: 2px solid #FFFF00;
        font-weight: bold;
        border-radius: 0;
        box-shadow: 4px 4px #000;
    }
    .stButton>button:hover {
        background-color: #FFFF00;
        color: #FF0000;
        border: 2px solid #FF0000;
    }

    /* Code/Terminal Output */
    pre { 
        background-color: #000000 !important; 
        color: #33ff33 !important; /* Keep output green for high legibility */
        border: 2px solid #FF0000 !important;
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
    st.markdown("### 🛑 AUTHORIZATION REQUIRED")
    pwd = st.text_input("PASSWORD:", type="password")
    if pwd == "superman":
        st.session_state['auth'] = True
        st.rerun()
    elif pwd:
        st.error(">> ACCESS DENIED: KRYPTONITE DETECTED")
    st.stop()

# --- THE WATCHTOWER DESK ---
provision_tools()
st.title("🗞️ DAILY PLANET: WATCHTOWER")
st.code(BANNER)

# 1. Targeting & Scope
c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST")
    in_scope = st.text_area(">> IN_SCOPE")
with c2:
    out_scope = st.text_area(">> OUT_SCOPE")

# 2. Module Selection
ability_label = st.selectbox(">> SELECT_POWER", ["Observer", "Kingpin", "Automated Hunt"])
mapping = {"Observer": "observer", "Kingpin": "kingpin", "Automated Hunt": "automated_hunt"}
ability = mapping[ability_label]

# 3. Execution
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
                    # Keeps the terminal scroll look inside the colorful UI
                    console.code(full_log)
                
                process.wait()
                
                if full_log.strip():
                    st.success(">> MISSION ACCOMPLISHED.")
                    st.download_button("📥 DOWNLOAD INTEL", full_log, f"Intel_{target}.txt")
            except Exception as e:
                st.error(f">> FATAL ERROR: {str(e)}")
