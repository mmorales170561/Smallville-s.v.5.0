import streamlit as st
import subprocess, os, requests, zipfile, tarfile, io, shutil
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'logs' not in st.session_state: st.session_state.logs = ">> SYSTEM READY."
if 'vuln_data' not in st.session_state: st.session_state.vuln_data = []

# --- 3. UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 15px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 450px; overflow-y: auto; font-size: 11px;
        box-shadow: inset 0 0 15px rgba(255,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE ROBUST LOADER ---
def prime_armory():
    URLS = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
    }
    
    os.makedirs(BIN_PATH, exist_ok=True)
    
    # Using st.status to prevent UI hanging
    with st.sidebar.status("🔓 Unlocking Armory...", expanded=True) as status:
        for name, url in URLS.items():
            try:
                status.write(f"Downloading {name}...")
                r = requests.get(url, timeout=60, stream=True) # Increased timeout
                data = io.BytesIO(r.content)
                target = os.path.join(BIN_PATH, name)
                
                # Check for ZIP
                if zipfile.is_zipfile(data):
                    with zipfile.ZipFile(data) as z:
                        for f in z.namelist():
                            if f.endswith(name):
                                with open(target, "wb") as b: b.write(z.read(f))
                # Check for TAR/GZ
                else:
                    data.seek(0)
                    try:
                        mode = "r:gz" if "gz" in url else "r:"
                        with tarfile.open(fileobj=data, mode=mode) as t:
                            for m in t.getmembers():
                                if m.name.endswith(name):
                                    with open(target, "wb") as b: b.write(t.extractfile(m).read())
                    except:
                        # Direct Binary fallback
                        data.seek(0)
                        with open(target, "wb") as b: b.write(data.read())
                
                if os.path.exists(target):
                    os.chmod(target, 0o755)
                    status.write(f"✅ {name} Ready")
                else:
                    status.write(f"❌ {name} Failed to extract")
            except Exception as e:
                status.write(f"⚠️ Error {name}: {str(e)[:50]}")
        
        status.update(label="⚔️ Armory Fully Loaded!", state="complete", expanded=False)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("🔴 HARD RESET", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.session_state.vuln_data = []
        st.rerun()
    
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        prime_armory()

    st.divider()
    st.subheader("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True)
    p4 = st.toggle("P4: STRIKE", True)
    p5 = st.toggle("P5: ARCHITECT", False)
    p6 = st.toggle("P6: OLYMPUS", True)
    
    st.divider()
    force_root = st.toggle("🚀 FORCE ROOT SCAN", False)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 6. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1.1, 2])

with col_in:
    st.subheader("📝 Mission Brief")
    mission_name = st.text_input("🎯 MISSION NAME", f"S.V_{datetime.now().strftime('%H%M')}")
    target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com, x.com")
    
    with st.expander("🛡️ Rules of Engagement", expanded=True):
        in_scope = st.text_area("✓ IN-SCOPE", "syfe.com", height=60)
        out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=60)
    
    # Visual Metrics
    v_counts = {"CRIT": 0, "HIGH": 0, "MED": 0}
    for v in st.session_state.vuln_data:
        for lvl in v_counts.keys():
            if lvl.lower() in v.lower(): v_counts[lvl] += 1
    
    c1, c2, c3 = st.columns(3)
    c1.metric("CRIT", v_counts["CRIT"])
    c2.metric("HIGH", v_counts["HIGH"])
    c3.metric("MED", v_counts["MED"])

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION: {mission_name} START ---\n"
        st.session_state.vuln_data = []
        
        env = os.environ.copy()
        env.update({
            "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "FORCE_ROOT": "1" if force_root else "0",
            "RUN_STEALTH": "1" if stealth else "0",
            "OUT_SCOPE": out_scope
        })
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        with col_term:
            term_placeholder = st.empty()
            proc = subprocess.Popen(["bash", SCRIPT_PATH, "strike", target_url, mission_name], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
            for line in iter(proc.stdout.readline, ""):
                st.session_state.logs += line
                term_placeholder.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)
                if any(lvl in line.lower() for lvl in ["[critical]", "[high]", "[medium]"]):
                    st.session_state.vuln_data.append(line.strip())
            proc.wait()

with col_term:
    if 'term_placeholder' not in locals():
        st.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)
