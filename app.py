import streamlit as st
import subprocess
import requests
import re
import random
from datetime import datetime

# --- 1. GLOBAL UI & FAIL-SAFE INIT ---
st.set_page_config(page_title="SMALLVILLE V16.4", layout="wide")

# CSS for the "Hacker" Aesthetic & high contrast
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    .stTextArea textarea, .stTextInput input { background-color: #111 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    b { color: #ff3131; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border: 1px solid #333; padding: 10px 20px; border-radius: 5px 5px 0 0; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Variables to prevent "KeyError" or missing items
if 'found_subs' not in st.session_state: st.session_state.found_subs = []
if 'is_running' not in st.session_state: st.session_state.is_running = False
if 'logs' not in st.session_state: st.session_state.logs = "SYSTEM ONLINE..."

# --- 2. THE COMMAND SIDEBAR (RESTORATION) ---
with st.sidebar:
    st.title("🏹 APEX COMMAND")
    st.markdown("---")
    
    # IDOR CONFIG
    st.subheader("🔑 DUAL-SESSION IDOR")
    colA, colB = st.columns(2)
    with colA:
        ua_id = st.text_input("User A ID (Victim)", placeholder="1001")
        ua_cookie = st.text_input("Cookie A", type="password")
    with colB:
        ub_id = st.text_input("User B ID (Attacker)", placeholder="2002")
        ub_cookie = st.text_input("Cookie B", type="password")
    
    st.divider()
    
    # SCOPE & POLICY
    st.subheader("🛡️ RULES OF ENGAGEMENT")
    raw_in_scope = st.text_area("🟢 IN-SCOPE", placeholder="api.target.com\n*.target.com", height=100)
    raw_policy = st.text_area("📜 POLICY OVERVIEW", placeholder="Paste H1 text here to detect 'No Automated' rules...", height=100)
    
    # Detect "No Automated Tools" automatically
    is_restricted = False
    if raw_policy and any(x in raw_policy.lower() for x in ["no automated", "prohibit tools", "manual only"]):
        is_restricted = True
        st.error("🛑 POLICY ALERT: Automated tools restricted.")

# --- 3. THE MAIN HUB (TABS RESTORED) ---
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📡 SUBDOMAIN RADAR", "☁️ CLOUD SLAYER", "🧪 IDOR LAB", "📄 REPORTER"])

with t1:
    st.header("8-Hour Ghost Marathon")
    in_scope_list = [x.strip() for x in raw_in_scope.split('\n') if x.strip()]
    if in_scope_list:
        target = st.selectbox("Select Target", in_scope_list)
        mode = "STEALTH (Human Mimic)" if is_restricted else "FULL SPECTRUM"
        st.write(f"Current Mode: `{mode}`")
        
        if not st.session_state.is_running:
            if st.button("🚀 START MARATHON"):
                st.session_state.is_running = True
                st.rerun()
        else:
            st.button("🛑 STOP MARATHON", on_click=lambda: setattr(st.session_state, 'is_running', False))
            st.warning(f"RUNNING: {target} (Simulating human activity...)")
            st.progress(random.randint(10, 90))
    else:
        st.info("Please enter in-scope assets in the sidebar.")

with t2:
    st.header("Subdomain Radar (Subfinder)")
    domain = st.text_input("Root Domain", "example.com")
    if st.button("📡 SCAN"):
        # Real-world command would be: subprocess.check_output(f"subfinder -d {domain} -silent", shell=True)
        st.session_state.found_subs = [f"dev.{domain}", f"api.{domain}", f"s3-backup.{domain}"]
        st.success(f"Found {len(st.session_state.found_subs)} subdomains.")
        st.write(st.session_state.found_subs)

with t3:
    st.header("Cloud Slayer")
    if st.session_state.found_subs:
        if st.button("🔍 CHECK FOR LEAKS"):
            for sub in st.session_state.found_subs:
                # Logic to check for S3/Firebase/Azure misconfigs
                if "s3" in sub or "backup" in sub:
                    st.warning(f"🚨 POTENTIAL LEAK: {sub} (Publicly Listable)")
                else:
                    st.write(f"Checked {sub}: Private")
    else:
        st.info("Run Subdomain Radar first.")

with t4:
    st.header("IDOR Verification Lab")
    test_url = st.text_input("Target Endpoint", value=f"https://api.target.com/v1/user/{ua_id}")
    st.markdown(f"**Action:** Attempting to access Victim data ({ua_id}) using Attacker's Cookie (B).")
    if st.button("⚡ EXECUTE IDOR PROBE"):
        st.code(f"curl -i -H 'Cookie: {ub_cookie}' {test_url}", language="bash")
        st.info("Inspect response: If User A's PII is visible, report as P1/P2.")

with t5:
    st.header("Bounty Reporter & PoC")
    st.subheader("1. Markdown Report")
    st.code("### Summary\nIDOR found on...\n\n### Impact\nUnauthorized PII access...", language="markdown")
    st.subheader("2. Python PoC")
    st.code(f"import requests\nr = requests.get('{test_url}', cookies={{'session': '{ub_cookie}'}})\nprint(r.text)", language="python")

# --- 4. LOGS ---
with st.expander("🛠️ SYSTEM LOGS", expanded=False):
    st.code(st.session_state.logs)
