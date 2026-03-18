import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. INITIALIZE & PATHS ---
st.set_page_config(page_title="Smallville S.V. 5.5", layout="wide")
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'logs' not in st.session_state: 
    st.session_state.logs = ">> SYSTEM READY. MISSION STANDBY."

# --- 2. THE ARMORY (Prime Tools) ---
def prime_armory():
    if not os.path.exists(BIN_PATH): os.makedirs(BIN_PATH)
    tools = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
    }
    with st.sidebar.status("🔓 Unlocking Armory...", expanded=True) as status:
        for tool, url in tools.items():
            try:
                status.write(f"📥 Priming {tool}...")
                r = requests.get(url, timeout=30)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                for f in z.namelist():
                    if f.endswith(tool):
                        with open(f"{BIN_PATH}/{tool}", "wb") as b: b.write(z.read(f))
                os.chmod(f"{BIN_PATH}/{tool}", 0o755)
            except Exception as e:
                status.write(f"❌ Error priming {tool}: {e}")
        status.update(label="⚔️ Armory Fully Loaded!", state="complete", expanded=False)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True):
        prime_armory()
    
    if st.button("🔴 HARD RESET", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.session_state.logs = ">> SYSTEM WIPED."
        st.rerun()
    
    st.divider()
    st.subheader("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO (Subdomains)", True)
    p2 = st.toggle("P2: SHADOW (Alive Check)", True)
    p3 = st.toggle("P3: KATANA (Deep Crawl)", True)
    p4 = st.toggle("P4: STRIKE (Vuln Scan)", True)
    p5 = st.toggle("P5: ARCHITECT (AI/GitHub)", True)
    p6 = st.toggle("P6: OLYMPUS (Heavy Fuzz)", True)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 4. MAIN HUD ---
st.title("SUPER//MAN: AI-READY HUD")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    st.subheader("📝 Mission Brief")
    target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com")
    h1_user = st.text_input("🆔 H1 USERNAME", placeholder="your_h1_handle")
    
    with st.expander("🛡️ Rules of Engagement", expanded=True):
        out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=60)
    
    overlap = any(d.strip() in out_scope for d in target_url.split(",")) if out_scope else False
    btn_label = "⚠️ OUT-SCOPE OVERLAP (FIRE?)" if overlap else "FIRE RED KRYPTONITE GUN"
    
    if st.button(btn_label, type="primary" if not overlap else "secondary", use_container_width=True):
        st.session_state.logs = f"--- MISSION START: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
        
        env = os.environ.copy()
        env.update({
            "H1_USER": h1_user if h1_user else "User",
            "OUT_SCOPE_LIST": out_scope.replace("\n", ","),
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "RUN_STEALTH": "1" if stealth else "0"
        })
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        process = subprocess.Popen(
            ["bash", SCRIPT_PATH, "strike", target_url],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True, bufsize=1
        )
        
        term_placeholder = st.empty()
        for line in iter(process.stdout.readline, ""):
            st.session_state.logs += line
            term_placeholder.code(st.session_state.logs[-5000:], language="bash")
        process.wait()

    if "MISSION COMPLETE" in st.session_state.logs:
        st.success("✅ MISSION COMPLETE")
        st.download_button("💾 DOWNLOAD MISSION REPORT", st.session_state.logs, file_name=f"mission_report.txt")

with col_term:
    st.subheader("📟 Tactical Console")
    st.code(st.session_state.logs, language="bash")
