import streamlit as st
import subprocess
import os
import requests
import zipfile
import io

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# Ensure the bin directory exists
if not os.path.exists(BIN_PATH):
    os.makedirs(BIN_PATH, exist_ok=True)

# --- 3. KRYPTONIAN STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .stCodeBlock { background-color: #000 !important; border: 1px solid #ff0000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        urls = {
            "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
            "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
            "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
            "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
            "airix": "https://github.com/projectdiscovery/airix/releases/download/v0.0.3/airix_0.0.3_linux_amd64.zip"
        }
        for name, url in urls.items():
            with st.spinner(f"Unlocking {name}..."):
                try:
                    r = requests.get(url)
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    for f in z.namelist():
                        if f.endswith(name):
                            content = z.read(f)
                            with open(os.path.join(BIN_PATH, name), "wb") as binary:
                                binary.write(content)
                            os.chmod(os.path.join(BIN_PATH, name), 0o755) # Force Execute Perms
                    st.success(f"✓ {name} Ready")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True)
    p4 = st.toggle("P4: STRIKE", True)
    p5 = st.toggle("P5: ARCHITECT", False)
    p6 = st.toggle("P6: OLYMPUS", False)
    st.divider()
    stealth = st.toggle("🕵️ STEALTH MODE", False)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1, 2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", "x.com")
    ru = st.text_input("🔗 ROOT URL", "x.com")
    gh = st.text_input("🐙 GITHUB REPO")
    
    is_scope = st.text_area("✓ IN-SCOPE")
    os_scope = st.text_area("✗ OUT-SCOPE")

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.terminal = ">> INITIALIZING STRIKE...\n"
        
        # Prepare Environment
        env = os.environ.copy()
        env.update({
            "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "RUN_STEALTH": "1" if stealth else "0",
            "OUT_SCOPE": os_scope, "GH_REPO": gh
        })
        
        # Force Script Permission
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        
        # Execution with Live Output
        with col_term:
            terminal_placeholder = st.empty()
            full_output = ""
            
            process = subprocess.Popen(
                ["bash", SCRIPT_PATH, "strike", ru, tn],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1
            )
            
            for line in iter(process.stdout.readline, ""):
                full_output += line
                terminal_placeholder.code(full_output, language="bash")
            
            process.wait()

with col_term:
    if 'full_output' not in locals():
        st.info("Awaiting Target Selection...")
