import streamlit as st
import subprocess
import os

# --- AUTHENTICATION STATE ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- TERMINAL STYLING ENGINE ---
st.set_page_config(page_title="ACTION_COMICS_TERMINAL", layout="wide")
st.markdown("""
    <style>
    .stApp { 
        background-color: #000000; 
        color: #33ff33; 
        font-family: 'Courier New', Courier, monospace;
        background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
    }
    h1, h2, h3, p, label, .stMarkdown, .stCodeBlock { color: #33ff33 !important; }
    input, textarea { background-color: #000 !important; color: #33ff33 !important; border: 1px solid #33ff33 !important; text-transform: uppercase; }
    pre { color: #33ff33 !important; background-color: transparent !important; border: none !important; font-size: 10px !important; line-height: 1.1 !important; }
    .stButton>button { background-color: transparent; color: #33ff33; border: 1px solid #33ff33; border-radius: 0; width: 100%; }
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

# --- AUTO-PROVISIONING (The Fortress Construction) ---
@st.cache_resource
def provision_tools():
    if not os.path.exists("/tmp/bin/subfinder"):
        try:
            os.makedirs("/tmp/bin", exist_ok=True)
            # Install Go and Tools via shell
            install_cmd = """
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
        except:
            return False
    return True

provision_tools()

# --- LOGIN GATE ---
if not st.session_state['auth']:
    st.code(BANNER)
    st.write(">> [UPLINK_ESTABLISHED_METROPOLIS_HUB]")
    col1, col2 = st.columns([1, 5])
    with col1: st.write("Password:")
    with col2: pwd = st.text_input("", type="password", label_visibility="collapsed", key="login_pwd")
    if pwd == "superman":
        st.session_state['auth'] = True
        st.rerun()
    elif pwd: st.error(">> [ERR] INVALID_KRYPTON_KEY")
    st.stop()

# --- RECON INTERFACE ---
st.code(BANNER)
st.write(">> WELCOME, AGENT_KENT. DAILY PLANET RECONNAISSANCE SUITE IS ONLINE.")

c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST")
    in_scope = st.text_area(">> SET_IN_SCOPE")
with c2:
    out_scope = st.text_area(">> SET_OUT_SCOPE")

ability = st.selectbox(">> SELECT_POWER", ["Observer", "Kingpin", "Automated Hunt"])

if st.button(">> FILE_THE_STORY"):
    with st.spinner(">> [BUSY] TYPING_REPORT..."):
        try:
            # Set up the execution environment
            env = os.environ.copy()
            env["PATH"] = f"{env.get('PATH', '')}:/tmp/bin"
            env["OUT_SCOPE"] = out_scope
            env["IN_SCOPE"] = in_scope
            
            root_path = os.getcwd()
            powers_path = os.path.join(root_path, "powers.sh")
            
            mapping = {"Observer": "observer", "Kingpin": "kingpin", "Automated Hunt": "automated_hunt"}
            cmd = f"source {powers_path} && {mapping[ability]} '{target}'"
            
            result = subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT, env=env)
            
            st.markdown("### >> BREAKING_NEWS_RESULTS")
            st.code(result.decode('utf-8'))
            st.download_button("📥 EXPORT_TELETYPE", result.decode('utf-8'), f"DP_Log_{target}.txt")
            
        except subprocess.CalledProcessError as e:
            st.error(f">> [CRITICAL_FAILURE] COMMAND_FAILED: {e.output.decode()}")
        except Exception as e:
            st.error(f">> [CRITICAL_FAILURE] SYSTEM_ERROR: {str(e)}")
