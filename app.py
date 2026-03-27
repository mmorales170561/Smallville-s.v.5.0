import streamlit as st
import subprocess
import os
import time
import shutil
import requests
import zipfile
import io
from datetime import datetime, timedelta

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="SMALLVILLE V14.0 - MARATHON", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #00ff00; } .terminal-box { background:#000; color:#00ff00; padding:15px; height:400px; overflow:auto; border: 1px solid #00ff00; font-size: 11px; white-space: pre-wrap; }</style>", unsafe_allow_html=True)

LOCAL_BIN = "/home/appuser/.local/bin"
BIN_DIR, LOOT_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

os.environ["PATH"] = f"{LOCAL_BIN}:{BIN_DIR}:" + os.environ["PATH"]

if 'term_logs' not in st.session_state: st.session_state.term_logs = "SYSTEM INITIALIZED. READY FOR LONG-HAUL RECON..."
if 'is_running' not in st.session_state: st.session_state.is_running = False

# --- 2. THE PERSISTENT STRIKE ENGINE ---
def run_marathon(target_url):
    st.session_state.is_running = True
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=8)
    
    st.toast(f"🚀 Marathon Strike Initiated. Target: {target_url}")
    st.session_state.term_logs += f"\n[!] STRIKE START: {start_time.strftime('%H:%M:%S')}\n[!] WINDOW: 8 HOURS (UNTIL {end_time.strftime('%H:%M:%S')})\n"
    
    # Define the "Deep Scan" Routine
    scan_steps = [
        f"subfinder -d {target_url} -o {LOOT_DIR}/subs.txt",
        f"httpx -l {LOOT_DIR}/subs.txt -o {LOOT_DIR}/alive.txt",
        f"nuclei -l {LOOT_DIR}/alive.txt -as -o {LOOT_DIR}/vulns.txt",
        f"python3 {BIN_DIR}/arjun/arjun.py -u https://{target_url} -oJ {LOOT_DIR}/params.json",
        f"garak --model_name {target_url} --probes all"
    ]
    
    while st.session_state.is_running and datetime.now() < end_time:
        for cmd in scan_steps:
            if not st.session_state.is_running: break
            
            st.session_state.term_logs += f"\n[*] EXECUTING: {cmd}\n"
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            st.session_state.term_logs += process.stdout + process.stderr
            
            # Brief sleep to prevent CPU throttling in the Streamlit container
            time.sleep(5) 
            
        st.session_state.term_logs += "\n[!] Cycle Complete. Re-scanning for delta changes...\n"
        time.sleep(60) # Wait 1 minute before the next deep iteration

# --- 3. SIDEBAR COMMAND ---
with st.sidebar:
    st.title("🏹 H1 COMMAND")
    target = st.text_input("TARGET", key="target_input", placeholder="target.com")
    
    st.divider()
    if not st.session_state.is_running:
        if st.button("🔥 START 8-HOUR STRIKE", use_container_width=True):
            run_marathon(target)
    else:
        if st.button("🛑 EMERGENCY STOP", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

    st.divider()
    if st.button("🔌 PRIME ARSENAL"):
        # Logic to install Arjun, Subfinder, Nuclei, Garak, Httpx (from v13.3)
        st.toast("Installing Deep-Scan tools...")

# --- 4. THE HUNTER'S HUB ---
t1, t2, t3, t4 = st.tabs(["📊 MATRIX", "🧪 DEEP ANALYSIS", "💰 LOOT", "🛠️ CONSOLE"])

with t1:
    st.subheader("Arsenal Integrity")
    tools = ["subfinder", "httpx", "nuclei", "arjun", "garak", "trufflehog"]
    cols = st.columns(3)
    for i, name in enumerate(tools):
        ready = shutil.which(name) or os.path.exists(os.path.join(BIN_DIR, name))
        status = "🟢" if ready else "🔴"
        cols[i % 3].metric(name.upper(), status)

with t2:
    st.subheader("Chaining & Deep Logic")
    st.info("The 8-hour loop uses 'Arjun' to find hidden parameters (?debug=true, ?admin=1) that Nuclei misses.")
    st.write("Current Strike Status:", "🏃 RUNNING" if st.session_state.is_running else "💤 IDLE")

with t3:
    st.subheader("💰 EVIDENCE VAULT")
    files = os.listdir(LOOT_DIR)
    if files:
        sel = st.selectbox("View Evidence", files)
        with open(os.path.join(LOOT_DIR, sel), 'r') as f:
            st.code(f.read())
    else:
        st.info("Loot vault is empty. Initiate strike to collect intel.")

with t4:
    st.subheader("⌨️ SYSTEM CONSOLE")
    st.markdown(f'<div class="terminal-box">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
