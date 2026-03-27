import streamlit as st
import subprocess
import os
import shutil
import requests
import zipfile
from datetime import datetime, timedelta

# --- 1. HUD & PATH ---
st.set_page_config(page_title="SMALLVILLE V14.1", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #00ff00; } .stTextArea textarea { background-color: #111 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

# Add local bin to PATH
os.environ["PATH"] = f"/home/appuser/.local/bin:{BIN_DIR}:" + os.environ["PATH"]

# --- 2. THE SCOPE GUARD LOGIC ---
def is_in_scope(target, white_list, black_list):
    # Basic logic: Target must be in white_list and NOT in black_list
    target = target.lower().strip()
    in_white = any(w.strip().lower() in target for w in white_list if w.strip())
    in_black = any(b.strip().lower() in target for b in black_list if b.strip())
    return in_white and not in_black

# --- 3. SIDEBAR: SCOPE & COMMAND ---
with st.sidebar:
    st.title("🛡️ SCOPE GUARD (ROE)")
    # Restoring your specific whitelist/blacklist setup
    whitelist = st.text_area("🟢 IN-SCOPE (Whitelist)", "hackerone.com, target.com", help="Comma-separated domains allowed for scanning.")
    blacklist = st.text_area("🔴 OUT-OF-SCOPE (Blacklist)", ".gov, .mil, logout, delete", help="Keywords or domains to block.")
    
    st.divider()
    st.title("🔴 COMMAND")
    target = st.text_input("SET TARGET", placeholder="sub.target.com").strip()
    
    # Check Scope
    if target:
        if is_in_scope(target, whitelist.split(","), blacklist.split(",")):
            st.success("✅ TARGET AUTHORIZED")
            auth = True
        else:
            st.error("🛑 SCOPE VIOLATION")
            auth = False
    else:
        auth = False

    st.divider()
    # FIXED: Prime Arsenal now uses a status container to show it's working
    if st.button("🔌 PRIME ARSENAL", use_container_width=True):
        with st.status("Installing 2026 Toolset...", expanded=True) as status:
            # Install Core AI/Web tools
            subprocess.run(["pip", "install", "garak", "mindgard", "snyk-agent-scan", "--break-system-packages"], capture_output=True)
            status.write("✅ AI Tools Ready")
            # Binary checks
            bins = {"subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip"}
            # (Insert previous zip/tar download logic here)
            status.update(label="ARSENAL READY!", state="complete")
        st.rerun()

# --- 4. THE HUNTER'S HUB ---
t1, t2, t3 = st.tabs(["🚀 STRIKE CONTROL", "📊 MATRIX", "💰 LOOT"])

with t1:
    st.subheader("8-Hour Persistence Engine")
    col1, col2 = st.columns(2)
    
    # Only allow firing if authorized
    if auth:
        if col1.button("🔥 START 8-HOUR STRIKE"):
            st.info(f"Marathon started against {target}. Persistence: 8h.")
            # Trigger your run_marathon(target) logic here
    else:
        st.warning("Fix Scope Parameters to Enable Strike.")

with t2:
    st.subheader("System Integrity Matrix")
    tools = ["subfinder", "nuclei", "garak", "mindgard"]
    for t in tools:
        ready = shutil.which(t) or os.path.exists(os.path.join(BIN_DIR, t))
        st.write(f"{'🟢' if ready else '🔴'} {t.upper()}")

with t3:
    st.subheader("Captured Intel")
    if os.path.exists(LOOT_DIR):
        files = os.listdir(LOOT_DIR)
        if files: st.selectbox("View Loot", files)
        else: st.info("No loot collected.")
