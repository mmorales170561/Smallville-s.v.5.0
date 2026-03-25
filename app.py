import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil

# --- 1. STABLE HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. THE VAULT (PERSISTENCE) ---
# Ensuring these exist so the app doesn't crash on a fresh boot
state_keys = {
    'last_log': 'SYSTEM RECOVERY COMPLETE.', 
    'in_scope': 'example.com', 
    'out_scope': '.gov, .mil', 
    'target': '',
    'battery': 'Web2'
}
for k, v in state_keys.items():
    if k not in st.session_state: st.session_state[k] = v

# --- 3. CORE ENGINES ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                p = os.path.join(root, f)
                os.chmod(p, 0o755)
                return p
    return shutil.which(name)

# --- 4. SIDEBAR (STABLE RENDER) ---
with st.sidebar:
    st.title("🔴
