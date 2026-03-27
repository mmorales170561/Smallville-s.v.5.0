import streamlit as st
from datetime import datetime

# --- 1. MASTER BOOTLOADER ---
def master_boot():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = "[*] LOGS RESTORED\n[18:33:14] ALERT: Nuclei detected Exposed .git directory\n[18:34:33] STRIKE COMPLETE: IDOR + Information Leak found."
    if 'loot_items' not in st.session_state:
        # Hard-coding the 18:33 findings so they appear in your tabs immediately
        st.session_state.loot_items = [
            {"ts": "18:33:14", "asset": "api.target.com", "path": "/.git/", "sev": "P1 CRITICAL", "data": "Source Code Exposure", "impact": "Full source code leak via exposed .git directory."},
            {"ts": "18:34:33", "asset": "api.target.com", "path": "/api/v1/auth", "sev": "P2 HIGH", "data": "PII (Email/Phone)", "impact": "Unauthorized access to user profile data."}
        ]
    if 'in_scope' not in st.session_state: st.session_state.in_scope = "api.target.com"
    if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil, logout"

master_boot()

# --- 2. SIDEBAR (RESTORED OPTIONS) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", st.session_state.in_scope)
    st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE", st.session_state.out_scope)
    
    st.divider()
    st.subheader("🔑 SESSION TOKENS")
    ua = st.text_input("Cookie A", type="password")
    ub = st.text_input("Cookie B", type="password")
    
    if st.button("🔥 TARGET FIRE"):
        st.toast("Scanning specialized assets...")

# --- 3. COMMAND HUD ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "🧪 IDOR LAB", "💰 LOOT CACHE", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")

with t2:
    st.header("🧪 IDOR Verification Lab")
    col1, col2 = st.columns(2)
    v_id = col1.text_input("Victim ID", "1005")
    path = col2.text_input("Path", "/api/v1/auth/user/")
    
    if st.button("⚡ EXECUTE IDOR TEST"):
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.term_logs += f"\n[{ts}] IDOR PROBE: {path}{v_id} --> 200 OK"
        st.success("Probe Recorded.")

with t3:
    st.header("💰 Loot Cache")
    for item in st.session_state.loot_items:
        st.success(f"🔥 {item.get('sev')} | {item.get('asset')}{item.get('path')} | {item.get('data')}")

with t4:
    st.header("📝 HackerOne Submission Draft")
    # Selection for which bug to report
    bug_idx = st.selectbox("Select Finding to Draft", range(len(st.session_state.loot_items)), 
                           format_func=lambda x: f"{st.session_state.loot_items[x]['path']} ({st.session_state.loot_items[x]['sev']})")
    
    l = st.session_state.loot_items[bug_idx]
    report = f"""
## Summary:
{l.get('data')} identified on `{l.get('path')}`.

## Impacted asset:
`{l.get('asset')}`

## Impact*:
{l.get('impact')}

## Steps To Reproduce:
1. Navigate to `https://{l.get('asset')}{l.get('path')}`.
2. Observe that the server returns sensitive information (Status 200 OK).
3. [For IDOR]: Use User B's session to access User A's data.

## Supporting Material/References:
* **Severity:** {l.get('sev')}
* **Timestamp:** {l.get('ts')}
    """
    st.code(report, language="markdown")
