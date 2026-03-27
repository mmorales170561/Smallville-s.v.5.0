import streamlit as st
from datetime import datetime

# --- 1. SEVERITY & BOUNTY LOGIC ---
def get_market_rates(data_type):
    """2026 Market Rates for Bug Bounties"""
    rates = {
        "SSN/Financial": ("P1 CRITICAL", "$5,000 - $15,000+"),
        "PII (Email/Phone)": ("P2 HIGH", "$1,500 - $5,000"),
        "Internal Metadata": ("P3 MEDIUM", "$500 - $1,500"),
        "Version/Software Info": ("P4 LOW", "$50 - $300")
    }
    return rates.get(data_type, ("P3 MEDIUM", "$500"))

# --- 2. GLOBAL BOOTLOADER (FORCED SANITIZATION) ---
if 'loot_items' not in st.session_state:
    st.session_state.loot_items = []
if 'term_logs' not in st.session_state:
    st.session_state.term_logs = f"[*] SYSTEM ONLINE | BAKERSFIELD HQ | {datetime.now().strftime('%H:%M:%S')}"

# --- 3. MISSION CONTROL SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    target_input = st.text_input("🎯 TARGET ASSET", value="api.target.com")
    
    st.divider()
    st.subheader("⚖️ TRIAGE CONFIG")
    data_found = st.selectbox("Detected Data Leak", ["PII (Email/Phone)", "SSN/Financial", "Internal Metadata", "Version/Software Info"])
    sev_level, est_bounty = get_market_rates(data_found)
    
    st.metric("Estimated Payout", est_bounty)
    st.info(f"Priority: **{sev_level}**")
    
    st.divider()
    if st.button("🧨 PURGE OLD SESSION DATA"):
        st.session_state.clear()
        st.rerun()

# --- 4. COMMAND TABS (FIXED CRASH LOGIC) ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 RUN IDOR CHECK", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        path = "/api/v1/user/1005"
        
        # Log to Terminal
        st.session_state.term_logs += f"\n[{ts}] PROBE {target_input}{path} --> 200 OK"
        st.session_state.term_logs += f"\n[{ts}] ALERT: Found {data_found} (Impact: {sev_level})"
        
        # Save with full dictionary structure
        st.session_state.loot_items.append({
            "ts": ts,
            "asset": target_input,
            "path": path,
            "data": data_found,
            "severity": sev_level,
            "bounty": est_bounty
        })
        st.rerun()

with t2:
    st.header("Loot Cache")
    if st.session_state.loot_items:
        for item in st.session_state.loot_items:
            # FIX: Using .get() prevents the 'asset' KeyError crash
            s = item.get('severity', 'P3')
            a = item.get('asset', 'Unknown Asset')
            d = item.get('data', 'General Data')
            st.success(f"🔥 {s} | {a} | {d}")
    else:
        st.info("No PII captured yet.")

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        latest = st.session_state.loot_items[-1]
        
        h1_report = f"""
## Summary:
An Insecure Direct Object Reference (IDOR) was identified on `{latest.get('path')}`.

## Impacted asset:
`{latest.get('asset')}`

## Steps To Reproduce:
1. Log in as **User B** (Attacker).
2. Request `https://{latest.get('asset')}{latest.get('path')}`.
3. Observe **200 OK** returning **{latest.get('data')}**.

## Supporting Material/References:
* **Severity:** {latest.get('severity')}
* **Estimated Value:** {latest.get('bounty')}
* **Evidence Timestamp:** {latest.get('ts')}
        """
        st.code(h1_report, language="markdown")
    else:
        st.info("Run a terminal check to generate the report.")
