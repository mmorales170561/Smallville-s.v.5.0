import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR ", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. ASENAL REGISTRY ---
BINARIES = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
    "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
}
REPOS = {
    "arjun": "https://github.com/s0md3v/Arjun.git",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap.git",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog.git"
}

# --- 3. THE FORGE ENGINE ---
def forge_arsenal():
    status = st.status("🛠️ FORGING ARSENAL...", expanded=True)
    
    # Process Binaries
    for name, url in BINARIES.items():
        try:
            status.write(f"📥 Fetching {name}...")
            r = requests.get(url, timeout=20)
            if url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif url.endswith(".tar.xz"):
                with open("/tmp/t.tar.xz", "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", "/tmp/t.tar.xz", "-C", BIN_DIR], capture_output=True)
            
            target_path = os.path.join(BIN_DIR, name)
            if os.path.exists(target_path):
                os.chmod(target_path, 0o755)
                status.write(f"✅ {name} Primed.")
        except Exception as e: status.write(f"❌ {name} Error: {e}")

    # Process Repos
    for name, url in REPOS.items():
        try:
            path = os.path.join(BIN_DIR, name)
            if not os.path.exists(path):
                status.write(f"🧬 Cloning {name}...")
                subprocess.run(["git", "clone", "--depth", "1", url, path], check=True)
            status.write(f"✅ {name} Repository Linked.")
        except Exception as e: status.write(f"❌ {name} Clone Error: {e}")
    
    status.update(label="FORGE COMPLETE", state="complete")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    if st.button("🔌 PRIME OMNI-ARSENAL", use_container_width=True):
        forge_arsenal()
    
    if st.button("💀 WIPE WORKSPACE", use_container_width=True):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', value=st.session_state.get('in_scope', 'example.com'))
    st.text_area("🔴 RED ZONE", key='out_scope', value=st.session_state.get('out_scope', '.gov, .mil'))

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.7")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_names = list(BINARIES.keys()) + list(REPOS.keys())
    cols = st.columns(4)
    for i, name in enumerate(all_names):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    cmd = st.text_input("CMD >", key="term_cmd")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.code(res.stdout + res.stderr)
