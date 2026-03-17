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
        white-space: pre-wrap; height: 400px; overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE SETUP (SMART MIGRATION) ---
def init_db():
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    # Create table if it doesn't exist
    conn.execute('''CREATE TABLE IF NOT EXISTS ledger 
                    (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, intel TEXT, 
                     report TEXT, crit_count INTEGER, high_count INTEGER)''')
    
    # Check for missing columns (Migration)
    cursor = conn.execute("PRAGMA table_info(ledger)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'crit_count' not in columns:
        conn.execute("ALTER TABLE ledger ADD COLUMN crit_count INTEGER DEFAULT 0")
    if 'high_count' not in columns:
        conn.execute("ALTER TABLE ledger ADD COLUMN high_count INTEGER DEFAULT 0")
        
    conn.commit()
    conn.close()

def parse_vulns(text):
    # Improved regex to handle colored terminal output tags
    crit = len(re.findall(r"\[critical\]", text, re.IGNORECASE))
    high = len(re.findall(r"\[high\]", text, re.IGNORECASE))
    return crit, high

init_db()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("PRIME ELITE TOOLS"):
        subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.rerun()

    st.divider()
    if st.button("☢️ WIPE DATABASE", help="Use this if you get SQL errors"):
        if os.path.exists('red_kryptonite_ledger.db'):
            os.remove('red_kryptonite_ledger.db')
            st.success("Database purged. Refreshing...")
            time.sleep(1)
            st.rerun()

    st.divider()
    debug_mode = st.toggle("DEBUG MODE", value=False)
    st.header("⚡ PHASE TOGGLES")
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: HOOK", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
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
                prog = st.progress(0, text="Initializing Sequence...")
                term = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope), 
                    "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                    "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                    "DEBUG": "1" if debug_mode else "0", "PORT_PROFILE": port_profile
                })
                
                p = subprocess.Popen(["bash", "powers.sh", "strike", root_url, target_name], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env, bufsize=1)
                
                full_rep = ""
                for line in iter(p.stdout.readline, ''):
                    full_rep += line
                    if "PHASE 1" in line: prog.progress(25, text="Phase 1: Mapping...")
                    if "PHASE 2" in line: prog.progress(50, text="Phase 2: Archiving...")
                    if "PHASE 3" in line: prog.progress(75, text="Phase 3: Port Scan...")
                    if "PHASE 4" in line: prog.progress(90, text="Phase 4: Striking...")
                    term.markdown(f'<div class="terminal-box">{full_rep}</div>', unsafe_allow_html=True)
                
                p.wait()
                prog.progress(100, text="Mission Complete.")
                c_cnt, h_cnt = parse_vulns(full_rep)
                
                conn = sqlite3.connect('red_kryptonite_ledger.db')
                sql = "INSERT INTO ledger (timestamp, target, intel, report, crit_count, high_count) VALUES (?, ?, ?, ?, ?, ?)"
                conn.execute(sql, (datetime.now().strftime('%Y-%m-%d %H:%M'), target_name, "Complete", full_rep, c_cnt, h_cnt))
                conn.commit()
                conn.close()
                st.rerun()

with t2:
    st.subheader("🗄️ INTELLIGENCE LEDGER")
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT id, timestamp, target, crit_count, high_count FROM ledger ORDER BY id DESC", conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Ledger Error: {e}. Try clicking 'Wipe Database' in the sidebar.")

with t3:
    st.subheader("📑 MISSION ARCHIVE")
    search = st.text_input("🔍 Search Logs", "").lower()
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        reps = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        conn.close()
        
        for _, row in reps.iterrows():
            if search in row['target'].lower() or search in row['report'].lower():
                with st.expander(f"MISSION: {row['target']} | 🔥 {row['crit_count']} CRIT"):
                    st.markdown(f'<div class="terminal-box" style="height:350px;">{row["report"]}</div>', unsafe_allow_html=True)
                    st.download_button(f"Download Log {row['id']}", row['report'], file_name=f"log_{row['id']}.txt", key=f"dl_{row['id']}")
    except:
        st.info("No logs found.")
