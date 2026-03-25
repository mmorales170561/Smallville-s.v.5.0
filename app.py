import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="SMALLVILLE T2 V9.5", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

if 'term_logs' not in st.session_state: st.session_state.term_logs = "SYSTEM ONLINE..."

# --- 2. THE FORGE ENGINE ---
def forge_arsenal():
    status = st.status("🛠️ FORGING ARSENAL...", expanded=True)
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }
    repos = {"arjun": "https://github.com/s0md3v/Arjun.git", "sqlmap": "https://github.com/sqlmapproject/sqlmap.git", "trufflehog": "https://github.com/trufflesecurity/trufflehog.git"}
    
    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=25)
            if url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif url.endswith(".tar.xz"):
                t_p = "/tmp/c.tar.xz"
                with open(t_p, "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", t_p, "-C", BIN_DIR], capture_output=True)
                for root, _, files in os.walk(BIN_DIR):
                    if name in files and root != BIN_DIR: shutil.move(os.path.join(root, name), os.path.join(BIN_DIR, name))
            p = os.path.join(BIN_DIR, name); os.chmod(p, 0o755)
            status.write(f"✅ {name.upper()}")
        except: status.write(f"❌ {name.upper()} FAIL")
    
    for name, url in repos.items():
        try:
            tp = os.path.join(BIN_DIR, name)
            if not os.path.exists(tp): subprocess.run(["git", "clone", "--depth", "1", url, tp], check=True)
            status.write(f"✅ {name.upper()} REPO")
        except: status.write(f"❌ {name.upper()} REPO FAIL")
    status.update(label="FORGE COMPLETE", state="complete")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    if st.button("🔌 PRIME OMNI-ARSENAL", use_container_width=True): forge_arsenal()
    if st.button("💀 WIPE WORKSPACE", use_container_width=True):
        shutil.rmtree(BIN_DIR, ignore_errors=True); shutil.rmtree(LOOT_DIR, ignore_errors=True)
        st.rerun()
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', value="example.com")
    st.text_area("🔴 RED ZONE", key='out_scope', value=".gov, .mil")

# --- 4. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 9.5")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

tgt = st.session_state.get('target_val', '').strip().lower()

with t3:
    st.subheader("📋 COLLECTED INTEL")
    loot_files = os.listdir(LOOT_DIR)
    if loot_files:
        col1, col2 = st.columns([3, 1])
        selected_file = col1.selectbox("View Loot", loot_files)
        
        # Zip Logic
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as csv_zip:
            for f in loot_files:
                csv_zip.write(os.path.join(LOOT_DIR, f), f)
        col2.download_button("📦 ZIP ALL", buf.getvalue(), file_name="smallville_loot.zip", mime="application/zip")
        
        with open(os.path.join(LOOT_DIR, selected_file), 'r') as f:
            st.code(f.read())
    else: st.info("No loot found.")

with t4:
    st.subheader("⌨️ TERMINAL & QUICK-START")
    # Quick Commands
    q1, q2, q3 = st.columns(3)
    if q1.button("🔍 PASSIVE RECON (SUBFINDER)"): st.session_state.c_input = f"subfinder -d {tgt} -o {LOOT_DIR}/subs.txt"
    if q2.button("🧪 VULN SCAN (NUCLEI)"): st.session_state.c_input = f"nuclei -u {tgt} -o {LOOT_DIR}/vulns.txt"
    if q3.button("💉 SQL INJECTION (SQLMAP)"): st.session_state.c_input = f"sqlmap -u {tgt} --batch --banner"

    st.markdown(f'<div class="terminal">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        cmd = c_in
        # Path Resolution Logic
        if "subfinder" in c_in and not c_in.startswith("/tmp"): cmd = c_in.replace("subfinder", f"{BIN_DIR}/subfinder")
        if "sqlmap" in c_in and not c_in.startswith("python3"): cmd = f"python3 {BIN_DIR}/sqlmap/sqlmap.py " + c_in.replace("sqlmap", "")
        if "arjun" in c_in: cmd = f"python3 {BIN_DIR}/arjun/arjun.py " + c_in.replace("arjun", "")
        
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {cmd}\n{res.stdout}{res.stderr}"
        st.rerun()

# (Other tabs logic from v9.4 remains)
