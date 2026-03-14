import streamlit as st
import subprocess
import os

# --- CLI THEME & NOVELIZATION ENGINE ---
st.set_page_config(page_title="DAILY_PLANET_CLI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #33ff33; font-family: 'Courier New', monospace; }
    h1, h2 { color: #33ff33; border-bottom: 1px solid #33ff33; padding-bottom: 10px; }
    .stTextInput>div>div>input { background-color: #0d0d0d; color: #33ff33; border: 1px solid #33ff33; }
    .stTextArea>div>div>textarea { background-color: #0d0d0d; color: #33ff33; border: 1px solid #33ff33; }
    .stButton>button { background-color: #33ff33; color: #000; border: none; font-weight: bold; }
    .narrative-box { border: 1px solid #33ff33; padding: 15px; margin-bottom: 20px; color: #00ff00; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN: ACTION COMICS GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.title(">> SYSTEM_ACCESS_RESTRICTED")
    st.markdown("### 🗞️ METROPOLIS_TERMINAL_V1.0")
    code = st.text_input("ENTER_SECRET_FREQUENCY", type="password")
    if code == "superman":
        u, p = st.text_input("ID"), st.text_input("KEY", type="password")
        if u == "clarkkent" and p == "smallville":
            if st.button("EXECUTE_AUTH"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- MAIN TERMINAL: DAILY PLANET DESK ---
st.title(">> DAILY_PLANET_NEWSROOM_TERMINAL")
st.markdown("<div class='narrative-box'>Status: Reporting live from Metropolis, CA. Bakersfield weather check: 72°F | Clear skies for aerial recon. Perry White is waiting for this story.</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    target = st.text_input(">> TARGET_HOST")
    in_scope = st.text_area(">> IN_SCOPE_ASSETS")
with col2:
    out_scope = st.text_area(">> OUT_OF_SCOPE")

module = st.selectbox(">> SELECT_INVESTIGATION_POWER", ["Observer", "Kingpin", "Automated Hunt"])

if st.button(">> EXECUTE_RECON"):
    with st.spinner(">> CLARK_KENT_TYPING..."):
        try:
            # Pass scope to environment
            os.environ["IN_SCOPE"], os.environ["OUT_SCOPE"] = in_scope, out_scope
            cmd = f"source ./powers.sh && {module.lower().replace(' ', '_')} {target}"
            result = subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT)
            
            st.markdown("### >>_INVESTIGATIVE_REPORT_FILE")
            st.code(result.decode('utf-8'), language='bash')
            st.download_button("📥_EXPORT_ARTICLE", result.decode('utf-8'), f"Daily_Planet_{target}.txt")
        except Exception as e:
            st.error(f">> ERROR: {str(e)}")
