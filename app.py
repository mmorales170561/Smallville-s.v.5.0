import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v6.8", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. INITIALIZE THE VAULT (Session State) ---
# This block ensures data persists between clicks
state_defaults = {
    'battery_type': 'Web2',
    'in_scope': 'example.com',
    'out_scope': '.gov, .mil',
    'last_log': 'SYSTEM ONLINE.',
    'target': 'example.com'
}
for key, val in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 3. SIDEBAR (The Command Center) ---
with st.sidebar:
    st.title("🔴 COMMAND")
    
    # Use 'key' to link widgets directly to session_state
    st.radio("ENVIRONMENT", ["Web2", "Web3", "AI Agent"], key='battery_type')
    
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', help="Allowed domains (comma separated)")
    st.text_area("🔴 RED ZONE", key='out_scope', help="Forbidden patterns")

    if st.button("🔌 PRIME ARSENAL"):
        st.session_state.last_log = "CORE INJECTION INITIATED..."
        # Logic for tool fabrication...
        st.rerun()
        
    if st.button("💀 BURN WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 4. TOOL REGISTRY ---
ARSENAL = {
    "Web2": ["subfinder", "httpx", "ffuf", "katana"],
    "Web3": ["aderyn", "arjun"],
    "AI Agent": ["trufflehog", "sqlmap", "commix"]
}

def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 6.8")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

# Check authorization
auth = any(g.strip().lower() in st.session_state.target.lower() for g in st.session_state.in_scope.split(",") if g.strip())
forbidden = any(r.strip().lower() in st.session_state.target.lower() for r in st.session_state.out_scope.split(",") if r.strip())

with t1:
    st.text_input("🎯 TARGET SECTOR", key='target')
    if forbidden: 
        st.error("🛑 INTERLOCK ENGAGED: TARGET IS IN RED ZONE")
    elif auth:
        st.success("✅ AUTHORIZED STRIKE ZONE")
        if st.button("🔥 FIRE"):
            st.session_state.last_log = f"Executing strike on {st.session_state.target}"
    else:
        st.warning("⚠️ OUT OF SCOPE: ADD TARGET TO GREEN ZONE")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    cols = st.columns(3)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.write(f"**{cat}**")
            for t in tools:
                ready = find_exe(t) is not None
                st.write(f"{'✅' if ready else '❌'} {t.upper()}")

with t3:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)

with t4:
    st.subheader("⌨️ MANUAL COMMAND DECK")
    cmd = st.text_input("ENTER OVERRIDE", "")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.code(f"{res.stdout}\n{res.stderr}")
