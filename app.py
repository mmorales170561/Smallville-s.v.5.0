import streamlit as st
import subprocess
import os
import shutil
import requests
import zipfile
import io

# --- 1. HUD & PATH INJECTION ---
st.set_page_config(page_title="SMALLVILLE V13.3", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .matrix-box { border: 1px solid #333; padding: 15px; text-align: center; background: #111; min-height: 100px; border-radius: 5px; } .terminal-box { background:#000; color:#00ff00; padding:15px; height:400px; overflow:auto; border-left:5px solid #ff3131; font-family: 'Courier New', monospace; font-size: 12px; white-space: pre-wrap; }</style>", unsafe_allow_html=True)

# FORCE PATH REALIGNMENT (Fixes the /home/appuser/.local/bin issue)
LOCAL_BIN = "/home/appuser/.local/bin"
BIN_DIR, LOOT_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

if LOCAL_BIN not in os.environ["PATH"]:
    os.environ["PATH"] = f"{LOCAL_BIN}:{BIN_DIR}:" + os.environ["PATH"]

if 'term_logs' not in st.session_state: st.session_state.term_logs = "ALL-FATHER SYSTEM ONLINE..."

# --- 2. THE STABILIZED FORGE ---
def forge_all_father():
    status = st.status("🛠️ FORGING TOTAL ARSENAL (VERSION LOCKED)...", expanded=True)
    
    # Resolving Dependency Hell: OpenAI < 2.0.0 is mandatory for Mindgard 2026
    commands = [
        "pip install --upgrade pip",
        "pip install 'openai<2.0.0' 'transformers<5.0.0' 'rich<14.0.0' --break-system-packages",
        "pip install mindgard garak snyk-agent-scan promptfoo mythril slither-analyzer --break-system-packages"
    ]
    
    # Binary Tools (Web2 & Web3 Static)
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }

    for cmd in commands:
        subprocess.run(cmd, shell=True, capture_output=True)
        status.write(f"🐍 PIP: {cmd.split(' ')[2].upper()} COMPLETED")

    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=30)
            ext = ".zip" if ".zip" in url else ".tar.xz"
            with open(f"/tmp/t{ext}", "wb") as f: f.write(r.content)
            if ".zip" in url:
                with zipfile.ZipFile(f"/tmp/t{ext}") as z:
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            else:
                subprocess.run(["tar", "-xvf", f"/tmp/t{ext}", "-C", BIN_DIR], capture_output=True)
            os.chmod(os.path.join(BIN_DIR, name), 0o755)
            status.write(f"✅ BIN: {name.upper()} ACTIVE")
        except: status.write(f"❌ BIN: {name.upper()} FAIL")

    status.update(label="SYSTEM REALIGNED & PRIMED", state="complete")
    st.rerun()

# --- 3. SIDEBAR (COMMAND CORE) ---
with st.sidebar:
    st.title("🔴 COMMAND CORE")
    sel_bat = st.selectbox("🎯 ACTIVE BATTERY", ["Web2 Recon", "Web3 Audit", "AI Agent Red-Team"])
    
    if st.button("🔌 PRIME TOTAL SYSTEM", use_container_width=True):
        forge_all_father()
    
    st.divider()
    st.subheader("🛠️ QUICK ACTIONS")
    if st.button("💀 WIPE ALL LOOT"):
        shutil.rmtree(LOOT_DIR); os.makedirs(LOOT_DIR); st.rerun()
    
    st.divider()
    st.info(f"Targeting: {st.session_state.get('target_val', 'NONE')}")

# --- 4. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 13.3")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

tgt = st.session_state.get('target_val', '').strip()

with t1:
    st.subheader(f"DEPLOY: {sel_bat}")
    st.text_input("SET TARGET", key="target_val", placeholder="example.com / 0x... / @model")
    if not tgt: st.info("Waiting for Target Lock...")
    else:
        st.success(f"TARGET LOCKED: {tgt}")
        if st.button("🔥 INITIATE STRIKE"):
            st.session_state.term_logs += f"\n[!] Engaging {sel_bat} on {tgt}..."

with t2:
    st.subheader("📊 ARSENAL INTEGRITY MATRIX")
    matrix = {
        "WEB2 RECON": ["subfinder", "nuclei", "ffuf", "httpx"],
        "WEB3 / CHAIN": ["aderyn", "mythril", "slither"],
        "AI / AGENTS": ["garak", "mindgard", "snyk-agent-scan", "promptfoo", "openai"]
    }
    
    for cat, tools in matrix.items():
        st.markdown(f"#### {cat}")
        cols = st.columns(4)
        for i, name in enumerate(tools):
            ready = shutil.which(name) is not None or os.path.exists(os.path.join(BIN_DIR, name))
            color = "green" if ready else "red"
            cols[i % 4].markdown(f"""<div class="matrix-box"><b style="color:{color};">{name.upper()}</b><br>{'🟢 ONLINE' if ready else '🔴 OFFLINE'}</div>""", unsafe_allow_html=True)
        st.write("")

with t3:
    st.subheader("💰 THE LOOT VAULT")
    files = os.listdir(LOOT_DIR)
    if files:
        sel_file = st.selectbox("Select File", files)
        with open(os.path.join(LOOT_DIR, sel_file), 'r') as f: st.code(f.read())
        
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as z:
            for f in files: z.write(os.path.join(LOOT_DIR, f), f)
        st.download_button("📦 DOWNLOAD ALL (ZIP)", buf.getvalue(), file_name="smallville_loot.zip")
    else: st.info("Loot vault empty.")

with t4:
    st.subheader("⌨️ TERMINAL")
    st.markdown(f'<div class="terminal-box">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(c_in, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {c_in}\n{res.stdout}{res.stderr}"
        st.rerun()

with t5:
    st.subheader("🔍 SYSTEM DEBUG")
    st.write(f"**Path Environment:** `{os.environ['PATH'][:100]}...`")
    st.write(f"**Bin Dir:** `{BIN_DIR}` | **Loot Dir:** `{LOOT_DIR}`")
    if st.button("🔎 LIST ALL BINARIES"):
        st.code("\n".join(os.listdir(BIN_DIR)))
