import streamlit as st
import subprocess
import os
import requests
import zipfile
import shutil
import io

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="SMALLVILLE V13.0 SINGULARITY", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 450px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; } .matrix-box { border: 1px solid #333; padding: 10px; text-align: center; background: #111; min-height: 80px; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR, WORD_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot", "/tmp/ruby_wordlists"
for d in [BIN_DIR, LOOT_DIR, WORD_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

if 'term_logs' not in st.session_state: st.session_state.term_logs = "SINGULARITY ONLINE [MARCH 2026]..."

# --- 2. THE TOTAL ARSENAL FORGE ---
def forge_all():
    status = st.status("🛠️ FORGING MULTI-DOMAIN ARSENAL...", expanded=True)
    
    # Core Binaries (Web2 + Recon)
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
        "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.82.12/trufflehog_3.82.12_linux_amd64.tar.gz",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }
    
    # Python Repos & Libraries (AI + Web2/3)
    pip_tools = ["garak", "mindgard", "snyk-agent-scan", "pentagi-cli", "promptfoo"]
    repos = {
        "sqlmap": "https://github.com/sqlmapproject/sqlmap.git",
        "arjun": "https://github.com/s0md3v/Arjun.git",
        "secretfinder": "https://github.com/m4ll0k/SecretFinder.git"
    }

    # 1. Bins
    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=25)
            ext = ".zip" if ".zip" in url else (".tar.gz" if ".gz" in url else ".tar.xz")
            tmp = f"/tmp/t{ext}"
            with open(tmp, "wb") as f: f.write(r.content)
            if ".zip" in url:
                with zipfile.ZipFile(tmp) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            else:
                subprocess.run(["tar", "-xvf", tmp, "-C", BIN_DIR], capture_output=True)
            if os.path.exists(os.path.join(BIN_DIR, name)):
                os.chmod(os.path.join(BIN_DIR, name), 0o755)
            status.write(f"✅ BIN: {name.upper()}")
        except: status.write(f"❌ BIN: {name.upper()} FAIL")

    # 2. Pip
    for tool in pip_tools:
        subprocess.run(["pip", "install", tool], capture_output=True)
        status.write(f"🐍 PIP: {tool.upper()}")

    # 3. Repos
    for name, url in repos.items():
        tp = os.path.join(BIN_DIR, name)
        if not os.path.exists(tp): subprocess.run(["git", "clone", "--depth", "1", url, tp])
        status.write(f"📂 REPO: {name.upper()}")

    status.update(label="SINGULARITY ARSENAL READY", state="complete")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    # Restored Target Battery Selection
    sel_bat = st.selectbox("🎯 BATTERY", ["Web2 (Recon/Fuzz)", "Web3 (Smart Contracts)", "AI Agent / LLM Red-Team"], key='active_bat')
    if st.button("🔌 PRIME TOTAL SYSTEM", use_container_width=True): forge_all()
    
    st.divider()
    st.subheader("➕ GLOBAL INSTALLER")
    new_tool = st.text_input("Install via PIP/Git")
    if st.button("🚀 DEPLOY TOOL"):
        subprocess.run(["pip", "install", new_tool])
        st.toast(f"Deployed {new_tool}")

# --- 4. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 13.0")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

tgt = st.session_state.get('target_val', '').strip()

with t1:
    st.subheader(f"DEPLOY: {sel_bat}")
    st.text_input("TARGET (URL / Repo / Contract Address / Model)", key="target_val", placeholder="example.com / 0x... / @model")
    if not tgt: st.info("Waiting for Target Lock...")
    else:
        st.success(f"TARGET LOCKED: {tgt}")
        # Battery-specific advice
        if sel_bat == "Web3 (Smart Contracts)": st.warning("Ensure target is a valid contract address or GitHub repo.")
        if st.button("🔥 INITIATE STRIKE"):
            st.session_state.term_logs += f"\n[!] Engaging {sel_bat} on {tgt}..."

with t2:
    st.subheader("📊 ARSENAL INTEGRITY MATRIX")
    matrix_tools = {
        "Web2": ["subfinder", "httpx", "nuclei", "ffuf", "sqlmap", "arjun"],
        "Web3": ["aderyn", "slither", "mythril"],
        "AI/Agents": ["garak", "mindgard", "snyk-agent-scan", "promptfoo"],
        "Secrets": ["trufflehog", "secretfinder"]
    }
    
    for category, tools in matrix_tools.items():
        st.markdown(f"#### {category}")
        cols = st.columns(4)
        for i, name in enumerate(tools):
            ready = shutil.which(name) or os.path.exists(os.path.join(BIN_DIR, name)) or os.path.exists(os.path.join(BIN_DIR, name, f"{name}.py"))
            status_icon = "🟢 ONLINE" if ready else "🔴 OFFLINE"
            cols[i % 4].markdown(f"""<div class="matrix-box"><b>{name.upper()}</b><br>{status_icon}</div>""", unsafe_allow_html=True)
        st.write("")

with t3:
    st.subheader("💰 THE LOOT VAULT")
    loot_files = os.listdir(LOOT_DIR)
    if loot_files:
        c1, c2 = st.columns([3, 1])
        sel_loot = c1.selectbox("Intel Files", loot_files)
        # Download ZIP
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as l_zip:
            for f in loot_files: l_zip.write(os.path.join(LOOT_DIR, f), f)
        c2.download_button("📦 ZIP ALL", buf.getvalue(), file_name="singularity_loot.zip")
        with open(os.path.join(LOOT_DIR, sel_loot), 'r') as f: st.code(f.read())
    else: st.info("Loot vault is currently empty.")

with t4:
    st.subheader("⌨️ ADVANCED TERMINAL")
    cols = st.columns(4)
    if cols[0].button("🔍 RECON"): st.session_state.c_input = f"subfinder -d {tgt}"
    if cols[1].button("🔗 WEB3 AUDIT"): st.session_state.c_input = f"aderyn {tgt}"
    if cols[2].button("🛡️ AI GARAK"): st.session_state.c_input = f"garak --model_name {tgt}"
    if cols[3].button("💉 SQL MAP"): st.session_state.c_input = f"sqlmap -u {tgt} --batch"

    st.markdown(f'<div class="terminal">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        cmd = c_in
        # Auto-path for binaries and python scripts
        for b in ["subfinder", "ffuf", "trufflehog", "nuclei", "httpx", "aderyn"]:
            if b in c_in and not c_in.startswith("/tmp"): cmd = c_in.replace(b, f"{BIN_DIR}/{b}")
        if "sqlmap" in c_in: cmd = f"python3 {BIN_DIR}/sqlmap/sqlmap.py " + c_in.replace("sqlmap", "")
        if "arjun" in c_in: cmd = f"python3 {BIN_DIR}/arjun/arjun.py " + c_in.replace("arjun", "")
        
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {cmd}\n{res.stdout}{res.stderr}"
        st.rerun()

with t5:
    st.subheader("🔍 SYSTEM DEBUG")
    st.write(f"Smallville Framework: `v13.0` | Target Status: `Locked` | Mode: `Overlord`")
    if st.button("🔎 SYSTEM AUDIT"):
        st.code(subprocess.run(["pip", "list"], capture_output=True, text=True).stdout)
