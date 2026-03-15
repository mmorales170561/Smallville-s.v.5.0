import streamlit as st
import subprocess
import os
import time

# --- AUTH & THEME ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

st.set_page_config(page_title="ACTION_COMICS_TERMINAL", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #33ff33; font-family: 'Courier New', monospace; }
    input, textarea { background-color: #000 !important; color: #33ff33 !important; border: 1px solid #33ff33 !important; }
    pre { color: #33ff33 !important; font-size: 10px !important; }
    .stButton>button { background-color: transparent; color: #33ff33; border: 1px solid #33ff33; width: 100%; }
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
            """
            subprocess.run(install_cmd, shell=True, executable='/bin/bash')
    return True

# --- LOGIN ---
if not st.session_state['auth']:
    st.code(BANNER)
    pwd = st.text_input("Password:", type="password")
    if pwd == "superman":
        st.session_state['auth'] = True
        st.rerun()
    st.stop()

# --- MAIN INTERFACE ---
provision_tools()
st.code(BANNER)

c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST (e.g. example.com)")
    in_scope = st.text_area(">> IN_SCOPE")
with c2:
    out_scope = st.text_area(">> OUT_SCOPE")

ability = st.selectbox(">> MODULE", ["Observer", "Kingpin"])

if st.button(">> FILE_THE_STORY"):
    if not target:
        st.error(">> [ERR] NO_TARGET_SPECIFIED")
    else:
        with st.spinner(">> [BUSY] SCANNING..."):
            try:
                env = os.environ.copy()
                env["PATH"] = f"/tmp/bin:{env.get('PATH', '')}"
                env["OUT_SCOPE"] = out_scope
                
                # Execute
                root_path = os.getcwd()
                powers_path = os.path.join(root_path, "powers.sh")
                
                cmd = f"source {powers_path} && {ability.lower()} '{target}'"
                result = subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT, env=env)
                
                output = result.decode('utf-8')
                
                if not output.strip():
                    st.warning(">> [WARN] REPORTER_RETURNED_NO_DATA. Check if subdomains exist for this target.")
                else:
                    st.markdown("### >> RESULTS")
                    st.code(output)
                    st.download_button("📥 DOWNLOAD_REPORT", output, f"report_{target}.txt")
                    
            except Exception as e:
                st.error(f">> [CRITICAL_FAILURE]: {str(e)}")
