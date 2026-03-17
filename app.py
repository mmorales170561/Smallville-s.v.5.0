import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
import re
from datetime import datetime

# --- 1. ENVIRONMENT ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

if 'auth' not in st.session_state: st.session_state['auth'] = False

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
    .vuln-badge { padding: 2px 8px; border-radius: 4px; font-weight: bold; margin-right: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE & ANALYTICS ---
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

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    tools_ready = os.path.exists("/tmp/bin/nuclei")
    st.markdown(f'<div style="background-color: {"#00ff41" if tools_ready else "#ffea00"}; color: black; padding: 5px; text-align: center; border-radius: 5px; font-weight: bold;">SYSTEMS {"ONLINE" if tools_ready else "OFFLINE"}</div>', unsafe_allow_html=True)
    
    if st.button("PRIME ELITE TOOLS"):
        subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.rerun()

    st.divider()
    debug_mode = st.toggle("DEBUG MODE", value=False)
    st.header("⚡ PHASE TOGGLES")
    p1, p2 = st.toggle("P1: CEREBRO", value=True), st.toggle("P2: SHADOW", value=True)
    p3, p4 = st.toggle("P3: HOOK", value=True), st.toggle("P4: STRIKE", value=True)
    port_profile = st.selectbox("PORT PROFILE", ["Top 20 (Ghost)", "Top 100", "Top 1000"])

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ MISSION LEDGER", "📑 MISSION ARCHIVE"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        target_name = st.text_input("🎯 TARGET NAME")
        root_url = st.text_input("🔗 ROOT DOMAIN")
        in_scope = st.text_area("✓ IN-SCOPE")
        out_scope = st.text_area("✗ OUT-OF-SCOPE")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if root_url and target_name:
                prog = st.progress(0, text="Initializing...")
                term = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({"IN_SCOPE": in_scope, "OUT_SCOPE": out_scope, "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0", "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0", "DEBUG": "1" if debug_mode else "0", "PORT_PROFILE": port_profile})
                
                p = subprocess.Popen(["bash", "powers.sh", "strike", root_url, target_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_rep = ""
                for line in iter(p.stdout.readline, ''):
                    full_rep += line
                    if "PHASE 1" in line: prog.progress(25)
                    if "PHASE 2" in line: prog.progress(50)
                    if "PHASE 3" in line: prog.progress(75)
                    if "PHASE 4" in line: prog.progress(90)
                    term.markdown(f'<div class="terminal-box">{full_rep}</div>', unsafe_allow_html=True)
                
                p.wait()
                prog.progress(100)
                c_cnt, h_cnt = parse_vulns(full_rep)
                
                conn = sqlite3.connect('red_kryptonite_ledger.db')
                conn.execute("INSERT INTO ledger (timestamp, target, intel, report, crit_count, high_count) VALUES (?, ?, ?, ?, ?, ?)",
                             (datetime.now().strftime('%Y-%m-%d %H:%M'), target_name, "Complete", full_rep, c_cnt, h_cnt))
                conn.commit()
                conn.close()
                st.rerun()

with t2:
    st.subheader("🗄️ INTELLIGENCE LEDGER")
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    df = pd.read_sql_query("SELECT id, timestamp, target, crit_count, high_count FROM ledger ORDER BY id DESC", conn)
    conn.close()
    st.dataframe(df, use_container_width=True, hide_index=True)

with t3:
    st.subheader("📑 MISSION ARCHIVE")
    search = st.text_input("🔍 Search Logs", "").lower()
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    reps = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
    conn.close()
    
    for _, row in reps.iterrows():
        if search in row['target'].lower() or search in row['report'].lower():
            with st.expander(f"MISSION: {row['target']} | 🔥 {row['crit_count']} CRIT"):
                st.markdown(f'<div class="terminal-box" style="height:300px;">{row["report"]}</div>', unsafe_allow_html=True)
