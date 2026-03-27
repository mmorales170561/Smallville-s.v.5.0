import streamlit as st
import random
import re
from datetime import datetime

# --- 1. THE ETERNAL BOOTLOADER ---
def initialize_system():
    # Double-Lock Persistence: Ensures sidebar data never vanishes
    if 'in_scope' not in st.session_state: st.session_state.in_scope = "api.target.com\n*.target.com"
    if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil, logout, delete"
    if 'target_handle' not in st.session_state: st.session_state.target_handle = "security"
    if 'term_logs' not in st.session_state: st.session_state.term_logs = "[*] SYSTEM BOOTED\n[*] READY FOR H1 STRIKE"
    if 'loot_items' not in st.session_state: st.session_state.loot_items = []

initialize_system()

# --- 2. GLOBAL STYLES ---
st.set_page_config(page_title="SMALLVILLE V17.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #0a0a0a !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .stMetric { border: 1px solid #333; padding: 10px; border-radius: 5px; background: #111; }
    .terminal-window { background-color: #000; border: 2px solid #333; padding: 10px; color: #0f0; }
    </style>
""", unsafe_allow_html=True)

# --- 3. RESTORED COMMAND SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.markdown("---")
    
    # Target Handle (The Program)
    st.session_state.target_handle = st.text_input("🎯 H1 PROGRAM HANDLE", value=st.session_state.target_handle)
    
    st.divider()
    
    # In-Scope / Out-of-Scope Restoration
    st.subheader("🛡️ RULES OF ENGAGEMENT")
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE (Whitelist)", value=st.session_state.in_scope, height=150)
    st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE (Blacklist)", value=st.session_state.out_scope, height=100)
    
    st.divider()
    
    # IDOR / Session State
    st.subheader("🔑 SESSION TOKENS")
    ua_cookie = st.text_input("Cookie A (Victim)", type="password")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password")

# --- 4. THE COMMAND CENTER HUD ---
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE HUD", "📊 ATTACK MAP", "💰 LOOT TAB", "🖥️ TERMINAL"])

with t1:
    st.header(f"Active Strike: {st.session_state.target_handle}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Probes", "1,402", delta="+1")
    c2.metric("Last Status", "200 OK", delta="Stable")
    c3.metric("Jitter Delay", "15.4s", delta="-0.2s")
    
    if st.button("🔥 EXECUTE GHOST PROBE", use_container_width=True):
        new_log = f"\n[{datetime.now().strftime('%H:%M:%S')}] GET /api/v1/auth --> 200 OK"
        st.session_state.term_logs += new_log
        # Logic: If 200 OK, check for Loot
        if random.random() > 0.7:
            st.session_state.loot_items.append(f"🟢 Found PII on /api/v1/auth (Timestamp: {datetime.now().strftime('%H:%M')})")
        st.rerun()

with t2:
    st.header("Vulnerability Attack Map")
    # Mapping the In-Scope list visually
    scope_list = st.session_state.in_scope.split('\n')
    cols = st.columns(min(len(scope_list), 4))
    for i, asset in enumerate(scope_list[:8]):
        with cols[i % 4]:
            status = random.choice(["🟢 OPEN", "🔴 BLOCKED", "🟢 OPEN"])
            st.button(f"{status}\n{asset}", key=f"map_{i}")

with t3:
    st.header("Loot Cache")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            st.success(item)
    else:
        st.info("No sensitive data captured yet. Continue the Marathon.")

with t4:
    st.header("Ghost Terminal Emulator")
    st.markdown('<div class="terminal-window">', unsafe_allow_html=True)
    st.code(st.session_state.term_logs, language="bash")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Clear Terminal"):
        st.session_state.term_logs = "[*] TERMINAL RESET"
        st.rerun()
