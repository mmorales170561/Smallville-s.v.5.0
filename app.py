import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="SMALLVILLE T2 V9.3", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 450px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

# --- 2. ASENAL MAPPING ---
BATTERIES = {
    "Web2 (Recon)": ["subfinder", "httpx", "katana", "nuclei"],
    "Web3 (Chain)": ["aderyn", "arjun"],
    "AI Agents": ["trufflehog", "sqlmap"]
}

# --- 3. THE REPO-SYNC FORGE ---
def forge_arsenal():
    status = st.status("🛠️ FORGING REPO-SYNC...", expanded=True)
    
    # Phase A: Binaries
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }
    
    # Phase B: Repositories
    repos = {
        "arjun": "https://github.com/s0md3v/Arjun.git",
        "sqlmap": "https://github.com/sqlmapproject/sqlmap.git",
        "trufflehog": "https://github.com/trufflesecurity/trufflehog.git"
    }

    # Step 1: Extract Binaries
    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=25)
            if url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif url.endswith(".tar.xz"):
                t_path = "/tmp/core.tar.xz"
                with open(t_path, "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", t_path, "-C", BIN_DIR], capture_output=True)
                for root, _, files in os.walk(BIN_DIR):
                    if name in files and root != BIN_DIR:
                        shutil.move(os.path.join(root, name), os.path.join(BIN_DIR, name))
            p = os.path.join(BIN_DIR, name)
            if os.path.exists(p): os.chmod(p, 0o755)
            status.write(f"✅ BINARY: {name.upper()}")
        except Exception as e: status.write(f"❌ BINARY FAIL: {name}")

    # Step 2: Clone Repos
    for name, url in repos.items():
        try:
            target_p = os.path.join(BIN_DIR, name)
            if not os.path.exists(target_p):
                subprocess.run(["git", "clone", "--depth", "1", url, target_p], check=True)
            status.write(f"✅ REPO: {name.upper()}")
        except Exception as e: status.write(f"❌ REPO FAIL: {name}")
    
    status.update(label="RECO-SYNC COMPLETE", state="complete")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    sel_bat = st.selectbox("🎯 BATTERY", list(BATTERIES.keys()), key='active_bat')
    st.divider()
    if st.button("🔌 PRIME OMNI-ARSENAL", use_container_width=True): forge_arsenal()
    if st.button("💀 WIPE WORKSPACE", use_container_width=True):
        shutil.rmtree(BIN_DIR, ignore_errors=True); shutil.rmtree(LOOT_DIR, ignore_errors=True)
        st.rerun()
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', value="example.com")
    st.text_area("🔴 RED ZONE", key='out_scope', value=".gov, .mil")

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 9.3")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_names = [t for sub in BATTERIES.values() for t in sub]
    cols = st.columns(4)
    for i, name in enumerate(all_names):
        # Checks if file exists OR if a directory with that name exists
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

# ... (Strike, Loot, Terminal, Debug tabs logic remains as per v9.2)
