import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v8.8", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. ASENAL MAPPING ---
BATTERIES = {
    "Web2 (Recon)": ["subfinder", "httpx", "katana", "nuclei"],
    "Web3 (Chain)": ["aderyn", "arjun"],
    "AI Agents": ["trufflehog", "sqlmap"]
}

# --- 3. THE FORGE ENGINE (WITH ADERYN BINARY FIX) ---
def forge_arsenal():
    status = st.status("🛠️ FORGING OMNI-ARSENAL...", expanded=True)
    
    # Binary Targets
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }
    
    # Repo Targets
    repos = {
        "arjun": "https://github.com/s0md3v/Arjun.git",
        "sqlmap": "https://github.com/sqlmapproject/sqlmap.git",
        "trufflehog": "https://github.com/trufflesecurity/trufflehog.git"
    }

    for name, url in bins.items():
        try:
            status.write(f"📡 Fetching {name.upper()}...")
            r = requests.get(url, timeout=25)
            if url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif url.endswith(".tar.xz"):
                # Specialized Aderyn Extraction
                with open("/tmp/aderyn.tar.xz", "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", "/tmp/aderyn.tar.xz", "-C", BIN_DIR], capture_output=True)
                # Ensure the aderyn binary is moved to the root of BIN_DIR
                for r_dir, _, files in os.walk(BIN_DIR):
                    if "aderyn" in files and r_dir != BIN_DIR:
                        shutil.move(os.path.join(r_dir, "aderyn"), os.path.join(BIN_DIR, "aderyn"))
            
            p = os.path.join(BIN_DIR, name)
            if os.path.exists(p): os.chmod(p, 0o755)
            status.write(f"✅ {name.upper()} Primed.")
        except Exception as e: status.write(f"❌ {name.upper()} Fail: {e}")

    for name, url in repos.items():
        try:
            p = os.path.join(BIN_DIR, name)
            if not os.path.exists(p):
                subprocess.run(["git", "clone", "--depth", "1", url, p], check=True)
            status.write(f"✅ {name.upper()} Repo Linked.")
        except Exception as e: status.write(f"❌ {name.upper()} Repo Fail: {e}")
    
    status.update(label="FORGE COMPLETE", state="complete")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    sel_bat = st.selectbox("🎯 BATTERY", list(BATTERIES.keys()), key='active_bat')
    st.divider()
    if st.button("🔌 PRIME OMNI-ARSENAL", use_container_width=True):
        forge_arsenal()
    if st.button("💀 WIPE WORKSPACE", use_container_width=True):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', value="example.com")
    st.text_area("🔴 RED ZONE", key='out_scope', value=".gov, .mil")

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.8")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

tgt = st.session_state.get('target_val', '').strip().lower()
grn = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
red = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
auth = any(d in tgt for d in grn) if tgt else False
deny = any(d in tgt for d in red) if tgt else False

with t1:
    st.subheader(f"ENGAGEMENT: {sel_bat}")
    st.text_input("SET TARGET", key="target_val", placeholder="target.com")
    if not tgt: st.info("Waiting for Target...")
    elif deny: st.error("🛑 INTERLOCK: RED ZONE.")
    elif not auth: st.warning("⚠️ UNAUTHORIZED: Not in Green Zone.")
    else:
        st.success("✅ AUTHORIZED.")
        if st.button("🔥 INITIATE FULL STRIKE"):
            st.status(f"Executing {sel_bat} Battery...")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_names = [t for sub in BATTERIES.values() for t in sub]
    cols = st.columns(4)
    for i, name in enumerate(all_names):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")
