import streamlit as st
from datetime import datetime
import random

# --- 1. GLOBAL BOOTLOADER (REDUNDANT CHECKS) ---
def global_init():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = "[*] SYSTEM READY\n[18:11:19] Status 200 OK - PII LEAK DETECTED"
    if 'loot_items' not in st.session_state: 
        # Initializing with the 18:11:19 hit so the tab isn't blank
        st.session_state.loot_items = ["🟢 [CRITICAL] PII Leak detected on /api/v1/auth/1001 (18:11:19)"]
    if 'in_scope' not in st.session_state:
        st.session_state.in_scope = "api.target.com"

global_init()

# --- 2. SIDEBAR (RESTORED & PERSISTENT) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", value=st.session_state.in_scope, height=100)
    
    st.divider()
    st.subheader("🔑 SESSION TOKENS")
    ua_cookie = st.text_input("Cookie A (Victim)", type="password", key="ua")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password", key="ub")
    
    st.divider()
    st.download_button("💾 DOWNLOAD EVIDENCE", st.session_state.term_logs, file_name="h1_evidence.txt")

# --- 3. THE COMMAND TABS ---
t1, t2, t3 = st.tabs(["🖥️ LIVE TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB"])

with t1:
    st.header("Ghost Terminal")
    st.caption("Status: Monitoring for IDOR/Broken Access Control")
    
    # The Terminal window
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 RUN IDOR CHECK", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        # Simulate the tool running
        cmd = f"\n[{ts}] curl -i -H
