import streamlit as st
from datetime import datetime

# --- 1. GLOBAL BOOTLOADER ---
def global_init():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = f"[*] SYSTEM ONLINE | {datetime.now().strftime('%H:%M:%S')}"
    if 'loot_items' not in st.session_state: 
        st.session_state.loot_items = []
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
        res_log = f"\n[{ts}] Status 200 OK - PII LEAK DETECTED"
        st.session_state.term_logs += cmd_log + res_log
        
        # Data structure with Asset Tracking
        st.session_state.loot_items.append({
            "ts": ts,
            "asset": st.session_state.in_scope, # Tracks the specific asset
            "path": target_path,
            "impact": "Unauthenticated PII Access",
            "severity": "P1 CRITICAL"
        })
        st.rerun()

with t2:
    st.header("Loot Cache")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            st.success(f"🔥 {item.get('severity')} | {item.get('asset')} | {item.get('ts')}")
    else:
        st.info("No PII captured. Run a check in the Terminal.")

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        latest = st.session_state.loot_items[-1]
        
        # UPDATED REPORT FORMAT WITH IMPACTED ASSET
        h1_report = f"""
## Summary:
An Insecure Direct Object Reference (IDOR) was identified on `{latest.get('path')}`.

## Impacted asset:
`{latest.get('asset', 'Unknown')}`

## Steps To Reproduce:
1. Log in to the application as **User B** (Attacker) and capture the session cookie.
2. Identify a valid User ID for **User A** (Victim), such as `1005`.
3. Send a GET request to `https://{latest.get('asset')}{latest.get('path')}` using User B's session cookie.
4. Observe that the server responds with a **200 OK** and returns User A's private data.

## Supporting Material/References:
* **Terminal Logs:** Evidence captured at {latest.get('ts')}.
        """
        st.markdown("### 📋 Copy-Paste to HackerOne")
        st.code(h1_report, language="markdown")
    else:
        st.info("No loot found yet. Hit 'RUN IDOR CHECK' in the Terminal to generate a report.")
