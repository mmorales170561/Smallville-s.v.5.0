import streamlit as st
import subprocess
import os
import sqlite3
import pandas as pd
from datetime import datetime

# --- 2026 PATH & ENVIRONMENT ---
if "/tmp/bin" not in os.environ["PATH"]:
    os.environ["PATH"] = "/tmp/bin" + os.pathsep + os.environ["PATH"]

# --- THEME: KRYPTONIAN TERMINAL ---
st.set_page_config(page_title="Operation: Red Kryptonite", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 500px; overflow-y: auto;
    }
    .stButton>button { background-color: #ff0000; color: black; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHORIZATION GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<h2 style='text-align:center; color:#ff0000;'>KRYPTONIAN ACCESS</h2>", unsafe_allow_html=True)
        u = st.text_input("ID")
        p = st.text_input("CRYPT", type="password")
        if st.button("AUTHORIZE"):
            if u == "clark_kent" and p == "superman":
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛠️ KRYPTONIAN ARMORY")
    if st.button("PRIME ELITE WEAPONS"):
        with st.spinner("RELOADING..."):
            subprocess.run(["bash", "powers.sh", "prime"], capture_output=True)
        st.success("Armory Status: ELITE")
    
    st.markdown("---")
    p2 = st.toggle("PHASE 2: WAYBACK LENS", value=True)
    p3 = st.toggle("PHASE 3: GRAPPLING HOOK", value=True)
    auto_purge = st.toggle("AUTO-PURGE (>7 Days)", value=True)

# --- MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
t1, t2, t3 = st.tabs(["🎯 ENGAGEMENT", "🗄️ LEDGER", "🖼️ GALLERY"])

with t1:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.subheader("Mission Brief")
        target = st.text_input("🎯 ROOT TARGET (Seed)")
        in_scope = st.text_area("✓ IN-SCOPE (List)")
        out_scope = st.text_input("✗ OUT-OF-SCOPE")
        
        if st.button("FIRE RED KRYPTONITE GUN"):
            if target or in_scope:
                terminal = st.empty()
                strike_env = os.environ.copy()
                strike_env.update({
                    "IN_SCOPE": str(in_scope), "OUT_SCOPE": str(out_scope),
                    "WAYBACK": "1" if p2 else "0", "PORTS": "1" if p3 else "0"
                })
                p = subprocess.Popen(["bash", "powers.sh", "strike", target], 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=strike_env)
                output = ""
                for line in iter(p.stdout.readline, ''):
                    output += line
                    terminal.markdown(f'<div class="terminal-box">{output}</div>', unsafe_allow_html=True)
                p.wait()
                st.rerun() # Refresh to update Ledger/Gallery
            else:
                st.error("TARGET REQUIRED.")

with t2:
    st.subheader("🗄️ MISSION INTELLIGENCE LEDGER")
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df = pd.read_sql_query("SELECT * FROM ledger ORDER BY id DESC", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 DOWNLOAD CSV", data=csv, file_name="mission_report.csv", mime='text/csv')
            if st.button("PURGE ALL LOGS"):
                conn = sqlite3.connect('red_kryptonite_ledger.db')
                conn.execute("DELETE FROM ledger"); conn.commit(); conn.close()
                st.rerun()
        else: st.info("Ledger is currently empty.")
    except: st.info("Initializing Intelligence Ledger...")

with t3:
    st.subheader("🖼️ RECON GALLERY")
    try:
        conn = sqlite3.connect('red_kryptonite_ledger.db')
        df_gal = pd.read_sql_query("SELECT DISTINCT target FROM ledger", conn)
        conn.close()
        if not df_gal.empty:
            cols = st.columns(4)
            for idx, row in df_gal.iterrows():
                with cols[idx % 4]:
                    # Using a 2026-stable favicon/preview API for the gallery
                    st.image(f"https://www.google.com/s2/favicons?domain={row['target']}&sz=128")
                    st.caption(f"Asset: {row['target']}")
        else: st.info("Gallery will populate after a successful strike.")
    except: st.info("Awaiting Recon Data...")
