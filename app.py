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
st.set_page_config(page_title="Watchtower v7 | Daily Planet", layout="wide")
init_db()

st.markdown("""
    <style>
    .stApp { background-color: #2b2d31; color: #e0e0e0; font-family: 'Georgia', serif; }
    .masthead { text-align: center; border-bottom: 2px solid #555; padding: 20px; margin-bottom: 30px; }
    .masthead h1 { font-family: 'Times New Roman', serif; font-size: 52px; color: #ffffff; margin: 0; text-transform: uppercase; }
    .scope-label { font-family: 'Arial'; font-weight: bold; font-size: 12px; margin-bottom: 5px; }
    .report-card { background-color: #fdfcf8; color: #1a1a1a; padding: 40px; border: 1px solid #000; box-shadow: 10px 10px 0px #002244; }
    .stButton>button { background-color: #444; color: white; border-radius: 0; width: 100%; border: 1px solid #666; font-weight: bold; }
    .stButton>button:hover { background-color: #ff0000; border-color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="masthead"><h1>THE DAILY PLANET</h1><p style="color:#aaa;">WATCHTOWER v7.0 | DUAL-GATE SCOPE CONTROL</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🗞️ NEWSROOM INVESTIGATION", "🗄️ EDITORIAL VAULT"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Field Boundaries")
        target = st.text_input("🎯 TARGET DOMAIN", placeholder="sub.example.com")
        
        st.markdown('<p class="scope-label" style="color:#4ade80;">✓ AUTHORIZED IN-SCOPE</p>', unsafe_allow_html=True)
        in_scope = st.text_input("Include (e.g., example.com)", value=target.split('.')[-2]+'.'+target.split('.')[-1] if '.' in target else "")
        
        st.markdown('<p class="scope-label" style="color:#f87171;">🛑 RESTRICTED OUT-OF-SCOPE</p>', unsafe_allow_html=True)
        out_scope = st.text_input("Exclude (e.g., dev.example.com or staging)")

        power = st.selectbox("MISSION PROFILE", ["passive", "active", "vuln_hunt"])
        
        if st.button("LAUNCH MISSION"):
            # GATE 1: Check if target is in the allowed zone
            is_allowed = in_scope and in_scope in target
            # GATE 2: Check if target hits the restricted zone
            is_restricted = out_scope and out_scope in target
            
            if is_allowed and not is_restricted:
                progress_bar = st.progress(0)
                log_area = st.empty()
                
                env = os.environ.copy()
                env["IN_SCOPE"] = in_scope
                env["OUT_SCOPE"] = out_scope
                
                p = subprocess.Popen(["bash", "powers.sh", power, target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
                
                for line in iter(p.stdout.readline, ''):
                    log_area.code(line)
                    if "CRITICAL" in line.upper():
                        log_to_vault(target, "CRITICAL", line.strip())
                p.wait()
                st.success("Mission Concluded.")
            else:
                if is_restricted:
                    st.error("🛑 MISSION ABORTED: Target identified in Restricted Out-of-Scope zone.")
                else:
                    st.error("⚠️ MISSION ABORTED: Target outside of Authorized In-Scope boundary.")

with tab2:
    st.subheader("The Editorial Vault")
    conn = sqlite3.connect('daily_planet_vault.db')
    df = pd.read_sql_query("SELECT * FROM vault ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        selection = st.selectbox("Select Intelligence Finding", df['finding'].tolist())
        target_row = df[df['finding'] == selection].iloc[0]
        
        if st.button("GENERATE POC & NEWSPAPER REPORT"):
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown(f"## 📰 EXCLUSIVE: CRISIS AT {target_row['domain'].upper()}!")
            st.markdown(f"**By Clark Kent, Daily Planet Correspondent**")
            
            st.markdown(f"""
            **METROPOLIS** — High-level digital disturbances were neutralized at `{target_row['domain']}` today. 
            The Daily Planet can confirm that the investigation was conducted strictly within authorized boundaries.
            
            "We had a clear perimeter," a Watchtower analyst stated. "Any attempts by the threat to move toward restricted zones were blocked by the Man of Steel's vigilant oversight."
            
            ---
            ### 🛠️ TECHNICAL DOSSIER (HACKERONE READY)
            **Summary:** {target_row['finding']}
            **Target Authority:** {target_row['domain']}
            **Reproduction Steps:**
            1. Initialize Watchtower module with Target: `{target_row['domain']}`.
            2. Verified that host resides within `{in_scope}` and avoids `{out_scope if out_scope else "N/A"}`.
            3. Executed `{power}` scan and identified `{target_row['severity']}` finding.
            """)
            st.markdown('</div>', unsafe_allow_html=True)
