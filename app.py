import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. SAFE PDF IMPORT ---
PDF_ENABLED = False
try:
    from fpdf import FPDF
    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False

# --- 2. GLOBAL STATE INITIALIZATION ---
INITIAL_STATE = {
    'target': "example.com",
    'last_log': "SYSTEM READY. PDF ENGINE: " + ("READY" if PDF_ENABLED else "OFFLINE"),
    'in_scope': "example.com",
    'out_scope': ".gov, .mil, localhost",
    'battery_type': "Web2"
}

for key, val in INITIAL_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 3. HUD CONFIGURATION ---
st.set_page_config(page_title="RUBY-OPERATOR v4.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 500px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; }
    .stTextArea>div>div>textarea { background-color: #111; color: #00ff00; border: 1px solid #444; font-family: monospace; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 4. CORE UTILITIES ---
def is_authorized(target):
    target = target.lower().strip()
    if not target: return False, "🎯 Awaiting Sector..."
    in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
    out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
    for forbidden in out_list:
        if forbidden in target: return False, f"🛑 FORBIDDEN: {forbidden}"
    for allowed in in_list:
        if allowed in target: return True, "✅ AUTHORIZED"
    return False, "⚠️ OUT OF SCOPE"

def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        if name in files:
            p = os.path.join(root, name)
            os.chmod(p, 0o755)
            return p
    return None

# --- 5. SIDEBAR: OPERATOR CONSOLE ---
with st.sidebar:
    st.title("🔴 OPERATOR")
    
    # Target Environment Selection
    st.session_state.battery_type = st.radio(
        "TARGET ENVIRONMENT", 
        ["Web2", "Web3", "AI Agent"], 
        index=0
    )
    
    st.divider()
    
    # Scope Parameters
    st.subheader("🛡️ RULES OF ENGAGEMENT")
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE (In-Scope)", st.session_state.in_scope, help="Comma separated domains")
    st.session_state.out_scope = st.text_area("🔴 RED ZONE (Out-of-Scope)", st.session_state.out_scope)
    
    st.divider()
    
    # Manual Controls
    if st.button("🔌 PRIME ARMORY"):
        st.info("Fabricating core binaries...")
        # (Download logic here)
        
    if st.button("🗑️ PURGE TERMINAL"):
        st.session_state.last_log = "TERMINAL WIPED."
        st.rerun()
        
    if st.button("💀 BURN INSTANCE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        st.session_state.last_log = "MEMORY WIPED."
        st.rerun()

# --- 6. MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.5")

# Check Authorization before showing the "Fire" button
auth, msg = is_authorized(st.session_state.target)

tabs = st.tabs(["🚀 STRIKE OPS", "📊 ARSENAL MATRIX", "📟 LIVE HUD"])

with tabs[0]:
    st.header(f"🔫 {st.session_state.battery_type.upper()} STRIKE")
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    
    if auth:
        st.success(f"{msg} | Ready to engage.")
        if st.button("🔥 INITIATE FULL AUTO-STRIKE"):
            st.session_state.last_log = f"🚀 [INIT] {st.session_state.battery_type} STRIKE STARTING...\n"
            # (Insert v3.6/3.7 Chained Logic here)
            st.info("Strike running. Monitor Live HUD.")
    else:
        st.error(msg)

with tabs[1]:
    st.header("📋 ARSENAL STATUS")
    # Grid of tools showing Ready/Missing
    st.write("Scan of /tmp/ruby_bin active...")

with tabs[2]:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
    if PDF_ENABLED and len(st.session_state.last_log) > 100:
        st.button("📄 DOWNLOAD PDF REPORT")
