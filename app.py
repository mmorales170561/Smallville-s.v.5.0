import streamlit as st
import subprocess
import os
import requests
import zipfile
import shutil
import time

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 300px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. PERSISTENCE LAYER ---
if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM V7.0 ONLINE."
if 'target' not in st.session_state: st.session_state.target = ""
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

# --- 3. THE ARMORY ---
TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
    "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip"
}

def log_event(msg):
    st.session_state.last_log += f"\n[>] {msg}"

def prime_armory():
    for name, url in TOOL_URLS.items():
        try:
            r = requests.get(url, timeout=10)
            pkg = f"/tmp/{name}.zip"
            with open(pkg, "wb") as f: f.write(r.content)
            with zipfile.ZipFile(pkg, 'r') as z: z.extractall(BIN_DIR)
            os.chmod(os.path.join(BIN_DIR, name), 0o755)
            log_event(f"SUCCESS: {name} Primed.")
        except Exception as e:
            log_event(f"FAIL: {name} -> {str(e)}")

# --- 4. COMMAND SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        prime_armory()
        st.rerun()
    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.0")
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD"])

# Scope Interlock Logic
is_auth = any(g.strip().lower() in st.session_state.target.lower() for g in st.session_state.in_scope.split(",") if g.strip())
is_forbidden = any(r.strip().lower() in st.session_state.target.lower() for r in st.session_state.out_scope.split(",") if r.strip())

with t1:
    st.subheader("🎯 ENGAGEMENT SECTOR")
    st.text_input("ENTER TARGET", key='target', placeholder="example.com")
    
    if is_forbidden:
        st.error("🛑 INTERLOCK ACTIVE: TARGET IS IN RED ZONE")
    elif is_auth and st.session_state.target:
        st.success("✅ AUTHORIZED: TARGET IN GREEN ZONE")
        if st.button("🔥 EXECUTE FULL CYCLE"):
            with st.status("Executing Strike Cycle...", expanded=True) as s:
                for tool in TOOL_URLS.keys():
                    exe = os.path.join(BIN_DIR, tool)
                    if os.path.exists(exe):
                        s.write(f"Running {tool}...")
                        # Example: subfinder -d target
                        log_event(f"STRIKE: {tool} launched against {st.session_state.target}")
                        time.sleep(1) # Simulating execution
                s.update(label="Strike Cycle Complete.", state="complete")
    else:
        st.warning("⚠️ WAITING FOR AUTHORIZED TARGET")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    for t in TOOL_URLS.keys():
        ready = os.path.exists(os.path.join(BIN_DIR, t))
        st.write(f"{'✅' if ready else '❌'} {t.upper()}")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
