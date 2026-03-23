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

# --- 4. THE MULTIVERSE TABS (CORE WORKSPACE) ---
tabs = st.tabs(["🚀 STRIKE OPS", "📊 INTELLIGENCE", "🧪 PAYLOAD LAB", "⚡ TACTICAL SHELL", "🖼️ VISUAL RECON"])

with tabs[0]: # MISSION CONTROL: MULTI-VECTOR
    # Domain-Specific Battlefields
    v_tabs = st.tabs(["🌐 WEB2 (Standard)", "💎 WEB3 (Blockchain)", "🤖 AI AGENTS (LLM)"])

    with v_tabs[0]: # WEB2 SECTION (RESTRUCTURED)
        st.header("🎯 WEB2 MISSION PARAMETERS")
        col_w2a, col_w2b = st.columns(2)
        with col_w2a:
            w2_name = st.text_input("📝 TARGET NAME", "Bose Corp", key="w2_name")
            w2_url = st.text_input("🔗 TARGET URL", "bose.com", key="w2_url")
        with col_w2b:
            w2_in = st.text_area("✓ IN-SCOPE", "*.bose.com", height=68, key="w2_in_scope")
            w2_out = st.text_area("✗ OUT-SCOPE", "dev-api.bose.com", height=68, key="w2_out_scope")
        
        if st.button("🔥 INITIATE WEB2 STRIKE", type="primary", use_container_width=True, key="w2_btn"):
            st.info(f"X-Ray Vision engaged on {w2_name} sector...")

    with v_tabs[1]: # WEB3 SECTION
        st.header("🎯 WEB3 MISSION PARAMETERS")
        col_w3a, col_w3b = st.columns(2)
        with col_w3a:
            w3_name = st.text_input("📝 PROJECT NAME", "Syfe Finance", key="w3_name")
            w3_frontend = st.text_input("🔗 FRONTEND URL", "app.syfe.com", key="w3_url")
        with col_w3b:
            w3_rpc = st.text_input("⛓️ RPC / NODE URL", "https://eth-mainnet.g.alchemy.com/v2/...", key="w3_rpc")
            w3_contract = st.text_input("📜 CONTRACT ADDR", "0x...", key="w3_contract")
        
        if st.button("🔥 INITIATE KRYPTONITE STRIKE", type="primary", use_container_width=True, key="w3_btn"):
            st.info(f"Probing Web3 Finality for {w3_name}...")

    with v_tabs[2]: # AI SECTION
        st.header("🎯 AI MISSION PARAMETERS")
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            ai_name = st.text_input("📝 AGENT NAME", "Support-Bot-v2", key="ai_name")
            ai_endpoint = st.text_input("🔗 API ENDPOINT", "https://api.target.com/v1/chat", key="ai_url")
        with col_ai2:
            ai_model = st.selectbox("🤖 MODEL ARCH", ["GPT-4o", "Claude-3.5", "Gemini-1.5", "Custom LLM"], key="ai_type")
            ai_prompt = st.text_area("📜 SYSTEM PROMPT (If Known)", "You are a helpful assistant...", height=68, key="ai_sys")
        
        if st.button("🔥 INITIATE PHANTOM ZONE PROBE", type="primary", use_container_width=True, key="ai_btn"):
            st.info(f"Neural Probe launched against {ai_name}...")

# (Tabs 1-4 continue below with Intelligence, Shell, and Visual Recon)
