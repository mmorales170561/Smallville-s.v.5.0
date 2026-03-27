import streamlit as st
import random
import time
import re
from datetime import datetime

# --- 1. GLOBAL UI & GHOST SETTINGS ---
st.set_page_config(page_title="SMALLVILLE V16.9", layout="wide")
# The "Ghost Terminal" CSS
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# Define variables globally for all tabs
defaults = {
    'terminal_logs': "[*] TERMINAL INITIALIZED...",
    'found_subs': ["api.target.com", "dev.target.com", "staging.target.com", "s3-backup.target.com"],
    'last_probe': "/api/v1 - Status 200",
    'loot_list': ["🟢 Email: admin@target.com found on /api/v1/users", "🟢 IP: 10.0.0.1 found on /api/v1/config"]
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 2. COMMAND SIDEBAR ---
with st.sidebar:
    st.title("🏹 COMMAND CENTER")
    st.divider()
    # The Bakersfield "Jitter" Control
    st.subheader("👻 JITTER (Human Mimicry)")
    jitter = st.slider("Request Delay (Seconds)", 5, 60, 15)
    st.info(f"Using {jitter}s delay to stay undetectable.")

# --- 3. THE COMMAND CENTER HUD (TABS) ---
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE HUD", "📊 VULNERABILITY MAP", "💰 LOOT CACHE", "🛠️ SYSTEM LOGS"])

with t1:
    st.header("Active Ghost Strike")
    c1, c2, c3 = st.columns(3)
    c1.metric("Probes Sent", "1,240", delta="+1 (Ghost Delay)")
    c2.metric("Last Probe Status", "200 OK", delta="Stable")
    c3.metric("Response Time", "142ms")
    
    st.markdown("---")
    
    # THE TERMINAL EMULATOR
    st.subheader("🖥️ TERMINAL EMULATOR (Live Feed)")
    st.code(st.session_state.terminal_logs, language="bash")
    
    if st.button("🔥 PUSH UPDATE TO TERMINAL"):
        # This simulates the tool working in the background
        new_log = f"\n[{datetime.now().strftime('%H:%M:%S')}] GET /api/v1/users?limit=10 --> 200 OK (Jitter {jitter}s)"
        st.session_state.terminal_logs += new_log
        st.rerun()

with t2:
    st.header("Vulnerability Attack Map")
    st.markdown("Visualizing which assets are 'Open' (Status 200) vs 'Closed' (Status 403).")
    
    # Simulation of the "Open" vs "Closed" assets
    cols = st.columns(len(st.session_state.found_subs))
    for i, sub in enumerate(st.session_state.found_subs):
        status = random.choice([200, 403, 200, 403])
        if status == 200:
            cols[i].success(f"🟢 OPEN\n{sub}")
            cols[i].caption("GET / --> 200 OK")
        else:
            cols[i].error(f"🔴 CLOSED\n{sub}")
            cols[i].caption("GET / --> 403 Forbidden")

with t3:
    st.header("Loot Cache (H1 Evidence)")
    st.info("P1/P2 evidence extracted from Status 200 responses.")
    if st.session_state.loot_list:
        for item in st.session_state.loot_list:
            st.success(item)
    else:
        st.write("Hunting for PII in open API endpoints...")

with t4:
    st.subheader("System Arsenal Health")
    st.write(f"Bakersfield Operation Center: **ONLINE**")
    st.write("Arsenal: Subfinder, Httpx, Arjun, Garak AI [READY]")
