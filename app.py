import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. CLOUD ENVIRONMENT SETUP ---
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
    .status-online { background-color: rgba(0,255,65,0.15); border: 2px solid #00ff41 !important; color: #00ff41; }
    .status-offline { background-color: rgba(255,234,0,0.05); border: 1px solid #ffea00 !important; color: #ffea00; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .crit-alert { color: #ff0000; font-weight: bold; animation: pulse 1s infinite; border: 1px solid #ff0000; padding: 10px; text-align: center; margin-bottom: 10px; }
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
    
    script_exists = os.path.exists("powers.sh")
    tools = ["nuclei", "naabu", "subfinder", "httpx"]
    ready = all([os.path.exists(f"/tmp/bin/{t}") for t in tools])
    
    # GREEN STATUS WHEN ONLINE
    if ready:
        st.markdown(f'''<div class="status-panel status-online">
            <h3 style="margin:0;">SYSTEMS ONLINE</h3>
            <small>Armory Primed: {st.session_state["last_prime"]}</small>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div class="status-panel status-offline">
            <h3 style="margin:0;">SYSTEMS OFFLINE</h3>
            <code>RE-PRIME REQUIRED</code>
        </div>''', unsafe_allow_html=True)

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        if not script_exists:
            st.error("powers.sh NOT FOUND")
        else:
            with st.spinner("📦 Fetching Tech..."):
                script_path = os.path.join(os.getcwd(), "powers.sh")
                res = subprocess.run(["bash", script_path, "prime"], capture_output=True, text=True)
                if res.returncode == 0:
                    st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
                    st.rerun()
                else:
                    st.error(f"Prime Failed: {res.stderr}")

    st.divider()
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: HOOK", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_in, col_term = st.columns([1, 2.2])
    with col_in:
        st.subheader("Mission Brief")
        # RESTORED INPUTS
        target_name = st.text_input("🎯 TARGET NAME", key="tn")
        root_url = st.text_input("🔗 ROOT DOMAIN", key="ru")
        in_scope = st.text_area("✓ IN-SCOPE ASSETS", placeholder="example.com\napi.example.com", key="is")
        out_scope = st.text_area("✗ OUT-OF-SCOPE", placeholder="dev.example.com", key="os")
        
        st.divider()
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.warning("Armory is empty. Prime tools in sidebar first.")
            elif root_url and target_name:
                st.session_state['crit_found'] = False
                prog = st.progress(0, text="Sequence Initialized...")
                header = st.empty()
                term = st.empty()
                
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope),
                    "OUT_SCOPE": str(out_scope),
                    "RUN_P1": "1" if p1 else "0",
                    "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0",
                    "RUN_P4": "1" if p4 else "0"
                })
                
                script_path = os.path.join(os.getcwd(), "powers.sh")
                cmd = ["bash", script_path, "strike", str(root_url), str(target_name)]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_rep = ""
                for line in iter(p.stdout.readline, ''):
                    full_rep += line
                    # Progress Logic
                    if "PHASE 1" in line: prog.progress(25, text="Phase 1: Recon")
                    elif "PHASE 2" in line: prog.progress(50, text="Phase 2: Discovery")
                    elif "PHASE 3" in line: prog.progress(75, text="Phase 3: Fuzzing")
                    elif "PHASE 4" in line: prog.progress(90, text="Phase 4: Striking")
                    
                    if "[critical]" in line.lower():
                        st.session_state['crit_found'] = True
                    
                    if st.session_state['crit_found']:
                        header.markdown('<div class="crit-alert">⚠️ CRITICAL VULNERABILITY DETECTED ⚠️</div>', unsafe_allow_html=True)

                    term.markdown(f'<div class="terminal-box">{full_rep}</div>', unsafe_allow_html=True)
                
                p.wait()
                st.success("Mission Complete")
                # SQL logic would go here to save full_rep

with t2:
    st.subheader("🗄️ MISSION LEDGER")
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT id, timestamp, target, crit_count, high_count FROM ledger ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, width="stretch", hide_index=True)
    except:
        st.info("Ledger is currently empty.")

with t3:
    st.subheader("📑 MISSION ARCHIVE")
    st.info("Archive sync active. Select a mission from the Ledger to view details.")
