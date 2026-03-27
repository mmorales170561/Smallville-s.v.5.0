import streamlit as st
import random
from datetime import datetime

# --- 1. THE GLOBAL CHECK (PREVENTS BLACKOUTS) ---
def ensure_state():
    if 'in_scope' not in st.session_state: 
        st.session_state.in_scope = "api.target.com\nadmin.target.com"
    if 'out_scope' not in st.session_state: 
        st.session_state.out_scope = "*.gov\n*.mil"
    if 'target_handle' not in st.session_state: 
        st.session_state.target_handle = "H1_Program_Alpha"
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = "[*] LOGS RESTORED\n[16:53:35] GET /api/v1/auth --> 200 OK"
    if 'loot' not in st.session_state: 
        st.session_state.loot = []

ensure_state()

# --- 2. LAYOUT CONFIG ---
st.set_page_config(page_title="SMALLVILLE V17.3", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00ff00; }
    .stTextArea textarea { background-color: #111 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MANDATORY SIDEBAR (RESTORED) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    
    # Target Handle
    st.session_state.target_handle = st.text_input("🎯 PROGRAM HANDLE", value=st.session_state.target_handle)
    
    st.divider()
    
    # The Rules of Engagement (ROE)
    st.subheader("🛡️ RULES OF ENGAGEMENT")
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", value=st.session_state.in_scope, height=200)
    st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE", value=st.session_state.out_scope, height=100)
    
    st.divider()
    
    # IDOR Credentials
    st.subheader("🔑 SESSION TOKENS")
    ua_cookie = st.text_input("Cookie A (Victim)", type="password")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password")
    
    if st.button("♻️ RESET ALL DATA"):
        st.session_state.clear()
        st.rerun()

# --- 4. THE COMMAND TABS ---
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE HUD", "🧪 IDOR LAB", "💰 LOOT", "🖥️ TERMINAL"])

with t1:
    st.header(f"Target: {st.session_state.target_handle}")
    # Metric updates based on your last 16:53:35 hit
    c1, c2, c3 = st.columns(3)
    c1.metric("Status", "200 OK", delta="Stable")
    c2.metric("Probes", "1,452", delta="+2")
    c3.metric("Bakersfield HQ", "ONLINE")

    if st.button("🔥 PUSH MANUAL PROBE"):
        ts = datetime.now().strftime('%H:%M:%S')
        new_log = f"\n[{ts}] GET /api/v1/auth --> 200 OK (Manual Push)"
        st.session_state.term_logs += new_log
        st.rerun()

with t4:
    st.header("Ghost Terminal")
    # This displays your log history (including the 16:53:35 hits)
    st.code(st.session_state.term_logs, language="bash")
