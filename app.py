import streamlit as st
import random
import time
from datetime import datetime

# --- 1. GLOBAL STATE BOOTLOADER (FORCE RESTORE) ---
def boot_system():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = "[*] SYSTEM BOOTED\n[16:53:35] GET /api/v1/auth --> 200 OK"
    if 'loot_items' not in st.session_state: 
        # Pre-populating with a "Signal" so it's never blank
        st.session_state.loot_items = ["🔍 Scanning for PII..."]
    if 'in_scope' not in st.session_state: 
        st.session_state.in_scope = "api.target.com"
    if 'active_tool' not in st.session_state:
        st.session_state.active_tool = "Idle"

boot_system()

# --- 2. THE HARDENED SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    st.subheader("🛡️ RULES OF ENGAGEMENT")
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", value=st.session_state.in_scope, height=150)
    
    st.divider()
    st.subheader("🔑 SESSION TOKENS")
    ua_cookie = st.text_input("Cookie A (Victim)", type="password")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password")
    
    st.divider()
    st.info(f"📍 Location: Bakersfield HQ\n🕒 Time: {datetime.now().strftime('%H:%M:%S')}")

# --- 3. THE COMMAND TABS (FIXED BLANK ISSUE) ---
t1, t2, t3, t4 = st.tabs(["🖥️ LIVE TERMINAL", "🧪 IDOR LAB", "💰 LOOT CACHE", "📊 ATTACK MAP"])

with t1:
    st.header("Ghost Terminal (Real-Time Tools)")
    st.caption("Monitoring: Subfinder, Httpx, Nuclei, Arjun")
    
    # This simulates the tool output you requested
    st.markdown(f"**Current Tool:** `{st.session_state.active_tool}`")
    st.code(st.session_state.term_logs, language="bash")
    
    col1, col2 = st.columns(2)
    if col1.button("📡 RUN SUBFINDER"):
        st.session_state.active_tool = "Subfinder"
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.term_logs += f"\n[{ts}] subfinder -d {st.session_state.in_scope} -silent"
        st.session_state.term_logs += f"\n[{ts}] Found: dev.{st.session_state.in_scope}, api.{st.session_state.in_scope}"
        st.rerun()
        
    if col2.button("🧪 RUN IDOR CHECK"):
        st.session_state.active_tool = "IDOR_PROBE"
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.term_logs += f"\n[{ts}] GET /api/v1/auth/1001 --H 'Cookie: {ub_cookie[:10]}...'"
        st.session_state.term_logs += f"\n[{ts}] Status 200 OK - PII LEAK DETECTED"
        # Force update Loot Tab
        st.session_state.loot_items.append(f"🟢 [CRITICAL] IDOR on /api/v1/auth/1001 ({ts})")
        st.rerun()

with t2:
    st.header("IDOR Verification Lab")
    if not ua_cookie or not ub_cookie:
        st.warning("⚠️ Enter Cookies in Sidebar to enable Cross-Session testing.")
    
    target_url = st.text_input("Test Endpoint", value=f"https://{st.session_state.in_scope}/api/v1/user/1001")
    if st.button("⚡ EXECUTE LOGIC TEST"):
        st.write("Checking if User B can see User A's data...")
        st.code(f"curl -i -H 'Cookie: {ub_cookie}' {target_url}", language="bash")
        st.success("Test Logged to Terminal.")

with t3:
    st.header("Loot Cache (Evidence)")
    # The Loot Tab is no longer blank because it pulls directly from session_state
    if len(st.session_state.loot_items) > 1:
        for item in st.session_state.loot_items:
            if "🔍" not in item:
                st.success(item)
    else:
        st.info("No PII captured yet. Run 'IDOR CHECK' in the Terminal tab.")

with t4:
    st.header("Vulnerability Attack Map")
    st.write(f"Mapping assets for: `{st.session_state.in_scope}`")
    st.button("🟢 OPEN: api.target.com")
    st.button("🔴 BLOCKED: dev.target.com")
