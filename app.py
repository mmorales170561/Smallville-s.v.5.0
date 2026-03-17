import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. CLOUD ENVIRONMENT SETUP ---
# Ensure /tmp/bin is in the PATH for the current session
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"
if 'crit_found' not in st.session_state: st.session_state['crit_found'] = False

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
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 1px solid #333; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .crit-alert { color: #ff0000; font-weight: bold; animation: pulse 1s infinite; border: 1px solid #ff0000; padding: 5px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE ---
def init_db():
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS ledger 
                    (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT, 
                     report TEXT, crit_count INTEGER, high_count INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# --- 4. SIDEBAR ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # CLOUD CHECK: Is the script present?
    script_exists = os.path.exists("powers.sh")
    if script_exists:
        st.caption("✅ powers.sh detected")
    else:
        st.error("❌ powers.sh NOT FOUND")

    # Check for binaries in /tmp/bin
    tools = ["nuclei", "naabu", "subfinder"]
    ready = all([os.path.exists(f"/tmp/bin/{t}") for t in tools])
    
    if ready:
        st.markdown(f'''<div class="status-panel" style="background-color: rgba(0,255,65,0.1); border-color: #00ff41;">
            <h3 style="color: #00ff41; margin:0;">SYSTEMS ONLINE</h3>
            <small style="color: #888;">Armory Primed: {st.session_state["last_prime"]}</small>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div class="status-panel" style="background-color: rgba(255,234,0,0.1); border-color: #ffea00;">
            <h3 style="color: #ffea00; margin:0;">SYSTEMS OFFLINE</h3>
            <code style="color: #ffea00;">RE-PRIME REQUIRED</code>
        </div>''', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        if not script_exists:
            st.error("Cannot prime: powers.sh is missing from the repository.")
        else:
            with st.spinner("📦 Fetching Tech..."):
                # Use absolute pathing for Cloud stability
                script_path = os.path.join(os.getcwd(), "powers.sh")
                res = subprocess.run(["bash", script_path, "prime"], capture_output=True, text=True)
                
                if res.returncode == 0:
                    st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
                    st.success("Armory Primed!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Prime Failed")
                    st.code(res.stderr)

    st.divider()
    p1, p2 = st.toggle("P1: CEREBRO", True), st.toggle("P2: SHADOW", True)
    p3, p4 = st.toggle("P3: HOOK", True), st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_in, col_term = st.columns([1, 2.2])
    with col_in:
        st.subheader("Mission Brief")
        tn = st.text_input("🎯 TARGET NAME", key="tn")
        ru = st.text_input("🔗 ROOT DOMAIN", key="ru")
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.warning("Prime tools first.")
            elif tn and ru:
                st.session_state['crit_found'] = False
                prog = st.progress(0, text="Initializing...")
                header = st.empty()
                term = st.empty()
                
                env = os.environ.copy()
                env.update({"RUN_P1": "1" if p1 else "0", "RUN_P4": "1" if p4 else "0"})
                
                cmd = ["bash", "powers.sh", "strike", str(ru), str(tn)]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
                
                full_rep = ""
                for line in iter(p.stdout.readline, ''):
                    full_rep += line
                    if "[critical]" in line.lower():
                        st.session_state['crit_found'] = True
                    
                    if st.session_state['crit_found']:
                        header.markdown('<div class="crit-alert">⚠️ CRITICAL DETECTED ⚠️</div>', unsafe_allow_html=True)
                    
                    term.markdown(f'<div class="terminal-box">{full_rep}</div>', unsafe_allow_html=True)
                p.wait()
                st.success("Mission Complete")

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    if os.path.exists('red_kryptonite_ledger.db'):
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        st.dataframe(df, width="stretch", hide_index=True)
        conn.close()

with t3:
    st.subheader("📑 MISSION ARCHIVE")
    st.info("Archive sync active.")
