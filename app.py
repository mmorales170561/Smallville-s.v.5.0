import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. STARK HUD STYLING (The JARVIS Theme) ---
st.set_page_config(page_title="JARVIS: Stark Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00d4ff; }
    [data-testid="stSidebar"] { background-color: #1a1c23; border-right: 2px solid #ffcc00; }
    .stButton>button { background-color: #ffcc00; color: #000; border-radius: 5px; font-weight: bold; border: 1px solid #ffcc00; }
    .stButton>button:hover { background-color: #00d4ff; color: #000; border: 1px solid #00d4ff; }
    .stHeader { color: #ffcc00; font-family: 'Courier New', Courier, monospace; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #1a1c23; border: 1px solid #333; color: #00d4ff; border-radius: 5px 5px 0 0; }
    .stTabs [aria-selected="true"] { background-color: #ffcc00 !important; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIG & STATE ---
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

for key in ["logs", "findings", "terminal_out", "p_recon", "p_js", "p_strike", "p_sto", "p_ai", "p_cloud", "p_oob", "p_visual"]:
    if key not in st.session_state:
        if key.startswith("p_"): st.session_state[key] = True
        elif key == "findings": st.session_state[key] = []
        else: st.session_state[key] = ">> JARVIS ONLINE. STANDING BY."

# --- 3. SIDEBAR: STARK SYSTEMS ---
with st.sidebar:
    st.header("⚡ STARK SYSTEMS")
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a3/Stark_Industries_logo.png", width=200)
    
    if st.button("🚀 ARMOR UP (Install Tools)", use_container_width=True, key="side_prime"):
        # prime_armory() logic here
        st.success("MARK-LXXXV SYSTEMS ARMED.")
    
    st.divider()
    st.subheader("🛠️ HUD OVERLAY")
    st.session_state.p_recon = st.toggle("🛰️ SATELLITE RECON (P1-2)", value=st.session_state.p_recon, key="t1")
    st.session_state.p_js = st.toggle("🕵️‍♂️ ANALYSIS (P3/JS)", value=st.session_state.p_js, key="t2")
    st.session_state.p_strike = st.toggle("🔥 REPULSOR BLAST (P4)", value=st.session_state.p_strike, key="t3")
    st.session_state.p_ai = st.toggle("🧠 NEURAL PROBE (AI)", value=st.session_state.p_ai, key="t5")
    st.session_state.p_cloud = st.toggle("💎 ARC REACTOR (Web3)", value=st.session_state.p_cloud, key="t6")
    st.session_state.p_oob = st.toggle("📡 BLIND SENSORS (OOB)", value=st.session_state.p_oob, key="t7")
    
    st.divider()
    if st.button("🧹 SELF-DESTRUCT (Purge)", use_container_width=True, key="side_purge"):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.rerun()

# --- 4. HUD TABS (The Workspace) ---
tabs = st.tabs(["🚀 STRIKE OPS", "📊 INTEL ANALYSIS", "🧪 ADVERSARIAL LAB", "⚡ J.A.R.V.I.S. TERMINAL", "🖼️ VISUAL HUD"])

with tabs[0]: # STRIKE OPS
    st.subheader("🎯 MISSION CONFIGURATION")
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("🔗 TARGET VECTOR", "stark.com", key="target_in")
        h1_user = st.text_input("🆔 OPERATOR ID", placeholder="Stark-001", key="h1_in")
    with col2:
        out_scope = st.text_area("✗ NO-FLY ZONE", "api.stark.com", height=68, key="scope_in")

    if st.button("💥 INITIATE HOUSE PARTY PROTOCOL", type="primary", use_container_width=True, key="strike_btn"):
        st.info("ENGAGING ADVERSARY...")

with tabs[3]: # TERMINAL
    st.subheader("⚡ J.A.R.V.I.S. CORE COMMAND")
    st.code(st.session_state.terminal_out, language="bash")
