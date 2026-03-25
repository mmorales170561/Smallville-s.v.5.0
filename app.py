import streamlit as st
import subprocess
import os
import requests
import zipfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="SMALLVILLE T2 V11.0", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR, WORD_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot", "/tmp/ruby_wordlists"
for d in [BIN_DIR, LOOT_DIR, WORD_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

if 'term_logs' not in st.session_state: st.session_state.term_logs = "CITADEL ONLINE [MARCH 2026]..."

# --- 2. THE 2026 ARSENAL FORGE ---
def forge_citadel():
    status = st.status("🛠️ FORGING CITADEL ARSENAL...", expanded=True)
    
    # 2026 Specialized AI Security Binaries
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
        "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.82.12/trufflehog_3.82.12_linux_amd64.tar.gz",
    }
    
    # Python-based 2026 Red-Teaming Tools
    # Garak is the primary LLM vulnerability scanner (Prompt Injection, Jailbreaks)
    # PentAGI-Light is used for autonomous agent assessment
    pip_tools = ["garak==0.14.0", "snyk-agent-scan", "pentagi-cli"]
    
    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=25)
            ext = ".zip" if ".zip" in url else ".tar.gz"
            with open(f"/tmp/temp{ext}", "wb") as f: f.write(r.content)
            if ".zip" in url:
                with zipfile.ZipFile(f"/tmp/temp{ext}") as z:
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            else:
                subprocess.run(["tar", "-xvf", f"/tmp/temp{ext}", "-C", BIN_DIR], capture_output=True)
            os.chmod(os.path.join(BIN_DIR, name), 0o755)
            status.write(f"✅ {name.upper()}")
        except: status.write(f"❌ {name.upper()} FAIL")

    # Install 2026 AI Guardrail Bypass & Scanning libs
    for tool in pip_tools:
        subprocess.run(["pip", "install", tool], capture_output=True)
        status.write(f"🐍 {tool.split('==')[0].upper()} INSTALLED")

    status.update(label="CITADEL ARSENAL READY", state="complete")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    sel_bat = st.selectbox("🎯 BATTERY", ["Web2 Recon", "AI Agent / LLM Red-Team", "Secret Mining"], key='active_bat')
    if st.button("🔌 PRIME CITADEL", use_container_width=True): forge_citadel()
    st.divider()
    st.subheader("📚 WORDLISTS")
    up_file = st.file_uploader("Upload .txt", type="txt")
    if up_file:
        with open(os.path.join(WORD_DIR, up_file.name), "wb") as f: f.write(up_file.getbuffer())

# --- 4. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 11.0")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

tgt = st.session_state.get('target_val', '').strip()

with t1:
    st.subheader(f"DEPLOY: {sel_bat}")
    st.text_input("SET TARGET (URL / GitHub / Model Endpoint)", key="target_val", placeholder="https://api.agent-target.ai")
    if not tgt: st.info("Waiting for Target...")
    else:
        st.success(f"TARGET LOCKED: {tgt}")
        if sel_bat == "AI Agent / LLM Red-Team":
            st.warning("Focus: Garak Probes (Injection, Jailbreak) & MCP Shadow-Escape Discovery.")
        if st.button("🔥 INITIATE STRIKE"):
            st.status(f"Scanning {tgt} for AI-specific vulnerabilities...")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    tools = ["garak", "trufflehog", "ffuf", "subfinder", "snyk-agent-scan", "pentagi"]
    cols = st.columns(4)
    for i, name in enumerate(tools):
        ready = shutil.which(name) or os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t3:
    st.subheader("💰 THE LOOT VAULT")
    loot_files = os.listdir(LOOT_DIR)
    if loot_files:
        c1, c2 = st.columns([3, 1])
        sel_loot = c1.selectbox("Files", loot_files)
        # Download ZIP
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as l_zip:
            for f in loot_files: l_zip.write(os.path.join(LOOT_DIR, f), f)
        c2.download_button("📦 ZIP ALL", buf.getvalue(), file_name="citadel_loot.zip")
        with open(os.path.join(LOOT_DIR, sel_loot), 'r') as f: st.code(f.read())
    else: st.info("Loot vault is currently empty.")

with t4:
    st.subheader("⌨️ ADVANCED TERMINAL")
    cols = st.columns(4)
    if cols[0].button("🛡️ GARAK SCAN"): st.session_state.c_input = f"python3 -m garak --model_type openai --model_name {tgt} --probes promptinject,dan"
    if cols[1].button("🔗 MCP PROBE"): st.session_state.c_input = f"snyk-agent-scan --mcp-check --url {tgt}"
    if cols[2].button("⚡ REPO SECRETS"): st.session_state.c_input = f"{BIN_DIR}/trufflehog github --repo {tgt}"
    if cols[3].button("🧪 AUTO-PENT"): st.session_state.c_input = f"pentagi scan --target {tgt} --depth 2"

    st.markdown(f'<div class="terminal">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        cmd = c_in
        for b in ["subfinder", "ffuf", "trufflehog"]:
            if b in c_in and not c_in.startswith("/tmp"): cmd = c_in.replace(b, f"{BIN_DIR}/{b}")
        
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {cmd}\n{res.stdout}{res.stderr}"
        st.rerun()

with t5:
    st.subheader("🔍 DEBUG")
    st.write(f"Environment: `Python 3.11+` | Framework: `Citadel v11.0`")
    if st.button("🔎 SYSTEM AUDIT"):
        st.code(subprocess.run(["pip", "list"], capture_output=True, text=True).stdout)
