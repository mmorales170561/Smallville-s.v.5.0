import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime

# --- DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('daily_planet_vault.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vault 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, domain TEXT, 
                  severity TEXT, finding TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def log_to_vault(domain, severity, finding):
    conn = sqlite3.connect('daily_planet_vault.db')
    c = conn.cursor()
    c.execute("INSERT INTO vault (timestamp, domain, severity, finding, status) VALUES (?,?,?,?,?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M"), domain, severity, finding, "Unreported"))
    conn.commit()
    conn.close()

# --- THE "DAILY PLANET" DESIGN SYSTEM ---
st.set_page_config(page_title="The Daily Planet | Watchtower", layout="wide")
init_db()

st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp { background-color: #fdfcf8; color: #1a1a1a; font-family: 'Georgia', serif; }
    
    /* The Masthead (Newspaper Header) */
    .masthead {
        text-align: center;
        border-top: 4px solid #002244;
        border-bottom: 2px solid #002244;
        padding: 25px 0;
        margin-bottom: 40px;
    }
    .masthead h1 {
        font-family: 'Old English Text MT', 'Times New Roman', serif;
        font-size: 64px;
        margin: 0;
        color: #002244;
        letter-spacing: -1px;
    }
    .masthead-sub {
        text-transform: uppercase;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        letter-spacing: 3px;
        color: #666;
        margin-top: 10px;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #002244 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* Modern Buttons */
    .stButton>button {
        background-color: #002244;
        color: #ffffff;
        border: 1px solid #002244;
        border-radius: 0px;
        font-family: 'Arial', sans-serif;
        text-transform: uppercase;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        border-color: #ff0000;
        color: white;
    }

    /* Cards/Sections */
    .news-card {
        background: white;
        padding: 20px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 0px #eee;
        margin-bottom: 20px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Arial Black', sans-serif;
        color: #ff0000 !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: #002244 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR STATUS ---
with st.sidebar:
    st.markdown("### 🛰️ SYSTEM STATUS")
    st.success("Watchtower: ONLINE")
    st.info("Identity Rotation: ACTIVE")
    st.warning("Storage: 2.1GB Used")
    if st.button("CLEAR LOCAL CACHE"):
        st.toast("Purging temporary binaries...")

# --- LOGIN GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown('<div class="masthead"><h1>The Daily Planet</h1><div class="masthead-sub">Security Archive & Investigation Portal</div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        st.markdown("<div class='news-card'>", unsafe_allow_html=True)
        user = st.text_input("REPORTER ID")
        key = st.text_input("ACCESS KEY", type="password")
        if st.button("SECURE LOGIN"):
            if user == "clark_kent" and key == "superman":
                st.session_state['auth'] = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- MAIN DASHBOARD ---
st.markdown('<div class="masthead"><h1>The Daily Planet</h1><div class="masthead-sub">Tuesday, March 17, 2026 | Metropolis Intelligence Framework</div></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗞️ NEWSROOM RECON", "🗄️ THE VAULT", "📋 QUEUE MANAGEMENT"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### INVESTIGATION SPECS")
        target = st.text_input("PRIMARY DOMAIN", placeholder="example.com")
        scope = st.text_input("AUTH SCOPE", placeholder="example.com")
        power = st.selectbox("INTEL LEVEL", ["passive", "active", "vuln_hunt", "nuclear"])
        if st.button("EXECUTE ASSAULT"):
            if target and scope:
                log_area = st.empty()
                full_log = ""
                env = os.environ.copy()
                env["IN_SCOPE"] = scope
                p = subprocess.Popen(["bash", "powers.sh", power, target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                for line in iter(p.stdout.readline, ''):
                    full_log += line
                    log_area.code(full_log)
                    if "CRITICAL" in line.upper(): log_to_vault(target, "CRITICAL", line.strip())
                p.wait()
    with c2:
        st.markdown("### LIVE WIRE")
        st.info("Monitor findings in the terminal to the left. Criticals are automatically moved to the Editorial Vault.")

with tab2:
    st.markdown("### 🗄️ EDITORIAL VAULT")
    conn = sqlite3.connect('daily_planet_vault.db')
    df = pd.read_sql_query("SELECT * FROM vault ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("FINDINGS", len(df))
        m2.metric("CRITICALS", len(df[df['severity'] == 'CRITICAL']))
        m3.metric("TARGETS", df['domain'].nunique())
        st.dataframe(df, use_container_width=True)
    else:
        st.info("The Vault is currently empty.")

with tab3:
    st.markdown("### 📋 BATCH ASSIGNMENTS")
    target_list = st.text_area("List Domains (One per Line)")
    if st.button("RUN BATCH INVESTIGATION"):
        domains = [d.strip() for d in target_list.split('\n') if d.strip()]
        for d in domains:
            st.write(f"Investigating {d}...")
            # Automatically uses the domain itself as the scope
            env = os.environ.copy()
            env["IN_SCOPE"] = d
            subprocess.run(["bash", "powers.sh", "vuln_hunt", d], env=env)
        st.balloons()
