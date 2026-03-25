import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v8.3", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. OMNI-SYNC ENGINE ---
def prime_omni_arsenal():
    """Handles multi-source tool fabrication with live UI updates."""
    status = st.status("⚔️ Synchronizing Omni-Arsenal...", expanded=True)
    
    # 🎯 Tool Registry
    tools = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }

    for name, url in tools.items():
        try:
            status.write(f"📡 Fetching {name.upper()}...")
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            
            if url.endswith(".zip"):
                z = zipfile.ZipFile(io.BytesIO(r.content))
                for f in z.namelist():
                    if f.endswith(name) and not f.endswith(('.md', '.txt')):
                        with open(os.path.join(BIN_DIR, name), "wb") as b:
                            b.write(z.read(f))
            
            elif url.endswith(".tar.xz"):
                with open("/tmp/temp.tar.xz", "wb") as f: f.write(r.content)
                with tarfile.open("/tmp/temp.tar.xz", "r:xz") as tar:
                    tar.extractall(BIN_DIR)
                    # Move binary if it extracted to a subfolder
                    for root, _, files in os.walk(BIN_DIR):
                        if name in files and root != BIN_DIR:
                            shutil.move(os.path.join(root, name), os.path.join(BIN_DIR, name))

            os.chmod(os.path.join(BIN_DIR, name), 0o755)
            status.write(f"✅ {name.upper()} Primed.")
        except Exception as e:
            status.write(f"❌ {name.upper()} Failed: {str(e)}")
            
    status.update(label="Sync Cycle Complete.", state="complete")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    if st.button("🔌 PRIME OMNI-ARSENAL"):
        prime_omni_arsenal()
        st.rerun()
    
    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 4. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.3")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_names = ["subfinder", "httpx", "katana", "nuclei", "aderyn", "arjun", "trufflehog", "sqlmap"]
    cols = st.columns(4)
    for i, name in enumerate(all_names):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    cmd_in = st.text_input("CMD >", key="term")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd_in, shell=True, capture_output=True, text=True)
        st.code(res.stdout + res.stderr)
