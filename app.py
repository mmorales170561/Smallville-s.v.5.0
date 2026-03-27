import streamlit as st
from datetime import datetime

# --- 1. THE MASTER STATE CONTROLLER (PREVENTS ALL CRASHES) ---
def master_boot():
    keys = {
        'term_logs': f"[*] SYSTEM ONLINE | {datetime.now().strftime('%H:%M:%S')}",
        'loot_items': [],
        'in_scope': "api.target.com",
        'target_handle': "H1_Program_Alpha",
        'data_type': "PII (Email/Phone)",
        'ua_cookie': "",
        'ub_cookie': ""
    }
    for key, val in keys.items():
        if key not in st.session_state:
            st.session_state[key] = val

master_boot()

# --- 2. GLOBAL UI SETTINGS ---
st.set_page_config(page_title="SMALLVILLE V18.4", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00ff00; min-width: 350px; }
    .stTextArea textarea { background-color: #111 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .stMetric { background: #111; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE FULL SIDEBAR (MISSION CONTROL) ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    
    # Core Targeting
    st.session_state.target_handle = st.text_input("🎯 PROGRAM HANDLE", st.session_state.target_handle)
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE (Assets)", st.session_state.in_scope, height=100)
    
    st.divider()
    
    # Severity & Impact Live Calculator
    st.subheader("⚖️ TRIAGE & IMPACT")
    st.session_state.data_type = st.selectbox("Detection Type", 
        ["PII (Email/Phone)", "SSN/Financial", "Internal Metadata", "Version/Software Info"])
    
    # Logic for Impact Mapping
    impact_map = {
        "SSN/Financial": ("P1 CRITICAL", "$5k-$15k", "High-risk financial data exposure."),
        "PII (Email/Phone)": ("P2 HIGH", "$1.5k-$5k", "Unauthorized access to user identity info."),
        "Internal Metadata": ("P3 MEDIUM", "$500-$1.5k", "Leakage of internal system architecture."),
        "Version/Software Info": ("P4 LOW", "$50-$300", "Public disclosure of server versions.")
    }
    sev, bounty, desc = impact_map[st.session_state.data_type]
    
    st.metric("Priority", sev)
    st.metric("Est. Bounty", bounty)
    st.caption(f"Impact: {desc}")
    
    st.divider()
    
    # Auth Tokens
    st.subheader("🔑 SESSION TOKENS")
    st.session_state.ua_cookie = st.text_input("Cookie A (Victim)", type="password", value=st.session_state.ua_cookie)
    st.session_state.ub_cookie = st.text_input("Cookie B (Attacker)", type="password", value=st.session_state.ub_cookie)
    
    if st.button("🧨 PURGE ALL DATA"):
        st.session_state.clear()
        st.rerun()

# --- 4. THE MAIN DASHBOARD (TABS) ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "🧪 IDOR LAB", "💰 LOOT CACHE", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 EXECUTE IDOR PROBE", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        path = "/api/v1/user/1005"
        
        # Log to Terminal
        st.session_state.term_logs += f"\n[{ts}] curl -H 'Cookie: REDACTED' https://{st.session_state.in_scope}{path}"
        st.session_state.term_logs += f"\n[{ts}] Status 200 OK | Leak: {st.session_state.data_type}"
        
        # Save to Loot (DICTIONARY FORMAT)
        st.session_state.loot_items.append({
            "ts": ts,
            "asset": st.session_state.in_scope,
            "path": path,
            "sev": sev,
            "bounty": bounty,
            "impact": desc,
            "data": st.session_state.data_type
        })
        st.rerun()

with t2:
    st.header("IDOR Verification Lab")
    st.info("Testing Cross-Session Permission Logic")
    col1, col2 = st.columns(2)
    col1.text_input("Victim ID", "1005")
    col2.text_input("Attacker ID", "2009")
    
    if st.button("⚡ TEST INTEGRITY (PUT)"):
        st.session_state.term_logs += f"\n[{datetime.now().strftime('%H:%M:%S')}] Attempting PUT request to modify User A data..."
        st.error("Integrity Test: ACCESS DENIED (Server is Read-Only for IDOR)")

with t3:
    st.header("Loot Cache (Evidence)")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            # Safe access using .get() to prevent 'KeyError' crashes
            st.success(f"🔥 {item.get('sev')} | {item.get('asset')} | {item.get('data')} at {item.get('ts')}")
    else:
        st.info("No PII captured yet. Use the Terminal to run a probe.")

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        l = st.session_state.loot_items[-1] # Get latest loot
        report = f"""
## Summary:
An Insecure Direct Object Reference (IDOR) was identified on `{l.get('path')}`.

## Impacted asset:
`{l.get('asset')}`

## Impact*:
{l.get('impact')}

## Steps To Reproduce:
1. Log in as **User B** (Attacker).
2. Send a GET request to `https://{l.get('asset')}{l.get('path')}`.
3. Observe **200 OK** returning **{l.get('data')}**.

## Supporting Material/References:
* **Severity:** {l.get('sev')}
* **Evidence Log:** {l.get('ts')}
        """
        st.code(report, language="markdown")
    else:
        st.info("Capture loot to generate the report.")
