import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime

# --- DATABASE ARCHIVE ENGINE ---
def init_db():
    conn = sqlite3.connect('daily_planet_vault.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vault 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, domain TEXT, 
                  severity TEXT, finding TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS leaks 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, domain TEXT, 
                  source TEXT, leak_count INTEGER)''')
    conn.commit()
    conn.close()

def log_to_vault(domain, severity, finding):
    conn = sqlite3.connect('daily_planet_vault.db')
    c = conn.cursor()
    c.execute("INSERT INTO vault (timestamp, domain, severity, finding, status) VALUES (?,?,?,?,?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M"), domain, severity, finding, "Unreported"))
    conn.commit()
    conn.close()

# --- PROFESSIONAL AESTHETIC ---
st.set_page_config(page_title="The Daily Planet | Watchtower", layout="wide")
init_db()

st.markdown("""
    <style>
    .stApp { background-color: #f4f1ea; color: #1a1a1a; font-family: 'Georgia', serif; }
    .masthead { text-align: center; border-bottom: 3px double #000; padding: 20px; margin-bottom: 30px; }
    .masthead h1 { font-family: 'Times New Roman', serif; font-size: 48px; font-weight: 900; color: #002244; margin: 0; }
    .masthead p { font-style: italic; color: #666; }
    .stButton>button { 
        background-color: #002244; color: #ffffff; border-radius: 2px; 
        font-weight: bold; width: 100%; height: 3em; border: none;
    }
    .stButton>button:hover { background-color: #ff0000; color: #fff; }
    [data-testid="stMetricValue"] { color: #002244 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #e0ddd5; border-radius: 5px; }
    code { color: #ff0000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- ACCESS GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1><p>Tuesday, March 17, 2026</p></div>', unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        st.markdown("### 🔒 Press Credentials")
        user = st.text_input("REPORTER ID")
        key = st.text_input("ACCESS KEY", type="password")
        if st.button("AUTHENTICATE"):
            if user == "clark_kent" and key == "superman":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Access Denied.")
    st.stop()

# --- MAIN INTERFACE ---
st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1><p>WATCHTOWER OSINT & VULNERABILITY ORCHESTRATOR</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🗞️ NEWSROOM", "🗄️ EDITORIAL VAULT", "📋 TARGET QUEUE", "📡 THE NEWS-WIRE"])

with tab1:
    col1, col2 = st.columns([1,3])
    with col1:
        st.markdown("### Mission Specs")
        target = st.text_input("PRIMARY DOMAIN")
        scope = st.text_input("AUTHORIZED SCOPE")
        power = st.selectbox("INTEL LEVEL", ["passive", "active", "vuln_hunt", "nuclear"])
        if st.button("RUN INVESTIGATION"):
            if target and scope:
                console = st.empty()
                full_log = ""
                env = os.environ.copy()
                env["IN_SCOPE"] = scope
                p = subprocess.Popen(["bash", "powers.sh", power, target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                for line in iter(p.stdout.readline, ''):
                    full_log += line
                    console.code(full_log)
                    if "CRITICAL" in line.upper(): log_to_vault(target, "CRITICAL", line.strip())
                p.wait()

with tab2:
    st.markdown("### 🗄️ THE VAULT")
    conn = sqlite3.connect('daily_planet_vault.db')
    df = pd.read_sql_query("SELECT * FROM vault ORDER BY id DESC", conn)
    conn.close()
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("FINDINGS", len(df))
        m2.metric("CRITICALS", len(df[df['severity'] == 'CRITICAL']))
        m3.metric("TARGETS", df['domain'].nunique())
        st.dataframe(df, use_container_width=True)
    else: st.info("Vault empty.")

with tab3:
    st.markdown("### 📋 MASS TARGET MANAGEMENT")
    target_list = st.text_area("Domains (One per line)")
    if st.button("START QUEUED SCAN"):
        domains = [d.strip() for d in target_list.split('\n') if d.strip()]
        prog = st.progress(0)
        for i, d in enumerate(domains):
            st.write(f"Investigating {d}...")
            env = os.environ.copy(); env["IN_SCOPE"] = d
            subprocess.run(["bash", "powers.sh", "vuln_hunt", d], env=env)
            prog.progress((i + 1) / len(domains))
        st.balloons()

with tab4:
    st.markdown("### 📡 THE NEWS-WIRE")
    check_domain = st.text_input("PROBE DOMAIN FOR LEAKS")
    if st.button("QUERY BREACH DATA"):
        st.spinner("Querying OSINT databases...")
        subprocess.run(["bash", "powers.sh", "leak_check", check_domain])
        st.success("Search complete. Check Vault for updates.")
