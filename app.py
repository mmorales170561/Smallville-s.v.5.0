import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. ENVIRONMENT & SESSION ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'last_prime' not in st.session_state: st.session_state['last_prime'] = "NEVER"
if 'crit_found' not in st.session_state: st.session_state['crit_found'] = False

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI STYLING ---
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
    .crit-alert { color: #ff0000; font-weight: bold; animation: pulse 1s infinite; border: 1px solid #ff0000; padding: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
def init_db():
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS ledger 
                    (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT, 
                     report TEXT, crit_count INTEGER, high_count INTEGER)''')
    conn.commit()
    conn.close()

def parse_vulns(text):
    crit = len(re.findall(r"\[critical\]", text, re.IGNORECASE))
    high = len(re.findall(r"\[high\]", text, re.IGNORECASE))
    return crit, high

init_db()

# --- 4. SIDEBAR ARMORY ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    tools = ["nuclei", "naabu", "subfinder", "httpx"]
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
        with st.spinner("📦 Fetching Tech..."):
            res = subprocess.run(["bash", "powers.sh", "prime"], capture_output=True, text=True)
            if res.returncode == 0:
                st.session_state["last_prime"] = datetime.now().strftime("%H:%M:%S")
                st.rerun()
            else:
                st.error(f"Prime Failed: {res.stderr}")

    st.divider()
    p1, p2 = st.toggle("P1: CEREBRO", True), st.toggle("P2: SHADOW", True)
    p3, p4 = st.toggle("P3: HOOK", True), st.toggle("P4: STRIKE", True)
    port_profile = st.selectbox("PORT PROFILE", ["Top 20 (Ghost)", "Top 100", "Top 1000"])

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    col_input, col_term = st.columns([1, 2.2])
    with col_input:
        st.subheader("Mission Brief")
        target_name = st.text_input("🎯 TARGET NAME", key="tn")
        root_url = st.text_input("🔗 ROOT DOMAIN", key="ru")
        in_scope = st.text_area("✓ IN-SCOPE ASSETS", key="is")
        out_scope = st.text_area("✗ OUT-OF-SCOPE", key="os")
        
        if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
            if not ready:
                st.warning("Armory is empty. Prime tools in sidebar first.")
            elif root_url and target_name:
                st.session_state['crit_found'] = False
                prog = st.progress(0, text="Sequence Initialized...")
                term_header = st.empty()
                term_display = st.empty()
                
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope), 
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                    "PORT_PROFILE": port_profile
                })
                
                cmd = ["bash", "powers.sh", "strike", str(root_url), str(target_name)]
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_rep = ""
                for line in iter(p.stdout.readline, ''):
                    full_rep += line
                    # PHASE UPDATES
                    if "PHASE 1" in line: prog.progress(25, text="Phase 1: Active")
                    elif "PHASE 2" in line: prog.progress(50, text="Phase 2: Active")
                    elif "PHASE 3" in line: prog.progress(75, text="Phase 3: Active")
                    elif "PHASE 4" in line: prog.progress(90, text="Phase 4: Striking")
                    
                    # CRITICAL PULSE TRIGGER
                    if "[critical]" in line.lower():
                        st.session_state['crit_found'] = True
                    
                    if st.session_state['crit_found']:
                        term_header.markdown('<div class="crit-alert">⚠️ CRITICAL VULNERABILITY DETECTED ⚠️</div>', unsafe_allow_html=True)
                    else:
                        term_header.info("Scan in progress... No criticals detected yet.")

                    term_display.markdown(f'<div class="terminal-box">{full_rep}</div>', unsafe_allow_html=True)
                
                p.wait()
                prog.progress(100, text="Mission Complete.")
                c_cnt, h_cnt = parse_vulns(full_rep)
                
                conn = sqlite3.connect('red_kryptonite_ledger.db')
                sql_q = """INSERT INTO ledger (timestamp, target, intel, report, crit_count, high_count) 
                           VALUES (?, ?, ?, ?, ?, ?)"""
                conn.execute(sql_q, (datetime.now().strftime('%Y-%m-%d %H:%M'), target_name, "Complete", full_rep, c_cnt, h_cnt))
                conn.commit()
                conn.close()
                st.rerun()

    with col_term:
        st.subheader("Live Terminal Output")
        st.info("Awaiting command to fire...")

with t2:
    st.subheader("🗄️ INTELLIGENCE LEDGER")
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    df = pd.read_sql_query("SELECT id, timestamp, target, crit_count, high_count FROM ledger ORDER BY id DESC", conn)
    conn.close()
    st.dataframe(df, width="stretch", hide_index=True)

with t3:
    st.subheader("📑 MISSION ARCHIVE")
    search = st.text_input("🔍 Search Logs", "").lower()
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    reps = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
    conn.close()
    for _, row in reps.iterrows():
        if search in row['target'].lower() or search in row['report'].lower():
            with st.expander(f"LOG: {row['target']} | 🔥 {row['crit_count']} CRITICAL"):
                st.markdown(f'<div class="terminal-box" style="height:300px;">{row["report"]}</div>', unsafe_allow_html=True)
