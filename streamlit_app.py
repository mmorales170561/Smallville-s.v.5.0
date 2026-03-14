import streamlit as st
import subprocess
import os
from datetime import datetime

# --- SETTINGS & AUTH ---
st.set_page_config(page_title="The Daily Planet", page_icon="🗞️", layout="wide")

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- STAGE 1: LOGIN GATES ---
if not st.session_state['auth']:
    st.title("🛡️ ACTION COMICS: ACCESS RESTRICTED")
    c1 = st.text_input("ACCESS CODE", type="password")
    if c1.lower() == "superman":
        st.info("GATE 1 CLEARED. ENTER SMALLVILLE CREDENTIALS.")
        u = st.text_input("USERNAME")
        p = st.text_input("PASSWORD", type="password")
        if u.lower() == "clarkkent" and p.lower() == "smallville":
            if st.button("LOGIN"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- STAGE 2: AUTO-INSTALLER ---
if not os.path.exists("/tmp/bin/subfinder"):
    with st.status("🛠️ Provisioning Superman's Arsenal...", expanded=False):
        subprocess.run(["sh", "setup_cloud.sh"])
os.environ["PATH"] += os.pathsep + "/tmp/bin"

# --- STAGE 3: THE DAILY PLANET UI ---
st.markdown("<h1 style='text-align: center; border-bottom: 2px solid black;'>THE DAILY PLANET</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"**DATE:** {datetime.now().strftime('%B %d, %Y')}")
with col2:
    st.write("**METROPOLIS WEATHER:** 81°F | Cloudy")
with col3:
    st.write("**EDITION:** Final Alpha")

st.sidebar.header("🦸 SUPERMAN'S ABILITIES")
power = st.sidebar.selectbox("Choose Power", ["Observer", "X-Ray Vision", "Heat Vision", "Phantom Zone"])
target = st.text_input("IDENTIFY TARGET HOST", placeholder="e.g., target.com")

if st.button("ENGAGE POWER"):
    with st.spinner("Writing the front-page story..."):
        try:
            mapping = {"Observer": "observer", "X-Ray Vision": "kingpin", 
                       "Heat Vision": "heat_vision", "Phantom Zone": "automated_hunt"}
            cmd = f"source powers.sh && {mapping[power]} {target}"
            result = subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT)
            st.markdown("### 🗞️ BREAKING NEWS")
            st.caption("Written by: Clark Kent")
            st.code(result.decode('utf-8'))
        except Exception as e:
            st.error(f"LEXCORP INTERFERENCE: {str(e)}")
