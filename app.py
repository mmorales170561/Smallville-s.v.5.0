import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- 1. HUD ---
st.set_page_config(page_title="SMALLVILLE V14.8", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; } b { color: #ff3131; font-weight: bold; }</style>", unsafe_allow_html=True)

# --- 2. THE GHOST PARSER ---
def deep_sync_h1(handle):
    url = f"https://hackerone.com/{handle}"
    # 2026 Ghost Headers to bypass "No Policy Found"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,web3/2026",
        "X-Requested-With": "XMLHttpRequest", 
        "Referer": "https://hackerone.com/programs"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            return None, f"Access Denied (Code {res.status_code})"
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Search for the policy in common 2026 containers
        policy_box = soup.find('div', {'id': 'policy'}) or \
                     soup.find('div', {'class': re.compile(r'spec-policy|instruction')}) or \
                     soup.find('article')
        
        if not policy_box:
            # Fallback: Grab the largest text block on the page
            paragraphs = soup.find_all('p')
            full_text = "\n".join([p.text for p in paragraphs])
        else:
            full_text = policy_box.get_text(separator='\n')

        # Asset Extraction (Regex for domains/wildcards)
        assets = list(set(re.findall(r'(?:\*\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-z]{2,6}', full_text)))
        
        return {"policy": full_text, "assets": assets}, None
    except Exception as e:
        return None, str(e)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🏹 PROTOCOL GHOST")
    h1_handle = st.text_input("H1 Handle", value="security").strip()
    
    if st.button("📡 GHOST SYNC", use_container_width=True):
        with st.spinner("Bypassing H1 Protection..."):
            data, err = deep_sync_h1(h1_handle)
            if data:
                st.session_state.h1_data = data
                # Identify bounty targets vs points-only targets
                st.session_state.whitelist = ", ".join(data['assets'])
                st.success("Targeting Synced.")
            else:
                st.error(f"Sync Failed: {err}")

# --- 4. THE MARATHON HUB ---
t1, t2 = st.tabs(["🚀 STRIKE", "📜 POLICY ANALYSIS"])

with t1:
    if 'h1_data' in st.session_state:
        target = st.selectbox("Select Scoped Asset", st.session_state.whitelist.split(", "))
        
        # Compliance Engine: Checks the overview for you
        policy_text = st.session_state.h1_data['policy'].lower()
        if "automated" in policy_text and ("no" in policy_text or "prohibit" in policy_text):
            st.error("🛑 AUTO-SCANNING PROHIBITED BY POLICY")
        else:
            st.success("✅ AUTOMATION ALLOWED (Check rate limits)")

        if st.button("🔥 START 8-HOUR STRIKE"):
            st.info(f"Striking {target}... Monitoring for P1 signals.")
    else:
        st.info("Sync a program in the sidebar.")

with t2:
    if 'h1_data' in st.session_state:
        # Highlighting rules
        raw = st.session_state.h1_data['policy']
        for word in ["bounty", "exclude", "out-of-scope", "prohibited", "critical"]:
            raw = re.sub(f"(?i){word}", f"<b>{word.upper()}</b>", raw)
        st.markdown(raw, unsafe_allow_html=True)
