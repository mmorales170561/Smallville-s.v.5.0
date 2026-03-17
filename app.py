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
                  severity TEXT, finding TEXT, reporter TEXT)''')
    conn.commit()
    conn.close()

def log_to_vault(domain, severity, finding):
    conn = sqlite3.connect('daily_planet_vault.db')
    c = conn.cursor()
    c.execute("INSERT INTO vault (timestamp, domain, severity, finding, reporter) VALUES (?,?,?,?,?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M"), domain, severity, finding, "Clark Kent"))
    conn.commit()
    conn.close()

# --- THEME: SLATE GREY & NEWSROOM ---
st.set_page_config(page_title="Watchtower | Daily Planet", layout="wide")
init_db()

st.markdown("""
    <style>
    /* Dark Slate Background */
    .stApp { background-color: #2b2d31; color: #e0e0e0; font-family: 'Georgia', serif; }
    
    /* Newspaper Masthead */
    .masthead {
        text-align: center; border-bottom: 2px solid #555; padding: 20px; margin-bottom: 30px;
    }
    .masthead h1 { font-family: 'Times New Roman', serif; font-size: 52px; color: #ffffff; margin: 0; }
    
    /* Scope Status Indicators */
    .scope-box { padding: 10px; border-radius: 5px; margin-bottom: 10px; font-weight: bold; }
    .in-scope { background-color: #1e3a1e; color: #4ade80; border: 1px solid #4ade80; }
    .out-scope { background-color: #3a1e1e; color: #f87171; border: 1px solid #f87171; }

    /* Inputs & Buttons */
    .stButton>button { background-color: #444; color: white; border: 1px solid #666; border-radius: 0; width: 100%; }
    .stButton>button:hover { background-color: #ff0000; color: white; border-color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        user = st.text_input("REPORTER ID")
        pwd = st.text_input("ACCESS KEY", type="password")
        if st.button("LOG IN"):
            if user == "clark_kent" and pwd == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- MAIN INTERFACE ---
st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1><p style="color:#aaa;">METROPOLIS BUREAU | WATCHTOWER v4.0</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🗞️ NEWSROOM INVESTIGATION", "🗄️ EDITORIAL VAULT"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Field Ops")
        target = st.text_input("TARGET DOMAIN")
        scope = st.text_input("AUTHORIZED SCOPE")
        power = st.selectbox("INTEL LEVEL", ["passive", "active", "vuln_hunt"])
        
        # Real-time Scope Visualizer
        if target and scope:
            if scope in target:
                st.markdown('<div class="scope-box in-scope">✓ TARGET IS IN-SCOPE</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="scope-box out-scope">⚠ WARNING: TARGET OUTSIDE SCOPE</div>', unsafe_allow_html=True)

        if st.button("START INVESTIGATION"):
            log_area = st.empty()
            env = os.environ.copy()
            env["IN_SCOPE"] = scope
            p = subprocess.Popen(["bash", "powers.sh", power, target], 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
            for line in iter(p.stdout.readline, ''):
                log_area.code(line)
                if "CRITICAL" in line.upper(): log_to_vault(target, "CRITICAL", line.strip())
            p.wait()

with tab2:
    st.subheader("The Vault")
    conn = sqlite3.connect('daily_planet_vault.db')
    df = pd.read_sql_query("SELECT * FROM vault ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        selection = st.selectbox("Select finding to generate Press Report", df['finding'].tolist())
        target_row = df[df['finding'] == selection].iloc[0]
        
        # --- THE SUPERMAN NEWSPAPER REPORT ENGINE ---
        st.markdown("---")
        st.markdown(f"## 📰 EXCLUSIVE: CRISIS AT {target_row['domain'].upper()}!")
        st.markdown(f"**By Clark Kent, Daily Planet Correspondent** | *{target_row['timestamp']}*")
        
        newspaper_report = f"""
        **METROPOLIS** — Citizens looked to the sky today as a new threat emerged from the digital shadows of {target_row['domain']}. 
        Eyewitnesses report that a technical anomaly, identified by Watchtower as a `{target_row['severity']}` event, 
        attempted to breach the city's defenses. 
        
        "It was like Kryptonite for their servers," said one technician. "Without the Man of Steel's intervention, the data would have been lost."
        Fortunately, Superman arrived on the scene, utilizing his heat vision to cauterize the leak and stabilize the mainframe. 
        
        While the city sleeps soundly tonight, the Daily Planet has obtained the technical dossier of the battle.
        
        ---
        ### 🛠️ TECHNICAL ADVISORY (HACKERONE FORMAT)
        **Title:** {target_row['severity']} - {target_row['finding'].split(' ')[0]} on {target_row['domain']}
        **Summary:** A vulnerability was discovered during a routine investigation of {target_row['domain']}. 
        **Steps to Reproduce:**
        1. Navigate to the affected endpoint on `{target_row['domain']}`.
        2. Observed Behavior: `{target_row['finding']}`.
        **Impact:** Unauthorized data exposure or system compromise.
        **Suggested Fix:** Sanitize all user inputs and enforce strict CORS policies.
        """
        st.markdown(newspaper_report)
        st.download_button("Download Official Report", newspaper_report)
    else:
        st.info("No findings in the Vault yet.")
