import streamlit as st
import subprocess
import os
import requests
import zipfile
import shutil
import io

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="SMALLVILLE V13.1", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 450px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; } .matrix-box { border: 1px solid #333; padding: 10px; text-align: center; background: #111; min-height: 80px; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR, WORD_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot", "/tmp/ruby_wordlists"
for d in [BIN_DIR, LOOT_DIR, WORD_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

# Add BIN_DIR to system PATH dynamically for this session
os.environ["PATH"] += os.pathsep + BIN_DIR

if 'term_logs' not in st.session_state: st.session_state.term_logs = "FORGE v13.1 ONLINE..."

# --- 2. THE RECOVERY FORGE ---
def forge_recovery():
    status = st.status("🛠️ RECOVERING ARSENAL...", expanded=True)
    
    # 1. CORE PIP INSTALLS (Force 2026 versions)
    # Using --break-system-packages for managed environments
    pip_tools = ["garak", "mindgard", "snyk-agent-scan", "promptfoo", "mythril", "slither-analyzer"]
    for tool in pip_tools:
        try:
            subprocess.run(["pip", "install", tool, "--break-system-packages"], capture_output=True)
            status.write(f"🐍 PIP: {tool.upper()} INSTALLED")
        except: status.write(f"❌ PIP: {tool.upper()} FAIL")

    # 2. CORE BINARIES (Ensuring extraction logic is solid)
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }

    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=30)
            ext = ".zip" if ".zip" in url else ".tar.xz"
            tmp = f"/tmp/t{ext}"
            with open(tmp, "wb") as f: f.write(r.content)
            
            if ".zip" in url:
                with zipfile.ZipFile(tmp) as z:
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            else:
                subprocess.run(["tar", "-xvf", tmp, "-C", BIN_DIR], capture_output=True)
            
            p = os.path.join(BIN_DIR, name)
            if os.path.exists(p): os.chmod(p, 0o755)
            status.write(f"✅ BIN: {name.upper()} ACTIVE")
        except: status.write(f"❌ BIN: {name.upper()} FAIL")

    status.update(label="RECOVERY COMPLETE", state="complete")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    if st.button("🔌 PRIME RECOVERY SYSTEM", use_container_width=True): forge_recovery()
    st.divider()
    st.subheader("➕ FORCE INSTALL")
    f_tool = st.text_input("Package Name")
    if st.button("🚀 FORCE DEPLOY"):
        subprocess.run(["pip", "install", f_tool, "--break-system-packages"])
        st.rerun()

# --- 4. MAIN HUD ---
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("📊 ARSENAL INTEGRITY MATRIX")
    matrix_tools = {
        "Web2": ["subfinder", "nuclei", "ffuf"],
        "Web3": ["aderyn", "mythril", "slither"],
        "AI/Agents": ["garak", "mindgard", "snyk-agent-scan", "promptfoo"]
    }
    
    for category, tools in matrix_tools.items():
        st.markdown(f"#### {category}")
        cols = st.columns(4)
        for i, name in enumerate(tools):
            # Check binary path, then check if it's in global PATH (shutil.which)
            ready = os.path.exists(os.path.join(BIN_DIR, name)) or shutil.which(name)
            status_icon = "🟢 ONLINE" if ready else "🔴 OFFLINE"
            cols[i % 4].markdown(f"""<div class="matrix-box"><b>{name.upper()}</b><br>{status_icon}</div>""", unsafe_allow_html=True)

with t4:
    st.subheader("⌨️ TERMINAL")
    st.markdown(f'<div class="terminal">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        # Direct execution with system-wide PATH access
        res = subprocess.run(c_in, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {c_in}\n{res.stdout}{res.stderr}"
        st.rerun()

# (Other tabs remain persistent as per v13.0 logic)
