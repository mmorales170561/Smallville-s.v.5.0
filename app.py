import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. INITIALIZE & PATHS ---
st.set_page_config(page_title="Smallville S.V. 5.8", layout="wide")
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'logs' not in st.session_state: 
    st.session_state.logs = ">> SYSTEM READY. STANDBY FOR MISSION."

# --- 2. THE RESTORED ARMORY ENGINE ---
def prime_armory():
    if not os.path.exists(BIN_PATH): os.makedirs(BIN_PATH)
    
    # Using specific Linux amd64 builds for Chromebook/Crostini compatibility
    tools = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
    }
    
    with st.sidebar:
        progress_bar = st.progress(0)
        for i, (tool, url) in enumerate(tools.items()):
            st.write(f"📡 Downloading {tool}...")
            try:
                r = requests.get(url, timeout=30)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                # Search zip for the binary and extract
                for f in z.namelist():
                    if f.endswith(tool) and not f.endswith('.md'):
                        data = z.read(f)
                        with open(f"{BIN_PATH}/{tool}", "wb") as b:
                            b.write(data)
                os.chmod(f"{BIN_PATH}/{tool}", 0o755)
                progress_bar.progress((i + 1) / len(tools))
            except Exception as e:
                st.error(f"❌ {tool} Failed: {e}")
        st.success("⚔️ ARMORY READY.")

# --- 3. SIDEBAR (Restored Buttons) ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # RESTORED: Prime Button
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True):
        prime_armory()
    
    # RESTORED: Clear Workspace (Purge)
    if st.button("🧹 PURGE WORKSPACE", use_container_width=True, help="Wipes all binaries and temp logs"):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        if os.path.exists("/tmp/target_list.txt"): os.remove("/tmp/target_list.txt")
        st.session_state.logs = ">> WORKSPACE CLEARED."
        st.rerun()
    
    st.divider()
    st.subheader("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True)
    p4 = st.toggle("P4: STRIKE", True)
    p5 = st.toggle("P5: ARCHITECT", True)
    p6 = st.toggle("P6: OLYMPUS", True)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 4. MAIN HUD ---
st.title("SUPER//MAN: AEGIS COMMAND")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    st.subheader("🎯 Mission Brief")
    target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com")
    h1_user = st.text_input("🆔 H1 USERNAME", placeholder="hackerone_handle")

    st.subheader("🛡️ Aegis Scope")
    in_scope = st.text_area("✓ IN-SCOPE", "syfe.com", height=70)
    out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=70)

    # FIRE LOGIC
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION START: {datetime.now().strftime('%H:%M')} ---\n"
        
        env = os.environ.copy()
        env.update({
            "H1_USER": h1_user if h1_user else "User",
            "OUT_SCOPE_LIST": out_scope.replace("\n", ","),
            "IN_SCOPE_LIST": in_scope.replace("\n", ","),
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "RUN_STEALTH": "1" if stealth else "0"
        })
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        process = subprocess.Popen(["bash", SCRIPT_PATH, "strike", target_url], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                    env=env, text=True, bufsize=1)
        
        term_placeholder = st.empty()
        for line in iter(process.stdout.readline, ""):
            st.session_state.logs += line
            term_placeholder.code(st.session_state.logs[-4000:], language="bash")
        process.wait()

with col_term:
    st.subheader("📟 Tactical Console")
    st.code(st.session_state.logs, language="bash")
