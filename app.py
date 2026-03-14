import streamlit as st
import subprocess
import os

# --- TERMINAL THEME ENGINE ---
st.set_page_config(page_title="Smallville Terminal", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #33ff33; font-family: 'Courier New', monospace; }
    h1, h2, h3 { color: #33ff33; text-transform: uppercase; border-bottom: 1px solid #33ff33; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: #33ff33; border: 1px solid #33ff33; }
    .stTextArea>div>div>textarea { background-color: #1a1a1a; color: #33ff33; border: 1px solid #33ff33; }
    .stButton>button { background-color: #33ff33; color: #000; border: none; font-weight: bold; }
    .terminal-output { background-color: #000; color: #33ff33; padding: 15px; border: 1px solid #33ff33; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title(">> ACCESS_RESTRICTED")
    code = st.text_input("ENTER SECRET FREQUENCY", type="password")
    if code == "superman":
        u, p = st.text_input("ID"), st.text_input("KEY", type="password")
        if u == "clarkkent" and p == "smallville":
            if st.button("EXECUTE AUTH"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- TERMINAL INTERFACE ---
st.title(">> SMALLVILLE_TERMINAL_V5.0")
st.write(">> SYSTEM: DAILY PLANET RECON DESK")

col1, col2 = st.columns(2)
with col1:
    target = st.text_input("TARGET_HOST")
    in_scope = st.text_area("IN_SCOPE")
with col2:
    out_scope = st.text_area("OUT_SCOPE")

power = st.selectbox("SELECT_MODULE", ["Observer", "Kingpin", "Automated Hunt"])

if st.button("RUN_INVESTIGATION"):
    with st.spinner(">> INITIALIZING KRYPTONIAN_ARBITRATION..."):
        try:
            os.environ["IN_SCOPE"], os.environ["OUT_SCOPE"] = in_scope, out_scope
            cmd = f"source ./powers.sh && {power.lower().replace(' ', '_')} {target}"
            result = subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT)
            
            st.markdown("### >> OUTPUT_STREAM")
            st.code(result.decode('utf-8'), language='bash')
            
            st.download_button("📥 EXPORT_LOG", result.decode('utf-8'), f"report_{target}.txt")
        except Exception as e:
            st.error(f">> ERROR: {str(e)}")
