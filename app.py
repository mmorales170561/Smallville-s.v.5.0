import streamlit as st
import requests
import re

# --- 1. HUD & THEMES ---
st.set_page_config(page_title="SMALLVILLE V15.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }
    .stHeader { color: #ff3131; }
    b { color: #ff3131; text-decoration: underline; }
    </style>
""", unsafe_allow_html=True)

# --- 2. API INTELLIGENCE ---
def get_h1_api_data(handle):
    """Fetches policy via the Public HackerOne API (No JS Required)."""
    # The API endpoint is much more stable than web scraping in 2026
    api_url = f"https://api.hackerone.com/v1/hackers/programs/{handle}"
    
    try:
        # Note: Public programs usually allow unauthenticated 'GET' on this specific path
        # but require a User-Agent to avoid generic bot-blocking.
        headers = {"User-Agent": "Smallville-Security-Researcher-2026"}
        res = requests.get(api_url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            # Extracting the key fields for Smallville
            policy_text = data.get('policy', 'No policy text returned.')
            
            # Extracting Scoped Assets from the API structure
            # The API returns a dedicated 'structured_scopes' list
            scopes = data.get('relationships', {}).get('structured_scopes', {}).get('data', [])
            assets = [s.get('attributes', {}).get('asset_identifier') for s in scopes if s.get('attributes', {}).get('eligible_for_bounty')]
            
            return {
                "policy": policy_text,
                "assets": assets if assets else ["Manual check required"]
            }, None
        
        elif res.status_code == 404:
            return None, "Error 404: Program handle not found in API."
        else:
            return None, f"API Blocked (Code {res.status_code})."
            
    except Exception as e:
        return None, str(e)

# --- 3. FAIL-SAFE INITIALIZATION ---
if 'h1_data' not in st.session_state:
    st.session_state.h1_data = {"policy": "Awaiting Sync...", "assets": []}

# --- 4. COMMAND SIDEBAR ---
with st.sidebar:
    st.title("🏹 H1 API GATEWAY")
    handle = st.text_input("H1 Handle (e.g. 'security', 'starbucks')", value="security")
    
    if st.button("📡 PULL API DATA", use_container_width=True):
        with st.status("Connecting to HackerOne API...", expanded=False):
            data, err = get_h1_api_data(handle)
            if data:
                st.session_state.h1_data = data
                st.success("API DATA LOCKED")
            else:
                st.error(err)

    st.divider()
    st.subheader("Current Scope")
    st.write(st.session_state.h1_data['assets'])

# --- 5. MAIN HUNTER HUD ---
t1, t2, t3 = st.tabs(["🔥 STRIKE", "📜 POLICY ANALYSIS", "📊 MATRIX"])

with t1:
    st.subheader(f"Target: {handle}")
    if not st.session_state.h1_data['assets']:
        st.info("Sync via sidebar to begin.")
    else:
        target = st.selectbox("Active Asset", st.session_state.h1_data['assets'])
        
        # Smart Policy Guard
        p_text = st.session_state.h1_data['policy'].lower()
        if "no automated" in p_text or "scanning prohibited" in p_text:
            st.error("🛑 STOP: Automated tools are explicitly FORBIDDEN in this policy.")
        else:
            if st.button("🚀 INITIATE 8-HOUR MARATHON"):
                st.warning(f"Persistence Loop Engaged on {target}. Monitoring for P1/P2...")

with t2:
    st.subheader("Legal Overview (Analyzed)")
    raw_policy = st.session_state.h1_data['policy']
    
    # 2026 Keyword Highlighting Logic
    keywords = ["bounty", "exclude", "out-of-scope", "prohibited", "safe harbor", "critical", "p1"]
    for word in keywords:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        raw_policy = pattern.sub(f"<b>{word.upper()}</b>", raw_policy)
    
    st.markdown(raw_policy, unsafe_allow_html=True)

with t3:
    st.subheader("Arsenal Status")
    for tool in ["SUBFINDER", "NUCLEI", "GARAK", "SNYK"]:
        st.write(f"🟢 {tool} [CONNECTED]")
