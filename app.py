import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v8.6", layout="wide")
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
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil"

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    sel_bat = st.selectbox("🎯 BATTERY", list(BATTERIES.keys()), key='active_bat')
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope')
    st.text_area("🔴 RED ZONE", key='out_scope')
    if st.button("🔌 PRIME OMNI-ARSENAL"):
        st.toast("Syncing Arsenal...")
        st.rerun()
    if st.button("💀 WIPE WORKSPACE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        os.makedirs(BIN_DIR)
        st.rerun()

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 8.6")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL"])

# --- ROE VALIDATION ENGINE ---
tgt = st.session_state.get('target_val', '').strip().lower()
grn = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
red = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]

# Short-hand logic to prevent SyntaxErrors
auth = any(d in tgt for d in grn) if tgt else False
deny = any(d in tgt for d in red) if tgt else False

with t1:
    st.subheader(f"ENGAGEMENT: {sel_bat}")
    st.text_input("SET TARGET", key="target_val", placeholder="e.g. target.com")
    
    if not tgt:
        st.info("Waiting for Target Acquisition...")
    elif deny:
        st.error("🛑 INTERLOCK: Target is in RED ZONE.")
    elif not auth:
        st.warning("⚠️ UNAUTHORIZED: Target not in GREEN ZONE.")
    else:
        st.success("✅ AUTHORIZED: Scope Verified.")
        st.divider()
        if st.button("🔥 INITIATE FULL STRIKE"):
            st.status(f"Executing {sel_bat} against {tgt}...")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    all_tools = [t for sub in BATTERIES.values() for t in sub]
    cols = st.columns(4)
    for i, name in enumerate(all_tools):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t4:
    cmd_in = st.text_input("CMD >", key="term")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(cmd_in, shell=True, capture_output=True, text=True)
        st.code(res.stdout + res.stderr)
