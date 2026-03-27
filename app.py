import streamlit as st
import random
import time
import re
import os
from datetime import datetime, timedelta

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="SMALLVILLE V15.2", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    .stTextArea textarea { background-color: #0a0a0a !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .stHeader { border-bottom: 1px solid #333; }
    .highlight { color: #ff3131; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GHOST ENGINE: HUMAN MIMICRY ---
def human_delay(min_sec=5, max_sec=15):
    """Randomizes sleep intervals to bypass behavioral WAF detection."""
    wait = random.uniform(min_sec, max_sec)
    time.sleep(wait)
    return wait

# --- 3. THE 8-HOUR MARATHON LOGIC ---
def start_marathon(target, mode, duration_hours=8):
    st.session_state.is_running = True
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=duration_hours)
    
    st.session_state.logs += f"\n[!] MARATHON INITIATED: {start_time.strftime('%H:%M:%S')}"
    st.session_state.logs += f"\n[!] MODE: {mode.upper()} | TARGET: {target}"
    
    # Tool sequences based on Policy Mode
    if mode == "STEALTH (Passive/Manual Mimic)":
        tools = ["Subfinder (Passive)", "Amass (Enum)", "Httpx (Title-only)", "Arjun (Low-Freq)"]
    else:
        tools = ["Subfinder", "Httpx", "Nuclei (Aggressive)", "Arjun", "Garak (AI-Scan)"]

    while datetime.now() < end_time and st.session_state.is_running:
        current_tool = random.choice(tools)
        st.session_state.logs += f"\n[*] Mimicking Human: Running {current_tool}..."
        
        # Simulated execution with randomized human-like pauses
        delay = human_delay(10, 30) 
        st.session_state.logs += f" (Paused {delay:.2f}s to mask signature)"
        
        # Logic to trigger actual subprocess.run() would go here
        time.sleep(2) # Buffer
        
        if not st.session_state.is_running: break

# --- 4. SIDEBAR: ROE & OVERRIDE ---
with st.sidebar:
    st.title("🏹 GHOST COMMAND")
    st.divider()
    
    # Manual Input
    raw_in_scope = st.text_area("🟢 IN-SCOPE", placeholder="target.com\napi.target.com", height=150)
    raw_policy = st.text_area("📜 PASTE POLICY OVERVIEW", placeholder="Paste the H1 policy text here...", height=200)
    
    st.divider()
    # Logic to auto-detect "No Automated Tools"
    auto_detect_restricted = False
    if raw_policy:
        if any(x in raw_policy.lower() for x in ["no automated", "prohibit tools", "manual only"]):
            auto_detect_restricted = True
            st.error("⚠️ RESTRICTION DETECTED: No Automated Tools.")

# --- 5. MAIN HUNTER HUB ---
t1, t2, t3 = st.tabs(["🔥 STRIKE CONTROL", "📊 ANALYZED ROE", "🛠️ SYSTEM LOGS"])

with t1:
    in_scope_list = [x.strip() for x in raw_in_scope.split('\n') if x.strip()]
    
    if not in_scope_list:
        st.info("Awaiting manual scope entry in sidebar...")
    else:
        target = st.selectbox("Active Target", in_scope_list)
        
        # Tool Swapper Logic
        strike_mode = "STEALTH (Passive/Manual Mimic)" if auto_detect_restricted else "FULL SPECTRUM (Aggressive)"
        st.write(f"**Recommended Mode:** `{strike_mode}`")
        
        col1, col2 = st.columns(2)
        if not st.session_state.get('is_running', False):
            if col1.button("🚀 LAUNCH 8-HOUR GHOST STRIKE"):
                start_marathon(target, strike_mode)
                st.rerun()
        else:
            if col1.button("🛑 EMERGENCY STOP"):
                st.session_state.is_running = False
                st.rerun()

with t2:
    if raw_policy:
        st.subheader("High-Signal Analysis")
        # Highlight critical keywords for safety
        processed_policy = raw_policy
        for word in ["BOUNTY", "EXCLUDE", "PROHIBITED", "SAFE HARBOR", "AUTOMATED"]:
            processed_policy = re.sub(f"(?i){word}", f"<span class='highlight'>{word.upper()}</span>", processed_policy)
        st.markdown(processed_policy, unsafe_allow_html=True)
    else:
        st.write("Paste policy text in sidebar to analyze ROE.")

with t3:
    if 'logs' not in st.session_state: st.session_state.logs = ""
    st.code(st.session_state.logs, language="bash")
