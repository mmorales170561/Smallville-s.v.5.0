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

# --- THEME & STYLING ---
st.set_page_config(page_title="Watchtower v8 | Daily Planet", layout="wide")
init_db()

st.markdown("""
    <style>
    .stApp { background-color: #2b2d31; color: #e0e0e0; font-family: 'Georgia', serif; }
    .masthead { text-align: center; border-bottom: 2px solid #555; padding: 20px; margin-bottom: 30px; }
    .masthead h1 { font-family: 'Times New Roman', serif; font-size: 52px; color: #ffffff; margin: 0; text-transform: uppercase; }
    .telemetry-card { background-color: #1a1b1e; border: 1px solid #4ade80; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; color: #4ade80; height: 300px; overflow-y: auto; }
    .stButton>button { background-color: #444; color: white; border-radius: 0; width: 100%; border: 1px solid #666; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000; border-color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN GATE (SIMPLIFIED) ---
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

st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1><p style="color:#aaa;">WATCHTOWER v8.0 | LIVE TELEMETRY FEED</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🗞️ NEWSROOM INVESTIGATION", "🗄️ EDITORIAL VAULT"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Field Parameters")
        target = st.text_input("🎯 TARGET DOMAIN")
        in_scope = st.text_input("✓ IN-SCOPE", value=target.split('.')[-2]+'.'+target.split('.')[-1] if '.' in target else "")
        out_scope = st.text_input("🛑 OUT-OF-SCOPE")
        power = st.selectbox("MISSION PROFILE", ["passive", "active", "vuln_hunt"])
        
        if st.button("LAUNCH MISSION"):
            if in_scope and in_scope in target and (not out_scope or out_scope not in target):
                st.session_state['telemetry'] = ">> INITIALIZING UPLINK...\n"
                telemetry_box = st.empty()
                log_area = st.empty()
                
                env = os.environ.copy()
                env["IN_SCOPE"] = in_scope
                env["OUT_SCOPE"] = out_scope
                
                p = subprocess.Popen(["bash", "powers.sh", power, target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                
                # Real-time Telemetry Loop
                full_log = ""
                for line in iter(p.stdout.readline, ''):
                    # We look for the ">>" prefix in our bash script to update the Telemetry box
                    if ">>" in line:
                        st.session_state['telemetry'] += line
                        telemetry_box.markdown(f'<div class="telemetry-card">{st.session_state["telemetry"]}</div>', unsafe_allow_html=True)
                    else:
                        full_log += line
                        log_area.code(full_log)
                    
                    if "CRITICAL" in line.upper():
                        log_to_vault(target, "CRITICAL", line.strip())
                p.wait()
            else:
                st.error("SCOPE BREACH DETECTED: MISSION ABORTED")

with tab2:
    st.subheader("The Editorial Vault")
    conn = sqlite3.connect('daily_planet_vault.db')
    df = pd.read_sql_query("SELECT * FROM vault ORDER BY id DESC", conn)
    conn.close()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
