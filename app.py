import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime
from PIL import Image

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

# --- THEME & STYLING ---
st.set_page_config(page_title="Watchtower v6 | Daily Planet", layout="wide")
init_db()

st.markdown("""
    <style>
    .stApp { background-color: #2b2d31; color: #e0e0e0; font-family: 'Georgia', serif; }
    .masthead { text-align: center; border-bottom: 2px solid #555; padding: 20px; margin-bottom: 30px; }
    .masthead h1 { font-family: 'Times New Roman', serif; font-size: 52px; color: #ffffff; margin: 0; text-transform: uppercase; }
    .report-card { background-color: #fdfcf8; color: #1a1a1a; padding: 40px; border: 1px solid #000; box-shadow: 10px 10px 0px #002244; }
    .stButton>button { background-color: #444; color: white; border-radius: 0; width: 100%; border: 1px solid #666; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000; border-color: #ff0000; }
    .status-text { font-family: 'Courier New', monospace; color: #4ade80; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        user = st.text_input("REPORTER ID")
        pwd = st.text_input("ACCESS KEY", type="password")
        if st.button("AUTHENTICATE"):
            if user == "clark_kent" and pwd == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1><p style="color:#aaa;">WATCHTOWER v6.0 | AUTONOMOUS TRIAGE</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🗞️ NEWSROOM INVESTIGATION", "🗄️ EDITORIAL VAULT"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Field Operations")
        target = st.text_input("TARGET DOMAIN", placeholder="example.com")
        scope = st.text_input("AUTHORIZED SCOPE", placeholder="example.com")
        power = st.selectbox("MISSION PROFILE", ["passive", "active", "vuln_hunt"])
        
        if st.button("LAUNCH MISSION"):
            if scope in target:
                progress_bar = st.progress(0)
                status_msg = st.empty()
                log_area = st.empty()
                
                # --- LIVE PROGRESS LOGIC ---
                phases = ["Initializing Identity Rotation...", "Verifying Scope Guard...", "Executing Reconnaissance...", "Mimicking Human Patterns...", "Finalizing Intel..."]
                
                env = os.environ.copy()
                env["IN_SCOPE"] = scope
                p = subprocess.Popen(["bash", "powers.sh", power, target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                
                phase_idx = 0
                for line in iter(p.stdout.readline, ''):
                    if "MIMIC" in line: 
                        phase_idx = min(phase_idx + 1, 4)
                        status_msg.markdown(f"**CURRENT PHASE:** <span class='status-text'>{phases[phase_idx]}</span>", unsafe_allow_html=True)
                        progress_bar.progress((phase_idx + 1) * 20)
                    
                    log_area.code(line)
                    if "CRITICAL" in line.upper():
                        log_to_vault(target, "CRITICAL", line.strip())
                p.wait()
                st.success("Mission Complete.")
            else:
                st.error("SCOPE VIOLATION: Investigation Aborted.")

with tab2:
    st.subheader("The Editorial Vault")
    conn = sqlite3.connect('daily_planet_vault.db')
    df = pd.read_sql_query("SELECT * FROM vault ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        selection = st.selectbox("Select Intelligence Finding", df['finding'].tolist())
        target_row = df[df['finding'] == selection].iloc[0]
        
        if st.button("AUTO-GENERATE POC & REPORT"):
            # --- AUTO-PoC LOGIC ENGINE ---
            finding_text = target_row['finding'].lower()
            poc_steps = "1. Deploy Watchtower Scanning Module.\n2. Interact with target host endpoints."
            
            if "xss" in finding_text:
                poc_steps = "1. Locate input parameter on endpoint.\n2. Inject `<script>alert(document.domain)</script>`.\n3. Observe execution in browser context."
            elif "sql" in finding_text:
                poc_steps = "1. Identify vulnerable parameter.\n2. Append `' OR 1=1--` to request.\n3. Observe unauthorized data return."
            elif "header" in finding_text:
                poc_steps = "1. Intercept request using Proxy.\n2. Check response for missing Security Headers (CSP, HSTS).\n
