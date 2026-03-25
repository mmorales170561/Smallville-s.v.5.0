import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v8.4", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. THE REPO-SYNC ENGINE ---
def prime_omni_arsenal():
    status = st.status("⚔️ Synchronizing Omni-Arsenal...", expanded=True)
    
    # Category A: Binaries (Direct Download)
    binaries = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }

    # Category B: Repositories (Git Clone Required)
    repos = {
        "arjun": "https://github.com/s0md3v/Arjun.git",
        "sqlmap": "https://github.com/sqlmapproject/sqlmap.git",
        "trufflehog": "https://github.com/trufflesecurity/trufflehog.git"
    }

    # Step 1: Process Binaries
    for name, url in binaries.items():
        try:
            status.write(f"📡 Downloading Binary: {name.upper()}")
            r = requests.get(url, timeout=15)
            if url.endswith(".zip"):
                z = zipfile.ZipFile(io.BytesIO(r.content))
                for f in z.namelist():
                    if f.endswith(name) and not f.endswith(('.md', '.txt')):
                        with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif url.endswith(".tar.xz"):
                with open("/tmp/t.tar.xz", "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", "/tmp/t.tar.xz", "-C", BIN_DIR], capture_output=True)
            os.chmod(os.path.join(BIN_DIR, name), 0o755)
            status.write(f"✅ Binary Ready: {name.upper()}")
        except Exception as e: status.write(f"❌ Binary Fail: {name} -> {e}")

    # Step 2: Process Repositories
    for name, url in repos.items():
        try:
            target_path = os.path.join(BIN_DIR, name)
            if not os.path.exists(target_path):
                status.write(f"🧬 Cloning Repo: {name.upper()}")
                subprocess.run(["git", "clone", "--depth", "1", url, target_path], check=True)
            status.write(f"✅ Repo Ready: {name.upper()}")
        except Exception as e: status.write(f"❌ Repo Fail: {name} -> {e}")

    status.update(label="All Systems Primed.", state="complete")

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
st.title("🏹 SMALLVILLE S.V. 8.4")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_names = ["subfinder", "httpx", "katana", "nuclei", "aderyn", "arjun", "trufflehog", "sqlmap"]
    cols = st.columns(4)
    for i, name in enumerate(all_names):
        # Check for binary OR directory
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    st.subheader("⌨️ MANUAL OVERRIDE")
    cmd_in = st.text_input("CMD >", key="term")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd_in, shell=True, capture_output=True, text=True)
        st.code(res.stdout + res.stderr)
