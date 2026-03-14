import streamlit as st
import subprocess
import os

# --- MAINFRAME THEME ENGINE ---
st.set_page_config(page_title="DAILY_PLANET_MAINFRAME", layout="wide")

# ASCII Banner (The Daily Planet)
ASCII_BANNER = """
    ____        _ __     __    ____  __                __ 
   / __ \____ _(_) /__  / /   / __ \/ /___ _____  ____/ /_
  / / / / __ `/ / / _ \/ /   / /_/ / / __ `/ __ \/ __  / _ \\
 / /_/ / /_/ / / /  __/ /   / ____/ / /_/ / / / / /_/ /  __/
/_____/\__,_/_/_/\___/_/   /_/   /_/\__,_/_/ /_/\__,_/\___/ 
"""

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; color: #00FF00; font-family: 'Courier New', monospace; }}
    pre {{ color: #00FF00; background-color: #000; border: none; }}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{ 
        background-color: #050505; color: #00FF00; border: 1px solid #00FF00; 
    }}
    .stButton>button {{ background-color: #00FF00; color: black; font-weight: bold; border-radius: 0; }}
    </style>
    <pre>{ASCII_BANNER}</pre>
""", unsafe_allow_html=True)

# --- LOGIN GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("### >>_SYSTEM_ACCESS_RESTRICTED")
    code = st.text_input("ENTER_SECRET_FREQUENCY", type="password")
    if code == "superman":
        u = st.text_input("ID")
        p = st.text_input("KEY", type="password")
        if u == "clarkkent" and p == "smallville":
            if st.button("EXECUTE_ACCESS"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- THE TERMINAL DESK ---
st.markdown("### >>_DAILY_PLANET_RECON_OS_V5.0")
st.write(">> STATUS: METROPOLIS MAIN OFFICE | WEATHER: 72°F | REPORTING BY: CLARK KENT")

c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">>_TARGET_DOMAIN")
    in_scope = st.text_area(">>_IN_SCOPE_ASSETS")
with c2:
    out_scope = st.text_area(">>_OUT_OF_SCOPE")

mod = st.selectbox(">>_INVESTIGATION_MODULE", ["Observer", "Kingpin", "Automated Hunt"])

if st.button(">>_ENGAGE"):
    with st.spinner(">>_PROCESSING_THROUGH_PHANTOM_ZONE..."):
        try:
            os.environ["IN_SCOPE"], os.environ["OUT_SCOPE"] = in_scope, out_scope
            cmd = f"source ./powers.sh && {mod.lower().replace(' ', '_')} {target}"
            result = subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT)
            
            st.markdown("### >>_SCAN_RESULTS")
            st.code(result.decode('utf-8'))
            
            st.download_button("📥_SAVE_REPORT", result.decode('utf-8'), f"DP_Report_{target}.txt")
        except Exception as e:
            st.error(f">>_FATAL_ERROR: {str(e)}")
