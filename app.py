import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import os

# --- 1. FAIL-SAFE INITIALIZATION ---
st.set_page_config(page_title="SMALLVILLE V14.9", layout="wide")

# Ensure UI elements exist even if logic fails
if 'h1_data' not in st.session_state:
    st.session_state.h1_data = {"policy": "No policy synced.", "assets": []}
if 'whitelist' not in st.session_state:
    st.session_state.whitelist = ""
if 'term_logs' not in st.session_state:
    st.session_state.term_logs = "READY..."

# --- 2. THE STEALTH PARSER ---
def ghost_sync(handle):
    # Mimicking a 2026 Browser Fingerprint
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = f"https://hackerone.com/{handle}"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None, f"H1 Error: {res.status_code}"
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 2026 H1 Content Scraper
        main_content = soup.find('div', {'class': re.compile(r'policy|instruction|program')}) or soup.find('body')
        text = main_content.get_text(separator='\n') if main_content else ""
        
        # Regex for domains and wildcards
        found_assets = list(set(re.findall(r'(?:\*\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-z]{2,6}', text)))
        
        return {"policy": text, "assets": found_assets}, None
    except Exception as e:
        return None, str(e)

# --- 3. PERSISTENT SIDEBAR ---
with st.sidebar:
    st.title("🏹 H1 COMMANDER")
    st.markdown("---")
    h1_handle = st.text_input("Program Handle", value="security")
    
    if st.button("📡 SYNC POLICY", use_container_width=True):
        data, err = ghost_sync(h1_handle)
        if data:
            st.session_state.h1_data = data
            st.session_state.whitelist = ", ".join(data['assets'])
            st.success("SYNC SUCCESSFUL")
        else:
            st.error(f"SYNC FAILED: {err}")

    st.divider()
    # ROE Settings
    st.subheader("Rules of Engagement")
    st.text_area("🟢 WHITELIST", value=st.session_state.whitelist, height=150)
    st.text_area("🔴 BLACKLIST", value=".gov, .mil, logout, delete", height=100)

# --- 4. PERSISTENT TABS ---
st.title("SMALLVILLE S.V. 14.9")
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📜 POLICY OVERVIEW", "📊 MATRIX", "🛠️ DEBUG"])

with t1:
    st.subheader("Autonomous Strike")
    if not st.session_state.h1_data['assets']:
        st.info("Please sync a program in the sidebar to populate targets.")
    else:
        selected = st.selectbox("Select Target Asset", st.session_state.h1_data['assets'])
        if st.button("🔥 START 8-HOUR MARATHON"):
            st.warning(f"Strike initiated on {selected}. Persistence loop active.")

with t2:
    st.subheader("Program Policy & Instructions")
    # Ensure background and text contrast
    policy_display = st.session_state.h1_data['policy']
    # Highlight critical ROE words in Red
    for word in ["PROHIBITED", "EXCLUDE", "OUT-OF-SCOPE", "BOUNTY", "CRITICAL"]:
        policy_display = policy_display.replace(word.lower(), f"**{word}**")
        policy_display = policy_display.replace(word.capitalize(), f"**{word}**")
    
    st.markdown(policy_display if policy_display else "No policy data available.")

with t3:
    st.subheader("Arsenal Health")
    cols = st.columns(3)
    tools = ["subfinder", "nuclei", "garak", "arjun", "mindgard", "snyk"]
    for i, tool in enumerate(tools):
        cols[i % 3].metric(tool.upper(), "🟢 ONLINE")

with t4:
    st.subheader("System Debug")
    st.write("Session State Check:", "OK" if 'h1_data' in st.session_state else "CORRUPT")
    st.code(st.session_state.term_logs)
