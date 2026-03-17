import streamlit as st
import subprocess, os, requests, zipfile, tarfile, io, shutil

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'logs' not in st.session_state:
    st.session_state.logs = ">> SYSTEM READY. PRIME ARMORY TO BEGIN."
if 'oob_url' not in st.session_state:
    st.session_state.oob_url = "Click 'Generate OOB' in Sidebar"

# --- 3. KRYPTONIAN UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 550px; overflow-y: auto; font-size: 12px;
        box-shadow: inset 0 0 15px rgba(255,0,0,0.3); border-radius: 5px;
    }
    .oob-box { 
        background: #111; border: 1px dashed #00ff41; padding: 10px; 
        color: #00ff41; font-size: 14px; text-align: center; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE UNIVERSAL LOADER ---
def prime_armory():
    URLS = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
    }
    os.makedirs(BIN_PATH, exist_ok=True)
    status_bar = st.sidebar.empty()
    for name, url in URLS.items():
        try:
            status_bar.info(f"Unlocking {name}...")
            r = requests.get(url, timeout=30)
            data = io.BytesIO(r.content)
            target = os.path.join(BIN_PATH, name)
            if zipfile.is_zipfile(data):
                with zipfile.ZipFile(data) as z:
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(target, "wb") as b: b.write(z.read(f))
            else:
                data.seek(0)
                try:
                    mode = "r:gz" if "gz" in url else "r:"
                    with tarfile.open(fileobj=data, mode=mode) as t:
                        for m in t.getmembers():
                            if m.name.endswith(name):
                                with open(target, "wb") as b: b.write(t.extractfile(m).read())
                except:
                    data.seek(0)
                    with open(target, "wb") as b: b.write(data.read())
            if os.path.exists(target):
                os.chmod(target, 0o755)
                st.sidebar.success(f"✓ {name}")
        except Exception as e: st.sidebar.error(f"Err {name}: {e}")
    status_bar.empty()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("🔴 HARD RESET", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.rerun()
    
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        prime_armory()

    st.divider()
    st.subheader("📡 OOB LISTENER")
    if st.button("GENERATE OOB CALLBACK"):
        # Simple placeholder logic for OOB generation
        st.session_state.oob_url = f"https://{os.urandom(4).hex()}.oast.me"
    st.code(st.session_state.oob_url)
    st.caption("Use this for manual Blind SSRF/RCE tests.")

    st.divider()
    st.subheader("⚡ PHASES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True)
    p4 = st.toggle("P4: STRIKE", True)
    st.divider()
    force_root = st.toggle("🚀 FORCE ROOT SCAN", False)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 6. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1, 2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 MISSION NAME", "Operation Smallville")
    ru = st.text_input("🔗 ROOT URL", "x.com")
    os_scope = st.text_area("✗ OUT-SCOPE (Exclude these domains)", height=100)
    
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION START: {tn} ---\n"
        env = os.environ.copy()
        env.update({
            "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "FORCE_ROOT": "1" if force_root else "0",
            "RUN_STEALTH": "1" if stealth else "0",
            "OUT_SCOPE": os_scope,
            "OOB_URL": st.session_state.oob_url
        })
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        with col_term:
            term_placeholder = st.empty()
            proc = subprocess.Popen(["bash", SCRIPT_PATH, "strike", ru, tn], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
            for line in iter(proc.stdout.readline, ""):
                st.session_state.logs += line
                term_placeholder.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)
            proc.wait()

with col_term:
    if 'term_placeholder' not in locals():
        st.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)
