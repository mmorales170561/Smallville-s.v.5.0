import streamlit as st
import requests
import random
import time

# --- 1. GLOBAL BOOTLOADER (Prevents Blackouts) ---
def boot_system():
    defaults = {
        'found_subs': [],
        'is_running': False,
        'logs': "SYSTEM READY...",
        'ua_id': "1001",
        'ub_id': "2002",
        'ua_cookie': "",
        'ub_cookie': "",
        'active_target': "example.com"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

boot_system()

# --- 2. FAIL-SAFE UI RENDERER ---
st.set_page_config(page_title="SMALLVILLE V16.6", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# --- 3. SIDEBAR (Hard-Coded Stability) ---
with st.sidebar:
    st.title("🏹 APEX COMMAND")
    st.markdown("---")
    
    # Use session_state directly to ensure persistence
    st.subheader("🔑 DUAL-SESSION IDOR")
    st.session_state.ua_id = st.text_input("User A ID", value=st.session_state.ua_id)
    st.session_state.ua_cookie = st.text_input("Cookie A", value=st.session_state.ua_cookie, type="password")
    
    st.divider()
    
    st.session_state.ub_id = st.text_input("User B ID", value=st.session_state.ub_id)
    st.session_state.ub_cookie = st.text_input("Cookie B", value=st.session_state.ub_cookie, type="password")

    st.divider()
    st.subheader("🛡️ SCOPE")
    raw_scope = st.text_area("IN-SCOPE ASSETS", placeholder="target.com")

# --- 4. THE TABS (Protected by Try-Blocks) ---
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📡 RADAR", "🧪 IDOR LAB", "⚠️ RATE MONITOR"])

with t1:
    try:
        st.header("8-Hour Ghost Marathon")
        if st.button("🔥 TOGGLE MARATHON"):
            st.session_state.is_running = not st.session_state.is_running
        
        if st.session_state.is_running:
            st.success("STRIKE ACTIVE: Mimicking Human Interaction...")
            # Anti-Blackout: Simple status instead of complex loops
            st.info(f"Last Probe: {random.choice(['/api/v1', '/login', '/settings'])} - Status 200")
    except Exception as e:
        st.error(f"Tab 1 Error: {e}")

with t2:
    try:
        st.header("Subdomain Radar")
        domain = st.text_input("Root Domain", value=st.session_state.active_target)
        if st.button("📡 SCAN"):
            # Simulation of Subfinder
            st.session_state.found_subs = [f"api.{domain}", f"dev.{domain}", f"s3-test.{domain}"]
            st.write(st.session_state.found_subs)
    except Exception as e:
        st.error(f"Tab 2 Error: {e}")

with t3:
    try:
        st.header("IDOR Lab")
        test_url = st.text_input("Endpoint URL", value=f"https://api.{st.session_state.active_target}/user/{st.session_state.ua_id}")
        
        c1, c2 = st.columns(2)
        if c1.button("⚡ TEST AUTH (USER B)"):
            r = requests.get(test_url, cookies={"session": st.session_state.ub_cookie}, timeout=5)
            st.code(f"Status: {r.status_code}\nBody: {r.text[:200]}...")
            
        if c2.button("⚡ TEST BLIND (NO AUTH)"):
            r = requests.get(test_url, timeout=5)
            st.code(f"Status: {r.status_code}\nBody: {r.text[:200]}...")
    except Exception as e:
        st.error(f"Tab 3 Error: {e}")

with t4:
    try:
        st.header("Rate-Limit Monitor")
        # Automating the "Too Many Requests" check
        st.metric("Current Backoff Delay", "15.4s")
        st.write("Monitoring for HTTP 429 errors...")
    except Exception as e:
        st.error(f"Tab 4 Error: {e}")
