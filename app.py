import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime

# --- 1. ENVIRONMENT & PERSISTENCE ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

# Initialize Session State for Scope Stability
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'output' not in st.session_state: st.session_state['output'] = ""

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto;
    }
    .stButton>button { background-color: #ff0000; color: black; font-weight: bold; border: none; }
    .stTextArea textarea { background-color: #111; color: #00ff41; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- 3. AUTH GATE ---
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("KRYPTONIAN ACCESS")
        u = st.text_input("ID", placeholder="clark_kent")
        p = st.text_input("CRYPT", type="password")
        if st.button("AUTHORIZE"):
            if u == "clark_kent" and p == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- 4. SIDEBAR TOOLBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("PRIME ELITE TOOLS"):
        with st.spinner("FETCHING ARSENAL..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.success("ELITE TOOLS ONLINE")
    
    st.divider()
    st.header("⚙️ MISSION CONFIG")
    # Toggle for Phase 2 (Shadow Archive/GAU)
    shadow_toggle = st.toggle("PHASE 2: SHADOW ARCHIVE", value=True, help="Toggle Wayback/CommonCrawl URL discovery")
    
    st.divider()
    if st.button("WIPE DATABASE"):
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        conn.execute("DROP TABLE IF EXISTS ledger")
        conn.commit()
        conn.close()
        st.info("Ledger Purged.")

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "🖼️ GALLERY"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        # Tier 1: The Root Target
        target_name = st.text_input("🎯 TARGET NAME", placeholder="e.g., Tesla, X, Google")
        root_url = st.text_input("🔗 ROOT DOMAIN", placeholder="example.com")
        
        # Tier 2: In-Scope (Specific allowed assets)
        in_scope = st.text_area("✓ IN-SCOPE", placeholder="api.example.com\nprod.example.com", height=100)
        
        # Tier 3: Out-of-Scope (Blacklisted assets)
        out_scope = st.text_area("✗ OUT-OF-SCOPE", placeholder="dev.example.com\n*.staging.example.com", height=100)
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if root_url and target_name:
                terminal = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope),
                    "OUT_SCOPE": str(out_scope),
                    "RUN_SHADOW": "1" if shadow_toggle else "0"
                })
                
                # Execute Strike
                p = subprocess.Popen(["bash", "powers.sh", "strike", root_url, target_name], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env)
                
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()
                st.rerun()
            else:
                st.error("NAME AND ROOT DOMAIN REQUIRED.")

with t2:
    st.subheader("🗄️ MISSION INTELLIGENCE LEDGER")
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("Awaiting Recon Data...")

with t3:
    st.subheader("🖼️ RECON GALLERY")
    st.info("Visual intelligence will populate based on successful strikes.")
