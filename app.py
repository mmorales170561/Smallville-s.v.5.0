import streamlit as st
from datetime import datetime

# --- 1. IMPACT LOGIC ENGINE ---
def get_impact_description(data_type):
    """Generates professional Impact statements for H1 reports."""
    impacts = {
        "SSN/Financial": "Critical: Full compromise of user financial data, leading to identity theft and regulatory (GDPR/CCPA) non-compliance.",
        "PII (Email/Phone)": "High: Mass harvesting of user contact details, enabling targeted phishing attacks and privacy violations.",
        "Internal Metadata": "Medium: Leakage of system architecture and user UUIDs, aiding in further exploitation of the infrastructure.",
        "Version/Software Info": "Low: Information disclosure of server versions, allowing attackers to map the attack surface for known CVEs."
    }
    return impacts.get(data_type, "Unauthorized access to restricted data endpoints.")

# --- 2. GLOBAL BOOTLOADER ---
if 'loot_items' not in st.session_state: st.session_state.loot_items = []
if 'term_logs' not in st.session_state: st.session_state.term_logs = "[*] SYSTEM READY"

# --- 3. MISSION CONTROL SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    target_asset = st.text_input("🎯 TARGET ASSET", value="api.target.com")
    
    st.divider()
    st.subheader("⚖️ IMPACT CONFIG")
    data_found = st.selectbox("Data Type", ["PII (Email/Phone)", "SSN/Financial", "Internal Metadata", "Version/Software Info"])
    
    # Logic: Auto-calculate Impact
    impact_statement = get_impact_description(data_found)
    st.warning(f"**Impact:** {impact_statement}")

# --- 4. COMMAND TABS ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    if st.button("🧪 RUN IDOR CHECK"):
        ts = datetime.now().strftime('%H:%M:%S')
        st.session_state.term_logs += f"\n[{ts}] IDOR HIT on {target_asset} --> 200 OK ({data_found})"
        st.session_state.loot_items.append({
            "ts": ts, "asset": target_asset, "path": "/api/v1/user/1005",
            "data": data_found, "impact_desc": impact_statement
        })
        st.rerun()

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        latest = st.session_state.loot_items[-1]
        h1_report = f"""
## Summary:
IDOR identified on `{latest.get('path')}`.

## Impacted asset:
`{latest.get('asset')}`

## Impact*:
{latest.get('impact_desc')}

## Steps To Reproduce:
1. Log in as **User B** (Attacker).
2. Request `https://{latest.get('asset')}{latest.get('path')}`.
3. Observe **200 OK** returning **{latest.get('data')}**.
        """
        st.code(h1_report, language="markdown")
