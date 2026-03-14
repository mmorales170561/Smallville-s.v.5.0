import streamlit as st
import subprocess
import os
from datetime import datetime

# --- NEWSPAPER THEME ENGINE ---
st.set_page_config(page_title="The Daily Planet", page_icon="🗞️", layout="wide")

# Custom CSS for 1940s Vintage Aesthetic
st.markdown("""
    <style>
    /* Newsprint Background */
    .stApp {
        background-color: #f4f1ea;
        background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
    }
    
    /* Vintage Typography */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        text-transform: uppercase;
        color: #1a1a1a;
        border-bottom: 2px solid #1a1a1a;
        text-align: center;
    }
    
    .stButton>button {
        background-color: #1a1a1a;
        color: #f4f1ea;
        border: none;
        font-weight: bold;
    }

    /* Newspaper Article Box */
    .article-box {
        background-color: #fff;
        padding: 20px;
        border: 1px solid #ccc;
        box-shadow: 5px 5px 0px #1a1a1a;
        font-family: 'Courier New', Courier, monospace;
        color: #333;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- AUTHENTICATION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h1>🛡️ Action Comics #1: Access Restricted</h1>", unsafe_allow_html=True)
    gate = st.text_input("ENTER SECRET FREQUENCY", type="password")
    if gate.lower() == "superman":
        st.info("Kryptonian Signature Detected.")
        u, p = st.text_input("USERNAME"), st.text_input("PASSWORD", type="password")
        if u.lower() == "clarkkent" and p.lower() == "smallville":
            if st.button("FILE THE STORY"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- CLOUD SETUP ---
if not os.path.exists("/tmp/bin/subfinder"):
    with st.status("🛠️ Calibrating X-Ray Vision..."):
        subprocess.run(["sh", "setup_cloud.sh"])
os.environ["PATH"] += os.pathsep + "/tmp/bin"

# --- MAIN DASHBOARD ---
st.markdown("<h1>THE DAILY PLANET</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.write(f"**DATE:** {datetime.now().strftime('%B %d, %Y')}")
c2.write("**LOCATION:** Metropolis (Bakersfield)")
c3.write("**PRICE:** TWO CENTS")

st.sidebar.header("🦸 SUPERMAN'S ABILITIES")
power = st.sidebar.selectbox("Choose Power", ["Observer", "X-Ray Vision", "Heat Vision", "Phantom Zone"])
target = st.text_input("IDENTIFY TARGET HOST", placeholder="e.g., target.com")

if st.button("ENGAGE POWER"):
    with st.spinner("Clark Kent is typing..."):
        try:
            mapping = {"Observer": "observer", "X-Ray Vision": "kingpin", 
                       "Heat Vision": "heat_vision", "Phantom Zone": "automated_hunt"}
            cmd = f"source powers.sh && {mapping[power]} {target}"
            result = subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT)
            
            # Render output inside the "Article Box"
            st.markdown(f"""
            <div class="article-box">
                <h2>BREAKING NEWS: {power.upper()} ACTIVE</h2>
                <p><i>Written by: Clark Kent, Chief Investigative Reporter</i></p>
                <hr>
                <pre style="white-space: pre-wrap; color: #1a1a1a;">{result.decode('utf-8')}</pre>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"LEXCORP INTERFERENCE: {str(e)}")
