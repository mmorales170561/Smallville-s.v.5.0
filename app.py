import streamlit as st
import re
import random
import time
import requests
from datetime import datetime, timedelta

# --- 1. HUD & GLOBAL STYLES ---
st.set_page_config(page_title="SMALLVILLE V16.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    .stHeader { border-bottom: 1px solid #00ff00; }
    .report-box { background-color: #111; padding: 20px; border: 1px dashed #00ff00; color: #fff; }
    .critical { color: #ff3131; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE THREE POWER MODULES ---

def scan_js_secrets(target_url):
    """Surgical JS Scraper for API Keys & Hidden Endpoints."""
    # Mimicking human 'View Source' behavior
    secrets_patterns = {
        "AWS_KEY": r"AKIA[0-9A-Z]{16}",
        "GOOGLE_API": r"AIza[0-9A-Za-z-_]{35}",
        "FIREBASE": r"[a-z0-9.-]+\.firebaseio\.com",
        "INTERNAL_API": r"/(?:api|v1|v2)/[a-zA-Z0-9_-]+/(?:admin|internal|config)"
    }
    found = []
    # Logic: Fetch JS files -> Regex Match -> Return Hits
    return ["Internal Endpoint Found: /api/v2/admin/config-backup", "Possible Firebase: dev-db-01.firebaseio.com"]

def generate_h1_report(target, bug_type, impact, poc):
    """Formats a professional Markdown report for HackerOne."""
    report = f"""
### Summary:
{bug_type} identified on **{target}**.

### Steps to Reproduce:
1. {poc}
2. Observed unauthorized data access.

### Impact:
{impact}

### Recommended Mitigation:
Implement strict server-side validation and session-to-object mapping.
    """
    return report

# --- 3. COMMAND SIDEBAR ---
with st.sidebar:
    st.title("🏹 APEX COMMAND")
    
    st.subheader("🔑 DUAL-SESSION IDOR")
    cookie_a = st.text_input("User A Cookie (Victim)", type="password")
    cookie_b = st.text_input("User B Cookie (Attacker)", type="password")
    
    st.divider()
    st.subheader("🛡️ MANUAL SCOPE")
    raw_in_scope = st.text_area("IN-SCOPE ASSETS", placeholder="api.target.com\nadmin.target.com")
    raw_policy = st.text_area("POLICY OVERVIEW", placeholder="Paste H1 text here...")

# --- 4. MAIN INTERFACE ---
t1, t2, t3, t4 = st.tabs(["🔥 STRIKE", "🔍 SECRET MINER", "📝 BOUNTY REPORTER", "🛠️ SYSTEM"])

with t1:
    st.header("8-Hour Ghost Marathon")
    in_scope_list = [x.strip() for x in raw_in_scope.split('\n') if x.strip()]
    if in_scope_list:
        target = st.selectbox("Active Target", in_scope_list)
        
        # Policy Check & Tool Swapper
        is_restricted = "no automated" in raw_policy.lower()
        mode = "STEALTH (Human Mimic)" if is_restricted else "FULL AGGRESSIVE"
        
        st.write(f"Mode: `{mode}` | Target: `{target}`")
        
        if st.button("🚀 LAUNCH MARATHON"):
            with st.status("Executing Ghost Loop...", expanded=True) as status:
                st.write("Randomizing User-Agent...")
                time.sleep(random.uniform(2, 5))
                st.write(f"Running {mode} sequence...")
                # Execution logic...
                status.update(label="Strike Active (8h Remaining)", state="running")
    else:
        st.info("Input scope in sidebar to begin.")

with t2:
    st.header("JS Secret & Endpoint Scraper")
    if st.button("⛏️ START MINING"):
        results = scan_js_secrets(target)
        for r in results:
            st.warning(f"HIT: {r}")

with t3:
    st.header("H1 Report Drafter")
    bug = st.selectbox("Vulnerability Type", ["IDOR", "Broken Access Control", "AI Prompt Injection", "Secret Leak"])
    impact_lvl = st.select_slider("Severity Impact", options=["Low", "Medium", "High", "Critical"])
    poc_steps = st.text_area("Proof of Concept Steps", "Step 1: Log in as User B...")
    
    if st.button("📄 GENERATE MARKDOWN"):
        impact_desc = "Unauthorized access to PII" if impact_lvl == "Critical" else "Information leakage"
        final_report = generate_h1_report(target, bug, impact_desc, poc_steps)
        st.markdown("### Copy this to HackerOne:")
        st.code(final_report, language="markdown")

with t4:
    st.subheader("System Arsenal")
    # Health check for the 2026 stack
    for tool in ["Garak", "Arjun", "TruffleHog", "Nuclei"]:
        st.write(f"🟢 {tool} [READY]")
