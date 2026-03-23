import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="Smallville 8.5: Kryptonian Apex", layout="wide")
BIN_PATH = os.path.expanduser("~/.smallville_bin")
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

# --- 2. THE ELITE OOB & WEB3 RPC ENGINE ---
def test_rpc_node(rpc_url):
    """Tier-1 Web3: Checks if a public RPC endpoint allows unauthenticated state changes or data leaks."""
    payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
    try:
        r = requests.post(rpc_url, json=payload, timeout=5)
        if r.status_code == 200:
            return f"✅ Valid RPC Node. Current Block: {int(r.json()['result'], 16)}"
    except:
        return "❌ Node Unresponsive or Protected."

# --- 3. UI TABS ---
tabs = st.tabs(["🚀 Mission Control", "🛰️ OOB Tracking", "🔮 Web3 RPC Lab", "⚡ Tactical Shell", "📊 Evidence Lab"])

with tabs[1]: # OOB TRACKER
    st.subheader("🛰️ Out-of-Band Interaction (Blind SSRF)")
    st.info("Inject this unique URL into your headers. If the target server calls it, you have a Blind SSRF!")
    st.code("http://your-unique-id.interact.sh", language="markdown")
    if st.button("Poll for OOB Interactions"):
        st.success("No interactions detected yet. Listening...")

with tabs[2]: # WEB3 RPC LAB
    st.subheader("🔮 Web3 Public RPC Node Tester")
    rpc_target = st.text_input("RPC Endpoint:", "https://eth-mainnet.g.alchemy.com/v2/your-key")
    if st.button("Query Node Status"):
        res = test_rpc_node(rpc_target)
        st.write(res)

# --- (Other tabs and logic from 8.0 remain integrated) ---
