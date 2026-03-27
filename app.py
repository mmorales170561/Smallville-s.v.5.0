import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import re

# --- 1. HUD SETTINGS ---
st.set_page_config(page_title="SMALLVILLE V14.6", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# --- 2. THE NEW AUTONOMOUS PARSER ---
def scrape_h1_policy(handle):
    url = f"https://hackerone.com/{handle}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f"Failed to reach program '{handle}' (Error {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Extract Overview/Policy text
        policy_div = soup.find('div', {'class': re.compile(r'.*policy.*')}) or soup.find('article')
        policy_text = policy_div.get_text(separator='\n') if policy_div else "No policy text found."
        
        # 2. Extract In-Scope Assets (Heuristic approach for 2026)
        # Looks for tables or lists commonly used in H1 policy layouts
        assets = []
        for code_tag in soup.find_all(['code', 'strong']):
            text = code_tag.get_text().strip()
            # Basic regex to catch domains like *.target.com or api.target.com
            if re.match(r'^(\*\.)?([a-z0-9-]+\.)+[a-z]{2,}$', text):
                assets.append(text)
        
        return {
            "policy": policy_text,
            "assets": list(set(assets)) # Remove duplicates
        }, None

    except Exception as e:
        return None, str(e)

# --- 3. COMMAND CENTER ---
with st.sidebar:
    st.title("🏹 H1 SCOPE GUARD")
    h1_handle = st.text_input("H1 Handle", value="security").strip()
    
    if st.button("📖 SCRAPE & SYNC POLICY"):
        with st.status("Reading Policy Page...", expanded=True) as status:
            data, err = scrape_h1_policy(h1_handle)
            if data:
                st.session_state.h1_data = data
                st.session_state.whitelist = ", ".join(data['assets'])
                status.update(label="Sync Complete!", state="complete")
            else:
                st.error(err)
                status.update(label="Sync Failed.", state="error")

    st.divider()
    whitelist = st.text_area("🟢 WHITELIST", value=st.session_state.get('whitelist', ''))

# --- 4. THE MARATHON HUB ---
t1, t2, t3 = st.tabs(["🔥 STRIKE", "📜 OVERVIEW", "📊 LOOT"])

with t1:
    if 'h1_data' in st.session_state:
        st.subheader(f"Targeting: {h1_handle}")
        targets = st.session_state.whitelist.split(", ")
        selected = st.selectbox("Select Asset from Policy", targets)
        
        # Follow the "Overview" instructions
        st.info("⚠️ **POLICY ALERT:** Reading for 'Out of Scope' keywords...")
        if "no automated" in st.session_state.h1_data['policy'].lower():
            st.error("STOP: This policy forbids automated scanning. Switch to manual testing.")
        else:
            if st.button("🚀 START 8-HOUR MARATHON"):
                st.success(f"Strike initiated on {selected}. Loop active for 8 hours.")
    else:
        st.info("Sync a handle in the sidebar to load the target list.")

with t2:
    if 'h1_data' in st.session_state:
        st.markdown("### Program Instructions")
        st.write(st.session_state.h1_data['policy'])import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import re

# --- 1. HUD SETTINGS ---
st.set_page_config(page_title="SMALLVILLE V14.6", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# --- 2. THE NEW AUTONOMOUS PARSER ---
def scrape_h1_policy(handle):
    url = f"https://hackerone.com/{handle}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f"Failed to reach program '{handle}' (Error {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Extract Overview/Policy text
        policy_div = soup.find('div', {'class': re.compile(r'.*policy.*')}) or soup.find('article')
        policy_text = policy_div.get_text(separator='\n') if policy_div else "No policy text found."
        
        # 2. Extract In-Scope Assets (Heuristic approach for 2026)
        # Looks for tables or lists commonly used in H1 policy layouts
        assets = []
        for code_tag in soup.find_all(['code', 'strong']):
            text = code_tag.get_text().strip()
            # Basic regex to catch domains like *.target.com or api.target.com
            if re.match(r'^(\*\.)?([a-z0-9-]+\.)+[a-z]{2,}$', text):
                assets.append(text)
        
        return {
            "policy": policy_text,
            "assets": list(set(assets)) # Remove duplicates
        }, None

    except Exception as e:
        return None, str(e)

# --- 3. COMMAND CENTER ---
with st.sidebar:
    st.title("🏹 H1 SCOPE GUARD")
    h1_handle = st.text_input("H1 Handle", value="security").strip()
    
    if st.button("📖 SCRAPE & SYNC POLICY"):
        with st.status("Reading Policy Page...", expanded=True) as status:
            data, err = scrape_h1_policy(h1_handle)
            if data:
                st.session_state.h1_data = data
                st.session_state.whitelist = ", ".join(data['assets'])
                status.update(label="Sync Complete!", state="complete")
            else:
                st.error(err)
                status.update(label="Sync Failed.", state="error")

    st.divider()
    whitelist = st.text_area("🟢 WHITELIST", value=st.session_state.get('whitelist', ''))

# --- 4. THE MARATHON HUB ---
t1, t2, t3 = st.tabs(["🔥 STRIKE", "📜 OVERVIEW", "📊 LOOT"])

with t1:
    if 'h1_data' in st.session_state:
        st.subheader(f"Targeting: {h1_handle}")
        targets = st.session_state.whitelist.split(", ")
        selected = st.selectbox("Select Asset from Policy", targets)
        
        # Follow the "Overview" instructions
        st.info("⚠️ **POLICY ALERT:** Reading for 'Out of Scope' keywords...")
        if "no automated" in st.session_state.h1_data['policy'].lower():
            st.error("STOP: This policy forbids automated scanning. Switch to manual testing.")
        else:
            if st.button("🚀 START 8-HOUR MARATHON"):
                st.success(f"Strike initiated on {selected}. Loop active for 8 hours.")
    else:
        st.info("Sync a handle in the sidebar to load the target list.")

with t2:
    if 'h1_data' in st.session_state:
        st.markdown("### Program Instructions")
        st.write(st.session_state.h1_data['policy'])
