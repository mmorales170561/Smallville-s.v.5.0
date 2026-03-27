import streamlit as st
from datetime import datetime

# --- 1. GLOBAL BOOTLOADER (WITH DATA SANITIZER) ---
def global_init():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = f"[*] SYSTEM ONLINE | BAKERSFIELD HQ | {datetime.now().strftime('%Y-%m-%d')}"
    
    # SANITIZER: If loot_items contains strings instead of dictionaries, clear it to prevent the KeyError
    if 'loot_items' not in st.session_state:
        st.session_state.loot_items = []
    elif len(st.session_state.loot_items) > 0:
        if isinstance(st.session_state.loot_items[0], str):
            st.session_state.loot_items = [] # Purge legacy string data
            
    if 'in_scope' not in st.session_state:
        st.session_state.in_scope = "api.target.com"

global_init()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", value=st.session_state.in_scope, height=80)
    
    st.divider()
    st.subheader("🔑 SESSION TOKENS")
    ua_cookie = st.text_input("Cookie A (Victim)", type="password")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password")
    
    st.divider()
    if st.button("🧨 EMERGENCY PURGE CACHE"):
        st.session_state.clear()
        st.rerun()

# --- 3. THE COMMAND TABS ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 RUN IDOR CHECK", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        target_path = "/api/v1/user/1005"
        
        # Terminal Logging
        cmd_log = f"\n[{ts}] curl -i -H 'Cookie: [REDACTED_B]' https://{st.session_state.in_scope}{target_path}"
        res_log = f"\n[{ts}] HTTP/1.1 200 OK | PII LEAK: {{'email': 'admin@target.com'}}"
        
        st.session_state.term_logs += cmd_log + res_log
        
        # Data structure for the Loot Tab
        st.session_state.loot_items.append({
            "ts": ts,
            "path": target_path,
            "impact": "Unauthenticated PII Access",
            "severity": "P1 CRITICAL"
        })
        st.rerun()

with t2:
    st.header("Loot Cache")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            # Safe access using .get() to prevent further crashes
            sev = item.get('severity', 'UNKNOWN')
            path = item.get('path', 'N/A')
            time_found = item.get('ts', '00:00:00')
            st.success(f"🔥 {sev} | {path} | {time_found}")
    else:
        st.info("No PII captured. Run a check in the Terminal.")

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        latest = st.session_state.loot_items[-1]
        h1_report = f"""
## Summary:
An Insecure Direct Object Reference (IDOR) was identified on `{latest.get('path')}`.

## Steps To Reproduce:
1. Log in as User B (Attacker).
2. Request `https://{st.session_state.in_scope}{latest.get('path')}`.
3. Observe 200 OK with User A's data.

## Supporting Material/References:
* **Terminal Logs:** Evidence captured at {latest.get('ts')}.
        """
        st.code(h1_report, language="markdown")
    else:
        st.info("Capture loot to generate report.")
