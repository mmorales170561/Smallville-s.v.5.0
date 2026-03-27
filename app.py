import streamlit as st
import requests  # This must be here
import os
import shutil
from datetime import datetime, timedelta

# --- 1. SETTINGS & PATHS ---
st.set_page_config(page_title="SMALLVILLE V14.5", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# Define directories
BIN_DIR = "/tmp/ruby_bin"
LOOT_DIR = "/tmp/ruby_loot"
for d in [BIN_DIR, LOOT_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# --- 2. H1 POLICY LOGIC ---
def get_h1_data(handle):
    # This function uses the 'requests' library imported at the top
    headers = {"Accept": "application/json", "User-Agent": "Smallville-Scanner/2026"}
    url = f"https://hackerone.com/{handle}.json"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json(), None
        return None, f"Status {r.status_code}: Program not found."
    except Exception as e:
        return None, str(e)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🏹 H1 COMMANDER")
    h1_handle = st.text_input("H1 Handle", value="security").strip()
    
    if st.button("📖 SYNC POLICY", use_container_width=True):
        data, err = get_h1_data(h1_handle)
        if data:
            st.session_state.h1_policy = data
            # Filter for Bounty-Eligible assets only
            assets = [s['asset_identifier'] for s in data.get('structured_scopes', []) if s.get('eligible_for_bounty')]
            st.session_state.whitelist = ", ".join(assets)
            st.success(f"Locked onto {len(assets)} assets!")
        else:
            st.error(f"Sync Failed: {err}")

    st.divider()
    whitelist = st.text_area("🟢 WHITELIST", value=st.session_state.get('whitelist', ''))

# --- 4. MAIN HUD ---
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📜 POLICY OVERVIEW", "📊 MATRIX"])

with t1:
    if 'h1_policy' in st.session_state:
        st.subheader(f"Targeting: {h1_handle}")
        targets = st.session_state.whitelist.split(", ")
        selected = st.selectbox("Select Asset", targets)
        
        # Display Instructions
        scopes = st.session_state.h1_policy.get('structured_scopes', [])
        instr = next((s.get('instruction') for s in scopes if s.get('asset_identifier') == selected), "No specific instructions.")
        
        st.info(f"**INSTRUCTION:** {instr}")
        
        if st.button("🚀 START 8-HOUR MARATHON"):
            st.warning(f"Marathon engaged on {selected}...")
    else:
        st.info("Sync a program handle in the sidebar to begin.")

with t2:
    if 'h1_policy' in st.session_state:
        st.markdown(st.session_state.h1_policy.get('policy', 'No policy text.'))

with t3:
    st.subheader("Arsenal Health")
    for tool in ["subfinder", "nuclei", "garak"]:
        ready = shutil.which(tool) or os.path.exists(os.path.join(BIN_DIR, tool))
        st.write(f"{'🟢' if ready else '🔴'} {tool.upper()}")
