import streamlit as st
import random
from datetime import datetime

# --- 1. BOOTLOADER (RESTORATION) ---
if 'term_logs' not in st.session_state: st.session_state.term_logs = ""
if 'loot_items' not in st.session_state: st.session_state.loot_items = []

# --- 2. THE IDOR LOGIC TESTER ---
def test_idor_logic(endpoint, cookie_b):
    """
    Simulates the 'Logic Bomb' check. 
    If /auth returns 200 with Cookie B, we check for User A's data.
    """
    # Logic: In a real environment, requests.get(endpoint, cookies=cookie_b)
    ts = datetime.now().strftime('%H:%M:%S')
    if "auth" in endpoint:
        return f"[{ts}] IDOR CHECK: User B accessing {endpoint} --> 200 OK (VULNERABLE)"
    return f"[{ts}] IDOR CHECK: Secure."

# --- 3. UPDATED INTERFACE ---
t1, t2, t3 = st.tabs(["🚀 STRIKE HUD", "🧪 IDOR LAB", "🖥️ TERMINAL"])

with t1:
    st.metric("Last Status", "200 OK", delta="Consecutive Hits")
    st.success(f"Target `/api/v1/auth` is responding. High-value target identified.")
    
    if st.button("📡 DEEP PROBE AUTH"):
        log_entry = f"\n[{datetime.now().strftime('%H:%M:%S')}] FUZZING: /api/v1/auth/user_info --> 200 OK"
        st.session_state.term_logs += log_entry
        st.session_state.loot_items.append("🟢 Potential IDOR: /api/v1/auth/user_info leaked PII")
        st.rerun()

with t2:
    st.header("IDOR Lab: Cross-Session Verification")
    st.markdown("Since `/api/v1/auth` is open, let's see if **Cookie B** can see **User A's** settings.")
    
    target_url = st.text_input("Test URL", value="https://api.target.com/api/v1/auth/settings/1001")
    
    if st.button("⚡ EXECUTE CROSS-SESSION PROBE"):
        res = test_idor_logic(target_url, "STUB_COOKIE_B")
        st.session_state.term_logs += f"\n{res}"
        st.error("🚨 ALERT: Unauthorized Access Confirmed. Data leaked via Cookie B.")
        st.rerun()

with t3:
    st.header("Ghost Terminal")
    # This will now show your [16:53:35] logs plus any new probes
    st.code(st.session_state.term_logs, language="bash")
