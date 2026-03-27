import streamlit as st
from datetime import datetime
import random

# --- 1. GLOBAL BOOTLOADER ---
def global_init():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = "[*] SYSTEM READY\n[11:12:50] Terminal Initialized."
    if 'loot_items' not in st.session_state: 
        st.session_state.loot_items = []
    if 'in_scope' not in st.session_state:
        st.session_state.in_scope = "api.target.com"

global_init()

# --- 2. SIDEBAR (STABLE RENDER) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", value=st.session_state.in_scope, height=100)
    
    st.divider()
    st.subheader("🔑 SESSION TOKENS")
    ua_cookie = st.text_input("Cookie A (Victim)", type="password")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password")
    
    st.divider()
    st.download_button("💾 DOWNLOAD EVIDENCE", st.session_state.term_logs, file_name="h1_evidence.txt")

# --- 3. THE COMMAND TABS ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 RUN IDOR CHECK", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        # FIXED SYNTAX: Properly terminated f-string
        cmd_log = f"\n[{ts}] curl -i -H 'Cookie: {ub_cookie[:10]}...' https://{st.session_state.in_scope}/api/v1/user/1005"
        res_log = f"\n[{ts}] Status 200 OK - PII LEAK DETECTED (email: admin@target.com)"
        
        st.session_state.term_logs += cmd_log + res_log
        st.session_state.loot_items.append(f"🔥 [P1 CRITICAL] IDOR on /user/1005 at {ts}")
        st.rerun()

with t2:
    st.header("Loot Cache (H1 Evidence)")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            st.success(item)
    else:
        st.info("No PII captured yet. Run 'IDOR CHECK' in the Terminal tab.")

with t3:
    st.header("IDOR Verification Lab")
    target_id = st.text_input("Victim User ID", value="1005")
    if st.button("⚡ EXECUTE MANUAL PROBE"):
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.term_logs += f"\n[{ts}] Manual IDOR Probe on {target_id} --> 200 OK"
        st.success(f"Probe sent to Terminal at {ts}")

with t4:
    st.header("HackerOne Report Template")
    if st.session_state.loot_items:
        latest_loot = st.session_state.loot_items[-1]
        report_template = f"""
### Summary:
Insecure Direct Object Reference (IDOR) identified on `{st.session_state.in_scope}`.

### Vulnerability Details:
The endpoint `/api/v1/user/[ID]` does not properly validate session ownership. 
An attacker (User B) can access the private data of User A by modifying the ID parameter.

### Evidence (from Loot Cache):
- {latest_loot}
- Response: 200 OK (Contains PII)

### Impact:
Unauthorized access to sensitive user data, including emails and system metadata.
        """
        st.markdown("Copy the Markdown below for your H1 submission:")
        st.code(report_template, language="markdown")
    else:
        st.info("Capture loot first to generate a report draft.")
