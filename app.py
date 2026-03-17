import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# --- 2026 ENVIRONMENT ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- KRYPTONIAN UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 400px; overflow-y: auto;
    }
    .secret-card {
        background-color: #1a1a1a; border-left: 5px solid #ffea00; 
        padding: 10px; margin-bottom: 10px; color: #ffea00; font-size: 0.85rem;
    }
    .stButton>button { background-color: #ff0000; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- VULNERABILITY DICTIONARY ---
VULN_MAP = {
    "git-config": "Exposed Git Configuration. Source code leak possible.",
    "env-file": "Environment File Exposure. DB/API secrets leaked.",
    "subdomain-takeover": "Subdomain Takeover. High risk of phishing/malware hosting.",
    "js-secret": "Hardcoded Credentials in JS. API keys found in code.",
    "cve": "Documented CVE. Exploit is publicly available."
}

# --- DB HELPERS ---
def get_db():
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    conn.execute('CREATE TABLE IF NOT EXISTS ledger (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT, ports INTEGER, vulns INTEGER, poc TEXT)')
    return conn

# --- AUTH GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("KRYPTONIAN ACCESS")
        u = st.text_input("ID")
        p = st.text_input("CRYPT", type="password")
        if st.button("AUTHORIZE"):
            if u == "clark_kent" and p == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "🖼️ GALLERY & DEEP DIVE"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        target
