import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
import time
from datetime import datetime

# --- DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ledger 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, target TEXT, 
                  threat_level TEXT, intel TEXT, duration_sec REAL)''')
    conn.commit()
    conn.close()

def log_to_ledger(target, threat, intel, duration_sec):
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    c = conn.cursor()
    c.execute("INSERT INTO ledger (timestamp, target, threat_level, intel, duration_sec) VALUES (?,?,?,?,?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M"), target, threat, intel, duration_sec))
    conn.commit()
    conn.close()

# --- THEME: KRYPTONIAN ELITE ---
st.set_page_config(page_title="Operation: Red Kryptonite | ELITE", layout="wide")
init_db()

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Courier New', monospace; }
    .welcome-hud { border-left: 5px solid #ff0000; padding: 20px; margin-bottom: 20px; background-color: #121416; }
    .welcome-hud h1 { font-family: 'Georgia', serif; font-size: 32px; color: #ffffff; margin: 0; text-transform: uppercase; }
    .sidebar-stat { background-color: #1a1a1a; border: 1px solid #444; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .stat-val { color: #ff0000; font-weight: bold; font-size: 20px; }
    .telemetry-card { background-color: #000; border: 1px solid #ff0000; padding: 15px; color: #ff0000; height: 400px; overflow-y: auto; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHORIZATION GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h2 style='text-align:center; color:#ff0000;'>KRYPTONIAN ACCESS</h2>", unsafe_allow_html=True)
        user = st.text_input("ID: clark_kent")
        pwd = st.text_input("CRYPT: superman", type="password")
        if st.button("AUTHORIZE"):
            if user == "clark_kent" and pwd == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- SIDEBAR: NEURAL CORE & ARMORY ---
with st.sidebar:
    st.markdown("### 🧠 NEURAL CORE: EFFICIENCY")
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    df_stats = pd.read_sql_query("SELECT * FROM ledger", conn)
    conn.close()
    
    if not df_stats.empty:
        total_crits = len(df_stats[df_stats['threat_level'] == 'CRITICAL'])
        total_time_min = df_stats['duration_sec'].sum() / 60
        cpm = total_crits / total_time_min if total_time_min > 0 else 0
        st.markdown(f'<div class="sidebar-stat"><p style="margin:0; font-size:12px;">HUNT VELOCITY (CPM)</p><p class="stat-val">{cpm:.2f}</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ KRYPTONIAN ARMORY")
    if st.button("PRIME ELITE WEAPONS"):
        with st.spinner("Refining Binaries..."):
            subprocess.run(["bash", "powers.sh", "prime"])
        st.success("Armory: ELITE STATUS")
    
    st.markdown("---")
    st.markdown("### 🕵️ SHADOW ARCHIVE")
    wayback = st.toggle("WAYBACK LENS", value=True)
    ports = st.toggle("GRAPPLING HOOK", value=False)

# --- MAIN HUD ---
st.markdown('<div class="welcome-hud"><h1>WELCOME SUPER//MAN</h1><p style="color:#ff0000; letter-spacing:2px;">NEURAL LINK: ELITE | STATUS: OPERATIONAL</p></div>', unsafe_allow_html=True)

t1, t2 = st.tabs(["🎯 ENGAGEMENT", "🗄️ TARGET LEDGER"])

with t1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Mission Brief")
        target = st.text_input("🎯 TARGET")
        in_scope = st.text_input("✓ IN-SCOPE", value=target.split('.')[-2] + '.' + target.split('.')[-1] if '.' in target else "")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if in_scope and in_scope in target:
                start_t = time.time()
                status_box = st.empty()
                env = os.environ.copy()
                env["IN_SCOPE"] = in_scope
                env["WAYBACK"] = "1" if wayback else "0"
                env["PORTS"] = "1" if ports else "0"
                
                p = subprocess.Popen(["bash", "powers.sh", "strike", target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                
                telemetry = ""
                for line in iter(p.stdout.readline, ''):
                    telemetry += line + "\n"
                    status_box.markdown(f'<div class="telemetry-card">{telemetry}</div>', unsafe_allow_html=True)
                    if "CRITICAL" in line.upper():
                        log_to_ledger(target, "CRITICAL", line.strip(), time.time() - start_t)
                p.wait()
            else:
                st.error("SCOPE BREACH.")

with t2:
    st.subheader("Intelligence Ledger")
    conn = sqlite3.connect('red_kryptonite_ledger.db')
    df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
    conn.close()
    # 2026 Update: stretch instead of use_container_width
    st.dataframe(df, width='stretch')
