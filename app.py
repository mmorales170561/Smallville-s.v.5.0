import streamlit as st
from datetime import datetime
import time
import random

# --- 1. MASTER BOOT (PREVENTS UI BLACKOUTS) ---
def master_boot():
    defaults = {
        'term_logs': f"[*] SYSTEM READY | BAKERSFIELD HQ | {datetime.now().strftime('%H:%M:%S')}",
        'loot_items': [],
        'in_scope': "api.target.com",
        'data_type': "PII (Email/Phone)",
        'is_scanning': False,
        'ua_cookie': "",
        'ub_cookie': ""
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

master_boot()

# --- 2. UI & STYLING ---
st.set_page_config(page_title="SMALLVILLE V18.5", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #00ff00; min-width: 350px; }
    .stMetric { background: #111; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    .stButton>button { width: 100%; border-radius: 0px; font-weight: bold; }
    .fire-button>button { background-color: #ff4b4b !important; color: white !important; border: none !important; font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MISSION CONTROL SIDEBAR ---
with st.sidebar:
    st.title("🏹 MISSION CONTROL")
    st.divider()
    
    # Target Inputs
    st.session_state.in_scope = st.text_area("🟢 IN-SCOPE ASSETS", st.session_state.in_scope, height=80)
    
    # TARGET FIRE BUTTON
    st.markdown('<div class="fire-button">', unsafe_allow_html=True)
    if st.button("🔥 TARGET FIRE"):
        st.session_state.is_scanning = True
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Triage Settings
    st.subheader("⚖️ TRIAGE CONFIG")
    st.session_state.data_type = st.selectbox("Current Focus", 
        ["PII (Email/Phone)", "SSN/Financial", "Internal Metadata", "Version/Software Info"])
    
    st.divider()
    
    # Session Management
    st.subheader("🔑 SESSION TOKENS")
    st.session_state.ua_cookie = st.text_input("Cookie A", type="password", value=st.session_state.ua_cookie)
    st.session_state.ub_cookie = st.text_input("Cookie B", type="password", value=st.session_state.ub_cookie)
    
    if st.button("🧨 PURGE SESSION"):
        st.session_state.clear()
        st.rerun()

# --- 4. MAIN DASHBOARD ---
t1, t2, t3, t4 = st.tabs(["🖥️ TERMINAL", "🧪 IDOR LAB", "💰 LOOT CACHE", "📝 REPORT DRAFTER"])

with t1:
    st.header("Ghost Terminal")
    
    # Logic for "TARGET FIRE" Sequence
    if st.session_state.is_scanning:
        with st.status("🚀 EXECUTING KRYPTON STRIKE...", expanded=True) as status:
            st.write("🔍 Running Subfinder (Discovery)...")
            time.sleep(1)
            st.write("📡 Running HTTPX (Probing)...")
            time.sleep(1)
            st.write("🏹 Running Arjun (Parameter Mining)...")
            time.sleep(1)
            st.write("🛡️ Running Nuclei (Template Matching)...")
            
            ts = datetime.now().strftime('%H:%M:%S')
            st.session_state.term_logs += f"\n[{ts}] STRIKE COMPLETE: Found IDOR on /api/v1/auth"
            st.session_state.term_logs += f"\n[{ts}] ALERT: Nuclei detected Exposed .git directory"
