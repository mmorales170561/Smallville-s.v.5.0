import os
import sys
import subprocess

# --- 0. DEPENDENCY SELF-HEAL ---
# This ensures BeautifulSoup and Requests are present before the rest of the app loads
def heal_dependencies():
    try:
        import bs4
        import requests
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "requests", "--break-system-packages"])
        os.execl(sys.executable, sys.executable, *sys.argv) # Restart script to load new modules

heal_dependencies()

import streamlit as st
import shutil
from datetime import datetime, timedelta

# --- 1. THE H1 POLICY INTELLIGENCE ---
def fetch_h1_policy(handle):
    """
    HackerOne programs often expose their structured scope via their public handle.
    This function pulls the 'Instruction' and 'Bounty Eligibility' for each asset.
    """
    headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0 Smallville-Bot/2026"}
    url = f"https://hackerone.com/{handle}.json"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None, f"Error: Program '{handle}' not found (Status {res.status_code})"
        
        data = res.json()
        policy_text = data.get("policy", "No policy text found.")
        scopes = data.get("structured_scopes", [])
        
        # Filter for only bounty-eligible assets to avoid 'points-only' rabbit holes
        bounty_assets = [
            {
                "identifier": s.get("asset_identifier"),
                "type": s.get("asset_type"),
                "instruction": s.get("instruction", "None provided.")
            }
            for s in scopes if s.get("eligible_for_bounty")
        ]
        
        return {"policy": policy_text, "assets": bounty_assets}, None
    except Exception as e:
        return None, str(e)

# --- 2. LAYOUT & UI ---
st.set_page_config(page_title="SMALLVILLE V14.3", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# --- 3. SIDEBAR: THE POLICY ENGINE ---
with st.sidebar:
    st.title("🛡️ POLICY ENGINE")
    h1_handle = st.text_input("HackerOne Handle", value="security", help="e.g., 'uber', 'starbucks', 'security'").strip()
    
    if st.button("📖 READ & SYNC POLICY", use_container_width=True):
        data, err = fetch_h1_policy(h1_handle)
        if err:
            st.error(err)
        else:
            st.session_state.h1_data = data
            st.session_state.whitelist = ", ".join([a['identifier'] for a in data['assets']])
            st.success(f"Synced {len(data['assets'])} Bounty Assets!")

    st.divider()
    st.subheader("Rules of Engagement")
    # This text area is now auto-filled by the scraper
    whitelist_str = st.text_area("🟢 WHITELIST (Bounty Eligible)", value=st.session_state.get('whitelist', ''))
    
# --- 4. MAIN HUD ---
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📖 POLICY OVERVIEW", "📊 MATRIX", "🛠️ CONSOLE"])

with t1:
    st.subheader("Autonomous Strike Control")
    target = st.selectbox("SELECT ASSET FROM SCOPE", st.session_state.get('whitelist', '').split(", "))
    
    if target:
        # Show specific instructions for the selected asset
        if 'h1_data' in st.session_state:
            asset_info = next((a for a in st.session_state.h1_data['assets'] if a['identifier'] == target), None)
            if asset_info:
                st.warning(f"**INSTRUCTION FOR {target}:**\n{asset_info['instruction']}")
        
        col1, col2 = st.columns(2)
        if col1.button("🔥 INITIATE 8-HOUR MARATHON"):
            st.session_state.is_running = True
            # The run_marathon function would go here
    else:
        st.info("Sync a policy in the sidebar to select a target.")

with t2:
    st.subheader("Program Policy & Safe Harbor")
    if 'h1_data' in st.session_state:
        st.markdown(st.session_state.h1_data['policy'])
    else:
        st.write("No policy data loaded.")

with t4:
    st.subheader("⌨️ SYSTEM CONSOLE")
    # Persistent terminal logs
    if 'term_logs' not in st.session_state: st.session_state.term_logs = ""
    st.code(st.session_state.term_logs, language="bash")
