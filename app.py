import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. ERADICATOR THEME (Red & Black HUD) ---
st.set_page_config(page_title="Smallville: Eradicator", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 2px solid #ff0000; }
    .stButton>button { background-color: #ff0000; color: #ffffff; border-radius: 2px; font-weight: bold; border: none; text-transform: uppercase; }
    .stButton>button:hover { background-color: #cc0000; color: #ffffff; box-shadow: 0 0 10px #ff0000; }
    .stHeader { color: #ff0000; font-family: 'Share Tech Mono', monospace; text-shadow: 2px 2px #330000; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #111111; border: 1px solid #ff0000; color: #ffffff; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ff0000 !important; color: #ffffff !important; font-weight: bold; }
    code { color: #ff0000 !important; background-color: #111111 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIG & STATE ---
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# Force-initialize all keys to prevent tab-loss
for key in ["logs", "findings", "terminal_out", "p_recon", "p_js", "p_strike", "p_sto", "p_ai", "p_cloud", "p_oob", "p_visual"]:
    if key not in st.session_state:
        if key.startswith("p_"): st.session_state[key] = True
        elif key == "findings": st.session_state[key] = []
        else: st.session_state[key] = ">> KRYPTONIAN SYSTEM ONLINE."

# --- 3. SIDEBAR: HOUSE OF EL ---
with st.sidebar:
    st.header("🛡️ HOUSE OF EL")
    st.subheader("Bakersfield Tactical Node")
    
    if st.button("🚀 PRIME KRYPTONIAN ARMORY", use_container_width=True, key="side_prime"):
        # (prime_armory function call here)
        st.success("SOLAR CELLS CHARGED. BINARIES SYNCED.")
    
    st.divider()
    st.subheader("🧬 ABILITY TOGGLES")
    st.session_state.p_recon = st.toggle("🛰️ X-RAY VISION (Recon)", value=st.session_state.p_recon, key="t1")
    st.session_state.p_js = st.toggle("🧠 SUPER-HEARING (JS/Secrets)", value=st.session_state.p_js, key="t2")
    st.session_state.p_strike = st.toggle("🔥 HEAT VISION (Nuclei)", value=st.session_state.p_strike, key="t3")
    st.session_state.p_ai = st.toggle("🤖 PHANTOM ZONE (AI Probes)", value=st.session_state.p_ai, key="t5")
    st.session_state.p_cloud = st.toggle("💎 KRYPTONITE (Web3/RPC)", value=st.session_state.p_cloud, key="t6")
    st.session_state.p_oob = st.toggle("📡 TELEPATHY (Blind OOB)", value=st.session_state.p_oob, key="t7")
    
    st.divider()
    if st.button("🧹 PURGE FORTRESS", use_container_width=True, key="side_purge"):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.rerun()

# --- 4. THE MULTIVERSE TABS ---
tabs = st.tabs(["🚀 STRIKE OPS", "📊 INTELLIGENCE", "🧪 PAYLOAD LAB", "⚡ TACTICAL SHELL", "🖼️ VISUAL RECON"])

with tabs[0]: # STRIKE OPS
    st.subheader("🎯 MISSION PARAMETERS")
    col1, col2 = st.columns(2)
    with col1:
        target_url = st.text_input("🔗 TARGET SECTOR", "syfe.com", key="target_in")
        h1_user = st.text_input("🆔 OPERATOR CODE", placeholder="Krypton-01", key="h1_in")
    with col2:
        out_scope = st.text_area("✗ NO-GO ZONE", "api.syfe.com", height=68, key="scope_in")

    if st.button("🔥 INITIATE FULL SPECTRUM STRIKE", type="primary", use_container_width=True, key="strike_btn"):
        st.info("BREACHING TARGET DEFENSES...")

with tabs[3]: # TACTICAL SHELL
    st.subheader("⚡ DIRECT INTERFACE")
    st.code(st.session_state.terminal_out, language="bash")
