import streamlit as st
from datetime import datetime

# --- 1. SEVERITY LOGIC ENGINE ---
def calculate_severity(data_type):
    """Maps data types to HackerOne standard severity levels."""
    levels = {
        "SSN/Financial": "P1 CRITICAL",
        "PII (Email/Phone)": "P2 HIGH",
        "Internal Metadata": "P3 MEDIUM",
        "Version/Software Info": "P4 LOW"
    }
    return levels.get(data_type, "P3 MEDIUM")

# --- 2. GLOBAL BOOTLOADER ---
if 'term_logs' not in st.session_state: 
    st.session_state.term_logs = f"[*] SYSTEM ONLINE | {datetime.now().strftime('%H:%M:%S')}"
if 'loot_items' not in st.session_state: 
    st.session_state.loot_items = []

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    in_scope = st.text_input("🎯 TARGET ASSET", value="api.target.com")
    
    st.divider()
    st.subheader("⚖️ SEVERITY CONFIG")
    data_found = st.selectbox("Detected Data Type", ["PII (Email/Phone)", "SSN/Financial", "Internal Metadata", "Version/Software Info"])
    current_sev = calculate_severity(data_found)
    st.info(f"Calculated Priority: **{current_sev}**")

# --- 4. THE COMMAND TABS ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "💰 LOOT CACHE", "🧪 IDOR LAB", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    st.code(st.session_state.term_logs, language="bash")
    
    if st.button("🧪 RUN IDOR CHECK", use_container_width=True):
        ts = datetime.now().strftime('%H:%M:%S')
        target_path = "/api/v1/user/1005"
        
        # Log to Terminal
        st.session_state.term_logs += f"\n[{ts}] GET {target_path} --> 200 OK"
        st.session_state.term_logs += f"\n[{ts}] Found {data_found} in response body."
        
        # Save to Loot with the Calculator's Severity
        st.session_state.loot_items.append({
            "ts": ts,
            "asset": in_scope,
            "path": target_path,
            "data": data_found,
            "severity": current_sev
        })
        st.rerun()

with t2:
    st.header("Loot Cache")
    for item in st.session_state.loot_items:
        st.success(f"🔥 {item['severity']} | {item['asset']} | {item['data']}")

with t4:
    st.header("HackerOne Submission Draft")
    if st.session_state.loot_items:
        latest = st.session_state.loot_items[-1]
        
        h1_report = f"""
## Summary:
An Insecure Direct Object Reference (IDOR) was identified on `{latest['path']}`.

## Impacted asset:
`{latest['asset']}`

## Steps To Reproduce:
1. Log in as **User B** (Attacker).
2. Request `https://{latest['asset']}{latest['path']}`.
3. Observe **200 OK** returning **{latest['data']}**.

## Supporting Material/References:
* **Severity:** {latest['severity']}
* **Evidence Timestamp:** {latest['ts']}
        """
        st.code(h1_report, language="markdown")
    else:
        st.info("Run a check to generate a report.")
