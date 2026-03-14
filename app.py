import streamlit as st
import subprocess
import os

# --- METROPOLIS THEME ENGINE ---
st.set_page_config(page_title="The Daily Planet - Security Desk", page_icon="🗞️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f1ea; font-family: 'Courier New', Courier, monospace; }
    h1 { color: #1a1a1a; text-transform: uppercase; border-bottom: 3px double #1a1a1a; text-align: center; }
    .stButton>button { background-color: #1a1a1a; color: white; width: 100%; border-radius: 0px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🛡️ ACTION COMICS: ACCESS RESTRICTED")
    code = st.text_input("ENTER SECRET CODE", type="password")
    if code == "superman":
        u = st.text_input("IDENTITY")
        p = st.text_input("KEY", type="password")
        if u == "clarkkent" and p == "smallville":
            if st.button("AUTHORIZE"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- THE DAILY PLANET INVESTIGATION DESK ---
st.title("🗞️ THE DAILY PLANET: SECURITY DESK")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    target = st.text_input("PRIMARY TARGET DOMAIN")
    in_scope = st.text_area("IN-SCOPE ASSETS (Comma separated)")
with col2:
    out_scope = st.text_area("OUT-OF-SCOPE (DO NOT SCAN)")

power = st.selectbox("CHOOSE INVESTIGATION METHOD", ["Observer", "Kingpin", "Automated Hunt"])

if st.button("RUN DAILY PLANET INVESTIGATION"):
    with st.spinner("Clark Kent is investigating..."):
        try:
            # We pass the scope to our script as environment variables
            os.environ["IN_SCOPE"] = in_scope
            os.environ["OUT_SCOPE"] = out_scope
            
            mapping = {"Observer": "observer", "Kingpin": "kingpin", "Automated Hunt": "automated_hunt"}
            cmd = f"source ./powers.sh && {mapping[power]} {target}"
            result = subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT)
            
            st.markdown("### 📰 INVESTIGATIVE REPORT")
            st.code(result.decode('utf-8'))
        except Exception as e:
            st.error(f"LEXCORP INTERFERENCE: {str(e)}")
