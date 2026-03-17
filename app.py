import streamlit as st
import subprocess, os, requests, zipfile, io, shutil

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'full_output' not in st.session_state:
    st.session_state.full_output = ">> SYSTEM READY. PRIME ARMORY TO BEGIN."

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # NEW: HARD RESET BUTTON
    if st.button("🔴 HARD RESET (Wipe Binaries)", use_container_width=True):
        if os.path.exists(BIN_PATH):
            shutil.rmtree(BIN_PATH)
        st.session_state.full_output = ">> SYSTEM WIPED. RE-PRIME TOOLS."
        st.rerun()

    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        urls = {
            "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
            "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
            "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
            "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
            "airix": "https://github.com/projectdiscovery/airix/releases/download/v0.0.3/airix_0.0.3_linux_amd64.zip"
        }
        os.makedirs(BIN_PATH, exist_ok=True)
        for name, url in urls.items():
            with st.spinner(f"Unlocking {name}..."):
                try:
                    r = requests.get(url)
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(os.path.join(BIN_PATH, name), "wb") as b:
                                b.write(z.read(f))
                            os.chmod(os.path.join(BIN_PATH, name), 0o755)
                    st.success(f"✓ {name}")
                except Exception as e: st.error(f"Err: {e}")

    st.divider()
    p1 = st.toggle("P1", True); p2 = st.toggle("P2", True)
    p3 = st.toggle("P3", True); p4 = st.toggle("P4", True)
    p5 = st.toggle("P5", False); p6 = st.toggle("P6", False)

# --- 4. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1, 2])

with col_in:
    tn = st.text_input("🎯 TARGET", "x.com")
    ru = st.text_input("🔗 ROOT URL", "x.com")
    gh = st.text_input("🐙 GITHUB REPO")
    os_scope = st.text_area("✗ OUT-SCOPE")

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.full_output = "--- INITIALIZING STRIKE ---\n"
        
        env = os.environ.copy()
        env.update({
            "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "OUT_SCOPE": os_scope, "GH_REPO": gh
        })
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        
        with col_term:
            term_placeholder = st.empty()
            process = subprocess.Popen(["bash", SCRIPT_PATH, "strike", ru, tn], 
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                       text=True, env=env, bufsize=1)
            
            for line in iter(process.stdout.readline, ""):
                st.session_state.full_output += line
                term_placeholder.code(st.session_state.full_output, language="bash")
            process.wait()

with col_term:
    st.code(st.session_state.full_output, language="bash")
