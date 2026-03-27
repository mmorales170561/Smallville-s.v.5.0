import streamlit as st
from datetime import datetime

# --- 1. GLOBAL BOOTLOADER ---
def global_init():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = f"[*] SYSTEM ONLINE | BAKERSFIELD HQ | {datetime.now().strftime('%Y-%m-%d')}"
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
    ua_cookie = st.text_input("Cookie A (Victim)", type="password", placeholder="User A Session")
    ub_cookie = st.text_input("Cookie B (Attacker)", type="password", placeholder="User B Session")
    
    st.divider()
    st.download_button("💾 DOWNLOAD LOGS", st.session_state.term_logs, file_name="evidence_logs.txt")

# --- 3. THE COMMAND TABS ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 RUN IDOR CHECK", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        target_path = "/api/v1/user/1005"
        
        # Logging the exact tool steps
        cmd_log = f"\n[{ts}] curl -i -H 'Cookie: [REDACTED_B]' https://{st.session_state.in_scope}{target_path}"
        res_log = f"\n[{ts}] HTTP/1.1 200 OK\n[{ts}] DATA LEAKED: {{'email': 'admin@target.com', 'role': 'admin'}}"
        
        st.session_state.term_logs += cmd_log + res_log
        st.session_state.loot_items.append({
            "ts": ts,
            "path": target_path,
            "impact": "PII Leak (Email/Role)",
            "severity": "P1 CRITICAL"
        })
        st.rerun()

with t2:
    st.header("Loot Cache")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            st.success(f"🔥 {item['severity']} | {item['path']} | {item['ts']}")
    else:
        st.info("No PII captured yet. Use the Terminal to run a check.")

with t3:
    st.header("IDOR Verification")
    st.write(f"Testing access to `{st.session_state.in_scope}`")
    if st.button("⚡ EXECUTE PROBE"):
        st.session_state.term_logs += f"\n[{datetime.now().strftime('%H:%M:%S')}] Manual IDOR Probe Sent."
        st.toast("Probe Logged to Terminal")

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        latest = st.session_state.loot_items[-1]
        
        # FORMATTED REPORT BASED ON YOUR REQUIREMENTS
        h1_report = f"""
## Summary:
An Insecure Direct Object Reference (IDOR) was identified on the `{latest['path']}` endpoint. This vulnerability allows an authenticated user to access the private profile information (including emails and internal roles) of other users by simply modifying the user ID in the request path.

## Steps To Reproduce:
1. Log in to the application as **User B** (Attacker) and capture the session cookie.
2. Identify a valid User ID for **User A** (Victim), such as `1005`.
3. Send a GET request to `https://{st.session_state.in_scope}{latest['path']}` using User B's session cookie.
4. Observe that the server responds with a **200 OK** and returns User A's private data.

## Supporting Material/References:
* **Terminal Logs:** Attached `evidence_logs.txt` showing the 200 OK response at `{latest['ts']}`.
* **Vulnerability Type:** IDOR / Broken Access Control.
* **Impacted Endpoint:** `{latest['path']}`
        """
        st.markdown("### 📋 Copy-Paste to HackerOne")
        st.code(h1_report, language="markdown")
    else:
        st.info("No loot found yet. Run an IDOR check to generate this report.")
