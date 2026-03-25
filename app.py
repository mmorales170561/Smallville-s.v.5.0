import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil

# --- 1. HUD CONFIGURATION ---
st.set_page_config(page_title="RUBY-OPERATOR v2.8", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff3131; }
    .stButton>button { background-color: #ff3131; color: #000; border: none; font-weight: bold; border-radius: 0px; }
    .stTextInput>div>div>input { background-color: #111; color: #ff3131; border: 1px solid #444; }
    .terminal { background-color: #050505; color: #00ff00; padding: 15px; border: 1px solid #333; font-family: monospace; height: 300px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; }
    .scope-box { padding: 10px; border: 1px solid #444; margin-bottom: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL STATE & SCOPE ENGINE ---
if 'last_log' not in st.session_state: st.session_state.last_log = "GUARDRAILS ACTIVE..."
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com, target-api.io"
if 'out_scope' not in st.session_state: st.session_state.out_scope = "google.com, facebook.com, .gov, .mil"

def is_authorized(target):
    """Safety check: Returns True only if target is in-scope and NOT out-of-scope."""
    target = target.lower().strip()
    in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",")]
    out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",")]
    
    # Check Out-of-Scope first (Blacklist)
    for forbidden in out_list:
        if forbidden and forbidden in target:
            return False, f"🛑 TARGET IS FORBIDDEN: Matches blacklisted pattern '{forbidden}'"
            
    # Check In-Scope (Whitelist)
    for allowed in in_list:
        if allowed and allowed in target:
            return True, "✅ Target authorized."
            
    return False, "⚠️ TARGET IS OUT OF SCOPE: Not found in authorized list."

# --- 3. THE MISSION CONTROL ---
tabs = st.tabs(["🛡️ ENGAGEMENT ROE", "🚀 STRIKE OPS", "📊 INTELLIGENCE"])

with tabs[0]: # RULES OF ENGAGEMENT
    st.header("📋 RULES OF ENGAGEMENT (ROE)")
    st.info("Define your legal boundaries here. The system will block any strikes outside these parameters.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🟢 IN-SCOPE (Whitelist)")
        st.session_state.in_scope = st.text_area("Authorized Domains/IPs (comma separated)", st.session_state.in_scope, height=150)
        
    with col2:
        st.subheader("🔴 OUT-OF-SCOPE (Blacklist)")
        st.session_state.out_scope = st.text_area("Forbidden Patterns (e.g. .gov, specific IPs)", st.session_state.out_scope, height=150)

with tabs[1]: # STRIKE OPS
    st.header("🔫 RED KRYPTONITE GUN")
    target_input = st.text_input("🎯 TARGET SECTOR", "example.com")
    
    # Live Scope Validation
    auth_status, auth_msg = is_authorized(target_input)
    if auth_status:
        st.success(auth_msg)
        
        c1, c2, c3 = st.columns(3)
        # (Subfinder, Nuclei, and Katana logic goes here, wrapped in the auth_status check)
        with c1:
            if st.button("🔥 GHOST: SUBFINDER"):
                # Proceed with scan...
                st.session_state.last_log = f"Firing Subfinder at {target_input}..."
    else:
        st.error(auth_msg)
        st.warning("Firing Pin Locked. Adjust ROE to proceed.")

# --- 4. HUD / TERMINAL ---
st.divider()
st.subheader("📟 LIVE TERMINAL")
st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
