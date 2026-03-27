import streamlit as st
from datetime import datetime

# --- 1. MASTER BOOTLOADER (SAFETY FIRST) ---
def master_boot():
    if 'term_logs' not in st.session_state: 
        st.session_state.term_logs = "[*] LOGS RESTORED\n[18:33:14] ALERT: Nuclei detected Exposed .git directory\n[18:34:33] STRIKE COMPLETE: IDOR + Information Leak found."
    if 'loot_items' not in st.session_state:
        st.session_state.loot_items = [
            {"ts": "18:33:14", "asset": "api.target.com", "path": "/.git/", "severity": "P1 CRITICAL", "data": "Source Code Exposure", "impact": "Full source code leak."},
            {"ts": "18:34:33", "asset": "api.target.com", "path": "/api/v1/auth", "severity": "P2 HIGH", "data": "PII (Email/Phone)", "impact": "Unauthorized PII access."}
        ]
    if 'in_scope' not in st.session_state: st.session_state.in_scope = "api.target.com"
    if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil, logout"

master_boot()

# --- 2. SIDEBAR (RESTORED MISSION CONTROL) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE", st.session_state.in_scope, height=80)
    st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE", st.session_state.out_scope, height=60)
    
    st.divider()
    st.subheader("🔑 SESSION TOKENS")
    ua = st.text_input("Cookie A", type="password")
    ub = st.text_input("Cookie B", type="password")
    
    if st.button("🔥 TARGET FIRE", use_container_width=True):
        st.toast("Scan initiated...")

# --- 3. THE HUD (ALL TABS RESTORED) ---
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
        st.session_state.loot_items.append({
            "ts": ts, "asset": st.session_state.in_scope.splitlines()[0], 
            "path": f"{path}{v_id}", "severity": "P2 HIGH", 
            "data": "PII Leak", "impact": "Broken Access Control."
        })
        st.rerun()

with t3:
    st.header("💰 Loot Cache")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            # FIX: Using .get() with fallback to support both 'sev' and 'severity'
            s = item.get('severity') or item.get('sev') or "P3"
            p = item.get('path', 'N/A')
            d = item.get('data', 'Data Leak')
            st.success(f"🔥 {s} | {p} | {d}")
    else:
        st.info("No loot captured yet.")

with t4:
    st.header("📝 HackerOne Submission Draft")
    if st.session_state.loot_items:
        # SAFETY SELECTBOX: No more KeyErrors here
        bug_idx = st.selectbox(
            "Select Finding to Draft", 
            range(len(st.session_state.loot_items)), 
            format_func=lambda x: f"{st.session_state.loot_items[x].get('path')} ({st.session_state.loot_items[x].get('severity') or st.session_state.loot_items[x].get('sev') or 'N/A'})"
        )
        
        l = st.session_state.loot_items[bug_idx]
        report = f"""
## Summary:
{l.get('data', 'Vulnerability')} identified on `{l.get('path')}`.

## Impacted asset:
`{l.get('asset', 'Unknown')}`

## Impact*:
{l.get('impact', 'Unauthorized access to sensitive information.')}

## Steps To Reproduce:
1. Navigate to `https://{l.get('asset')}{l.get('path')}`.
2. Observe 200 OK response with sensitive data.

##
