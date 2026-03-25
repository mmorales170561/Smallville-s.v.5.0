import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="SMALLVILLE T2 V9.2", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 450px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

# --- 2. ASENAL ASSETS ---
BATTERIES = {
    "Web2 (Recon)": ["subfinder", "httpx", "katana", "nuclei"],
    "Web3 (Chain)": ["aderyn", "arjun"],
    "AI Agents": ["trufflehog", "sqlmap"]
}

if 'term_logs' not in st.session_state: st.session_state.term_logs = "READY..."

# --- 3. THE FORGE (ADERYN FIX APPLIED) ---
def forge_arsenal():
    status = st.status("🛠️ FORGING...", expanded=True)
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }
    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=25)
            if url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif url.endswith(".tar.xz"):
                # Simplified Extraction Logic
                t_path = "/tmp/core.tar.xz"
                with open(t_path, "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", t_path, "-C", BIN_DIR], capture_output=True)
                # Binary cleanup for Aderyn
                for root, dirs, files in os.walk(BIN_DIR):
                    if name in files and root != BIN_DIR:
                        shutil.move(os.path.join(root, name), os.path.join(BIN_DIR, name))
            
            p = os.path.join(BIN_DIR, name)
            if os.path.exists(p): os.chmod(p, 0o755)
            status.write(f"✅ {name.upper()}")
        except Exception as e: status.write(f"❌ {name}: {e}")
    status.update(label="FORGE COMPLETE", state="complete")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    sel_bat = st.selectbox("🎯 BATTERY", list(BATTERIES.keys()), key='active_bat')
    st.divider()
    if st.button("🔌 PRIME OMNI-ARSENAL", use_container_width=True): forge_arsenal()
    if st.button("💀 WIPE WORKSPACE", use_container_width=True):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        shutil.rmtree(LOOT_DIR, ignore_errors=True)
        st.rerun()
    st.divider()
    st.subheader("🛡️ ROE")
    st.text_area("🟢 GREEN", key='in_scope', value="example.com")
    st.text_area("🔴 RED", key='out_scope', value=".gov, .mil")

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 9.2")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

tgt = st.session_state.get('target_val', '').strip().lower()
grn = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
red = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
auth = any(d in tgt for d in grn) if tgt else False
deny = any(d in tgt for d in red) if tgt else False

with t1:
    st.subheader(f"DEPLOY: {sel_bat}")
    st.text_input("SET TARGET", key="target_val", placeholder="target.com")
    if not tgt: st.info("Ready...")
    elif deny: st.error("🛑 RED ZONE")
    elif not auth: st.warning("⚠️ UNAUTHORIZED")
    else:
        st.success("✅ AUTHORIZED")
        if st.button("🔥 INITIATE"): st.status(f"Striking {tgt}...")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_tools = [t for sub in BATTERIES.values() for t in sub]
    cols = st.columns(4)
    for i, name in enumerate(all_tools):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    st.subheader("⌨️ TERMINAL")
    st.markdown(f'<div class="terminal">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXEC"):
        res = subprocess.run(c_in, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {c_in}\n{res.stdout}{res.stderr}"
        st.rerun()

with t5:
    st.subheader("🔍 DEBUG")
    st.write(f"Bin: `{BIN_DIR}` | Loot: `{LOOT_DIR}`")
    if st.button("🔎 SCAN"):
        files = [os.path.join(r, f) for r, d, f in os.walk(BIN_DIR) for f in f]
        st.code("\n".join(files) if files else "Empty")
