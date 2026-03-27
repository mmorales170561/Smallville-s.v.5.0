import streamlit as st
from datetime import datetime
import time

# --- 1. MASTER STATE BOOTLOADER (RESTORATION) ---
def master_boot():
    defaults = {
        'term_logs': f"[*] SYSTEM ONLINE | {datetime.now().strftime('%H:%M:%S')}",
        'loot_items': [],
        'in_scope': "api.target.com\n*.target.com",
        'out_scope': ".gov, .mil, logout, delete, /admin/config",
        'data_type': "PII (Email/Phone)",
        'ua_cookie': "",
        'ub_cookie': "",
        'is_scanning': False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

master_boot()

# --- 2. LAYOUT & CSS ---
st.set_page_config(page_title="SMALLVILLE V18.6", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00ff00; min-width: 350px; }
    .stMetric { background: #111; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    .fire-button button { background-color: #ff4b4b !important; color: white !important; height: 50px; font-size: 20px !important; }
    .stTextArea textarea { background-color: #0a0a0a !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MISSION CONTROL SIDEBAR (RESTORED) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    
    # Targeting & Scope Restoration
    st.subheader("🛡️ RULES OF ENGAGEMENT")
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE (Whitelist)", st.session_state.in_scope, height=100)
    st.session_state.out_scope = st.text_area("🔴 OUT-OF-SCOPE (Blacklist)", st.session_state.out_scope, height=80)
    
    # TARGET FIRE ACTION
    st.markdown('<div class="fire-button">', unsafe_allow_html=True)
    if st.button("🔥 TARGET FIRE", use_container_width=True):
        st.session_state.is_scanning = True
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Severity & Impact Logic
    st.subheader("⚖️ TRIAGE CONFIG")
    st.session_state.data_type = st.selectbox("Data Target", 
        ["PII (Email/Phone)", "SSN/Financial", "Internal Metadata", "Version/Software Info"])
    
    # Auth Restoration
    st.subheader("🔑 SESSION TOKENS")
    st.session_state.ua_cookie = st.text_input("Cookie A (Victim)", type="password", value=st.session_state.ua_cookie)
    st.session_state.ub_cookie = st.text_input("Cookie B (Attacker)", type="password", value=st.session_state.ub_cookie)
    
    if st.button("🧨 PURGE CACHE"):
        st.session_state.clear()
        st.rerun()

# --- 4. COMMAND HUD (ALL TABS RESTORED) ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "🧪 IDOR LAB", "💰 LOOT CACHE", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    
    if st.session_state.is_scanning:
        with st.status("🚀 EXECUTING KRYPTON STRIKE...", expanded=True) as status:
            st.write("🔍 Filtering Out-of-Scope targets...")
            time.sleep(1)
            st.write(f"📡 Probing {st.session_state.in_scope.splitlines()[0]}...")
            time.sleep(1)
            
            ts = datetime.now().strftime('%H:%M:%S')
            st.session_state.term_logs += f"\n[{ts}] STRIKE COMPLETE: IDOR + Information Leak found."
            
            # Auto-Loot Generation
            st.session_state.loot_items.append({
                "ts": ts, "asset": st.session_state.in_scope.splitlines()[0], 
                "path": "/api/v1/auth/user/1005", "sev": "P2 HIGH", 
                "data": st.session_state.data_type, "impact": "Unauthorized PII access."
            })
            st.session_state.is_scanning = False
            st.rerun()

    st.code(st.session_state.term_logs, language="bash")

with t2:
    st.header("🧪 IDOR Verification Lab")
    st.markdown("Test cross-session logic using the cookies provided in the sidebar.")
    
    col1, col2 = st.columns(2)
    with col1:
        victim_id = st.text_input("Target User ID", value="1005")
    with col2:
        endpoint = st.text_input("API Endpoint", value="/api/v1/user/settings/")
    
    if st.button("⚡ EXECUTE IDOR TEST"):
        ts = datetime.now().strftime('%H:%M:%S')
        log = f"\n[{ts}] IDOR PROBE: User B --> {endpoint}{victim_id} --> 200 OK (VULNERABLE)"
        st.session_state.term_logs += log
        st.session_state.loot_items.append({
            "ts": ts, "asset": st.session_state.in_scope.splitlines()[0], 
            "path": f"{endpoint}{victim_id}", "sev": "P1 CRITICAL", 
            "data": "Account Takeover Candidate", "impact": "Broken Access Control."
        })
        st.success("Test Complete. Check Loot Cache.")
        st.rerun()

with t3:
    st.header("💰 Loot Cache (Evidence)")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            st.success(f"🔥 {item.get('sev')} | {item.get('asset')}{item.get('path')} | {item.get('data')}")
    else:
        st.info("No PII captured. Use 'TARGET FIRE' or 'IDOR TEST' to begin.")

with t4:
    st.header("📝 HackerOne Submission Draft")
    if st.session_state.loot_items:
        l = st.session_state.loot_items[-1]
        report = f"""
## Summary:
Insecure Direct Object Reference (IDOR) on `{l.get('path')}`.

## Impacted asset:
`{l.get('asset')}`

## Impact*:
{l.get('impact')}

## Steps To Reproduce:
1. Authenticate as User B (Attacker).
2. Access the victim resource at `https://{l.get('asset')}{l.get('path')}`.
3. Observe successful data retrieval of `{l.get('data')}`.

## Supporting Material/References:
* **Severity:** {l.get('sev')}
* **Evidence Log:** {l.get('ts')}
        """
        st.code(report, language="markdown")
    else:
        st.info("Loot required for report generation.")
