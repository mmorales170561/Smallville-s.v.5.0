import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v8.5", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. ASENAL MAPPING ---
BATTERIES = {
    "Web2 (Recon)": ["subfinder", "httpx", "katana", "nuclei"],
    "Web3 (Chain)": ["aderyn", "arjun"],
    "AI Agents": ["trufflehog", "sqlmap"]
}

# --- 3. PERSISTENCE ---
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com, target.local"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil, 127.0.0.1"
if 'target' not in st.session_state: st.session_state.target = ""

# --- 4. SIDEBAR (CONTROL CENTER) ---
with st.sidebar:
    st.title("🔴 COMMAND")
    
    # Target Battery Selection
    selected_battery = st.selectbox("🎯 TARGET BATTERY", list(BATTERIES.keys()), key='active_battery')
    
    st.divider()
    
    # Scope Protection Logic
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE (Authorized)", key='in_scope', help="Comma separated domains/IPs")
    st.text_area("🔴 RED ZONE (Forbidden)", key='out_scope', help="Restricted suffixes or IPs")
    
    st.divider()
    
    if st.button("🔌 PRIME OMNI-ARSENAL"):
        # (Prime logic from v8.4 remains here)
        st.toast("Syncing Arsenal...")
        st.rerun()

    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.5")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

# Scope Validation Logic
target = st.session_state.target.strip().lower()
in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]

is_authorized = any(domain in target for domain in in_list) if target else False
is_forbidden = any(domain in target for domain in out_list) if target else False

with t1:
    st.subheader(f"ENGAGEMENT: {selected_battery}")
    st.text_input("SET TARGET", key="target", placeholder="e.g. example.com")
    
    if not target:
        st.info("Waiting for Target Acquisition...")
    elif is
