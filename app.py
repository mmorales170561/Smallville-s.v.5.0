import streamlit as st
import subprocess
import os

# --- AUTHENTICATION STATE ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- TERMINAL STYLING ENGINE ---
st.set_page_config(page_title="ACTION_COMICS_TERMINAL", layout="wide")

st.markdown("""
    <style>
    /* Phosphor Green CRT Theme */
    .stApp { 
        background-color: #000000; 
        color: #33ff33; 
        font-family: 'Courier New', Courier, monospace;
        background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%;
    }
    
    /* Force Green Text for All Elements */
    h1, h2, h3, p, label, .stMarkdown, .stCodeBlock { color: #33ff33 !important; }
    
    /* Terminal Inputs */
    input, textarea { 
        background-color: #000 !important; 
        color: #33ff33 !important; 
        border: 1px solid #33ff33 !important;
        text-transform: uppercase;
    }
    
    /* Custom ASCII Styling */
    pre { 
        color: #33ff33 !important; 
        background-color: transparent !important; 
        border: none !important; 
        font-size: 10px !important;
        line-height: 1.1 !important;
    }
    
    /* Terminal Buttons */
    .stButton>button { 
        background-color: transparent; 
        color: #33ff33; 
        border: 1px solid #33ff33;
        border-radius: 0;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #33ff33;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# The Splash Banner
BANNER = r"""
    ___  ____________________  _   __  __________  __  __________________
   /   |/ ____/_  __/  _/ __ \/ | / / / ____/ __ \/  |/  /  _/ ____/ ___/
  / /| / /     / /  / // / / /  |/ / / /   / / / / /|_/ // // /    \__ \ 
 / ___ / /___ / / _/ // /_/ / /|  / / /___/ /_/ / /  / // // /___ ___/ / 
/_/  |_\____//_/ /___/\____/_/ |_/  \____/\____/_/  /_/___/\____//____/ 
                                                                         
"""

# --- STAGE 1: THE LOGIN TERMINAL ---
if not st.session_state['auth']:
    st.code(BANNER)
    st.write(">> [UPLINK_ESTABLISHED_METROPOLIS_HUB]")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        st.write("Password:")
    with col2:
        pwd = st.text_input("", type="password", label_visibility="collapsed", key="login_pwd")
    
    if pwd:
        if pwd == "superman":
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error(">> [ERR] INVALID_KRYPTON_KEY")
    st.stop()

# --- STAGE 2: THE RECON INTERFACE ---
st.code(BANNER)
st.write(">> WELCOME, AGENT_KENT. DAILY PLANET RECONNAISSANCE SUITE IS ONLINE.")

# Investigation Layout
c1, c2 = st.columns(2)
with c1:
    target = st.text_input(">> TARGET_HOST")
    in_scope = st.text_area(">> SET_IN_SCOPE")
with c2:
    out_scope = st.text_area(">> SET_OUT_SCOPE")

ability = st.selectbox(">> SELECT_POWER", ["Observer", "Kingpin", "Automated Hunt"])

if st.button(">> FILE_THE_STORY"):
    with st.spinner(">> [BUSY] TY
