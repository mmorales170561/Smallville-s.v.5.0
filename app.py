import streamlit as st
import subprocess
import os
import requests
import json
import time

# --- 1. T2 CORE CONFIG ---
st.set_page_config(page_title="SMALLVILLE T2 VANGUARD", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: 1px solid #ff3131; transition: 0.3s; } .stButton>button:hover { background-color: #000 !important; color: #ff3131 !important; }</style>", unsafe_allow_html=True)

# T2 Workspaces (Simulating persistence)
BIN_DIR = "/tmp/ruby_bin"
LOOT_DIR = "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]:
    if not os.path.exists(d): os.makedirs(d)

# --- 2. THE NOTIFICATION UPLINK ---
def send_alert(message):
    """Sends tactical alerts to a Discord/Slack Webhook."""
    webhook_url = st.session_state.get('webhook_url', '')
    if webhook_url:
        payload = {"content": f"🚨 **SMALLVILLE T2 ALERT**: {message}"}
        try:
            requests.post(webhook_url, json=payload, timeout=5)
        except:
            pass

# --- 3. THE AUTOMATED CHAIN ENGINE ---
def run_t2_chain(target):
    """Tier 2 Logic: Recon -> Filter -> Scan -> Alert"""
    log = st.status(f"🛰️ INITIALIZING CHAIN: {target}", expanded=True)
    
    # PHASE 1: RECON
    log.write("🔍 Phase 1: Subdomain Discovery...")
    # Example: subfinder -d target.com -o loot.txt
    loot_file = os.path.join(LOOT_DIR, f"{target}_subs.txt")
    subprocess.run(f"{BIN_DIR}/subfinder -d {target} -o {loot_file}", shell=True, capture_output=True)
    
    with open(loot_file, 'r') as f:
        subs = f.readlines()
    log.write(f"✅ Found {len(subs)} subdomains.")
    
    # PHASE 2: AUTOMATED FILTERING (HTTPX)
    log.write("⚡ Phase 2: Probing Alive Hosts...")
    alive_file = os.path.join(LOOT_DIR, f"{target}_alive.txt")
    subprocess.run(f"cat {loot_file} | {BIN_DIR}/httpx -o {alive_file}", shell=True, capture_output=True)
    
    # PHASE 3: VULNERABILITY SCAN (NUCLEI)
    log.write("🧪 Phase 3: Targeted Vulnerability Scan...")
    vuln_file = os.path.join(LOOT_DIR, f"{target}_vulns.txt")
    subprocess.run(f"{BIN_DIR}/nuclei -l {alive_file} -severity critical,high -o {vuln_file}", shell=True, capture_output=True)
    
    # PHASE 4: ALERTING
    if os.path.exists(vuln_file) and os.path.getsize(vuln_file) > 0:
        send_alert(f"CRITICAL VULNS FOUND ON {target}. Check Loot Tab.")
        log.update(label="🔥 CHAIN COMPLETE: VULNERABILITIES DETECTED", state="error")
    else:
        log.update(label="🛡️ CHAIN COMPLETE: NO CRITICALS FOUND", state="complete")

# --- 4. SIDEBAR & CONTROL ---
with st.sidebar:
    st.title("🔴 T2 COMMAND")
    st.text_input("📡 WEBHOOK URL", key="webhook_url", type="password", help="Discord/Slack Webhook for 24/7 Alerts")
    
    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        # Logic from v8.8
        st.toast("Forging T2 Engines...")
        st.rerun()
        
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 AUTHORIZED", key='in_scope', value="example.com")
    st.text_area("🔴 FORBIDDEN", key='out_scope', value=".gov, .mil")

# --- 5. MAIN HUD ---
st.title("🏹 SMALLVILLE T2 VANGUARD")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "💰 LOOT", "📊 MATRIX", "🛠️ TERMINAL"])

with t1:
    target = st.text_input("TARGET ACQUISITION", key="tgt_input")
    if st.button("🔥 INITIATE AUTOMATED CHAIN"):
        if target:
            run_t2_chain(target)
        else:
            st.warning("No target acquired.")

with t2:
    st.subheader("📋 COLLECTED INTEL (LOOT)")
    loot_files = os.listdir(LOOT_DIR)
    if loot_files:
        selected_file = st.selectbox("Select Loot File", loot_files)
        with open(os.path.join(LOOT_DIR, selected_file), 'r') as f:
            st.code(f.read())
        st.download_button("📥 Download Loot", f.read(), file_name=selected_file)
    else:
        st.info("No loot collected yet.")

with t3:
    # Matrix logic from v8.8
    st.subheader("SYSTEM INTEGRITY")
    tools = ["subfinder", "httpx", "katana", "nuclei", "aderyn", "arjun", "trufflehog", "sqlmap"]
    cols = st.columns(4)
    for i, name in enumerate(tools):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")
