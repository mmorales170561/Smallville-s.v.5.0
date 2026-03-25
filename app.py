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
    .terminal { background-color: #050505; color: #00ff00; padding: 15px; border: 1px solid #333; font-family: monospace; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; }
    code { color: #00ff00 !important; background-color: #111 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY & SCOPE ENGINE ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM STANDBY: SET ROE PARAMETERS..."
if 'target' not in st.session_state: st.session_state.target = "example.com"
if 'in_scope' not in st.session_state: st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: st.session_state.out_scope = ".gov, .mil, localhost, 127.0.0.1"

def get_bin(name):
    for r, _, f in os.walk(BIN_DIR):
        if name in f: return os.path.join(r, name)
    return None

def is_authorized(target):
    target = target.lower().strip()
    if not target: return False, "🎯 Awaiting Target Input..."
    in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
    out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
    for forbidden in out_list:
        if forbidden in target: return False, f"🛑 FORBIDDEN: Matches '{forbidden}'"
    for allowed in in_list:
        if allowed in target: return True, "✅ AUTHORIZED: Within scope."
    return False, "⚠️ BLOCKED: Not in authorized whitelist."

def fabricate_tool(tool_name, url, is_zip=False):
    try:
        with st.spinner(f"🧬 Fabricating {tool_name}..."):
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=20)
            if r.status_code != 200: 
                st.error(f"❌ 404: {tool_name}")
                return
            pkg = f"/tmp/{tool_name}_pkg"
            with open(pkg, 'wb') as f: f.write(r.content)
            if is_zip:
                with zipfile.ZipFile(pkg, 'r') as z: z.extractall(BIN_DIR)
            else:
                with tarfile.open(pkg, "r:gz") as t: t.extractall(path=BIN_DIR)
            for root, _, files in os.walk(BIN_DIR):
                for f in files:
                    if f == tool_name or (f.startswith(tool_name) and "." not in f):
                        os.chmod(os.path.join(root, f), 0o755)
            st.success(f"🔋 {tool_name} Ready.")
    except Exception as e: 
        st.error(f"⚠️ Error: {str(e)}")

# --- 3. SIDEBAR
