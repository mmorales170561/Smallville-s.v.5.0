import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import re

# --- 1. CORE CONFIG ---
st.set_page_config(page_title="SMALLVILLE V14.7", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; } b { color: #ff3131; font-weight: bold; text-decoration: underline; }</style>", unsafe_allow_html=True)

# --- 2. POLICY ANALYZER TOOLS ---
def highlight_policy(text):
    """Bolds and underlines critical H1 legal terms for fast reading."""
    keywords = [
        "bounty", "eligible", "in-scope", "out-of-scope", "exclude", 
        "prohibited", "automated", "dos", "denial of service", "critical",
        "p1", "p2", "safe harbor", "instruction"
    ]
    for word in keywords:
        # Case-insensitive replacement with HTML bold tags
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(f"<b>{word.upper()}</b>", text)
    return text

def scrape_h1_policy(handle):
    url = f"https://hackerone.com/{handle}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Smallville-Bot/2026"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f"Target '{handle}' Unreachable (Status {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract Policy Text
        policy_div = soup.find('div', {'class': re.compile(r'.*policy.*')}) or soup.find('article')
        raw_text = policy_div.get_text(separator='\n') if policy_div else "No policy found."
        
        # Extract Assets (Look for domains)
        assets = list(set(re.findall(r'[\w\*-]+\.[\w\.-]+\.[a-z]{2,}', raw_text)))
        
        return {"policy": raw_text, "assets": assets}, None
    except Exception as e:
        return None, str(e)

# --- 3. COMMAND CENTER ---
with st.sidebar:
    st.title("🏹 H1 SCOPE GUARD")
    h1_handle = st.text_input("H1 Program Handle", value="security").strip()
    
    if st.button("📖 SYNC & ANALYZE POLICY", use_container_width=True):
        data, err = scrape_h1_policy(h1_handle)
        if data:
            st.session_state.h1_data = data
            st.session_state.whitelist = ", ".join(data['assets'])
            st.success("Policy Synced!")
        else:
            st.error(err)

    st.divider()
    st.subheader("Rules of Engagement")
    whitelist = st.text_area("🟢 WHITELIST", value=st.session_state.get('whitelist', ''))

# --- 4. THE HUNTER'S HUB ---
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📜 OVERVIEW (ANALYZED)", "📊 MATRIX"])

with t1:
    if 'h1_data' in st.session_state:
        st.subheader(f"Strike Targets: {h1_handle}")
        targets = st.session_state.whitelist.split(", ")
        selected = st.selectbox("Select Target Domain", [t for t in targets if '.' in t])
        
        # Automatic Intelligence Check
        policy_lower = st.session_state.h1_data['policy'].lower()
        if any(x in policy_lower for x in ["no automated", "prohibit automated", "don't use tools"]):
            st.error("🚨 POLICY RESTRICTION: This program restricts automated tools. Engage with caution.")
        
        if st.button("🚀 INITIATE 8-HOUR MARATHON"):
            st.warning(f"Marathon active on {selected}. Scanning for P1/P2 vulnerabilities...")
    else:
        st.info("Sync a program handle to load targets.")

with t2:
    if 'h1_data' in st.session_state:
        st.subheader("Highlighted Policy Overview")
        # Use the highlighing function for "Reading Everything It Says"
        analyzed_text = highlight_policy(st.session_state.h1_data['policy'])
        st.markdown(analyzed_text, unsafe_allow_html=True)

with t3:
    st.subheader("System Arsenal")
    for tool in ["subfinder", "nuclei", "garak", "arjun"]:
        st.write(f"🟢 {tool.upper()}")
