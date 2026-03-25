import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time

# --- 1. GLOBAL STATE INITIALIZATION (CRITICAL: MUST BE FIRST) ---
if 'target' not in st.session_state: 
    st.session_state.target = "example.com"
if 'last_log' not in st.session_state: 
    st.session_state.last_log = "SYSTEM READY: AWAITING ORDERS..."
if 'in_scope' not in st.session_state: 
    st.session_state.in_scope = "example.com"
if 'out_scope' not in st.session_state: 
    st.session_state.out_scope = ".gov, .mil, localhost"

# --- 2. HUD CONFIGURATION ---
st.set_page_config(page_title="RUBY-OPERATOR v3.2", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 450px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE VOLATILE ARMORY ENGINE ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

def find_executable(name):
    """Deep-searches for the binary file."""
    for root, dirs, files in os.walk(BIN_DIR):
        if name in files:
            full_path = os.path.join(root, name)
            os.chmod(full_path, 0o755)
            return full_path
    return None

def fabricate_tool(tool_name, url, is_zip=False):
    try:
        with st.sidebar:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=20)
            pkg = f"/tmp/{tool_name}_pkg"
            with open(pkg, 'wb') as f: f.write(r.content)
            if is_zip:
                with zipfile.ZipFile(pkg, 'r') as z: z.extractall(BIN_DIR)
            else:
                with tarfile.open(pkg, "r:gz") as t: t.extractall(path=BIN_DIR)
            st.sidebar.success(f"🔋 {tool_name} Online.")
    except Exception as e: st.sidebar.error(f"⚠️ Error: {str(e)}")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔴 OPERATOR")
    battery = st.selectbox("TACTICAL BATTERY", ["⚡ AUTO-STRIKE", "Ghost", "Strike", "DeFi"])
    if st.button("🔌 PRIME ARMORY"):
        fabricate_tool("subfinder", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", is_zip=True)
        fabricate_tool("httpx", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", is_zip=True)
        fabricate_tool("nuclei", "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip", is_zip=True)
    
    st.divider()
    if st.button("🗑️ PURGE TERMINAL"):
        st.session_state.last_log = "TERMINAL PURGED."
        st.rerun()

# --- 5. MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.1")
t_tab, s_tab = st.tabs(["🛡️ ROE", "🚀 STRIKE OPS"])

with t_tab:
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE", st.session_state.in_scope)
    st.session_state.out_scope = st.text_area("🔴 RED ZONE", st.session_state.out_scope)

with s_tab:
    # Use a safe .get() method to prevent the AttributeError
    target = st.text_input("🎯 TARGET", st.session_state.get('target', 'example.com'))
    st.session_state.target = target # Update the state
    
    if st.button("🔥 INITIATE FULL AUTO-STRIKE"):
        st.session_state.last_log = f"🚀 [INIT] STRIKE SEQUENCE AUTHORIZED: {st.session_state.target}\n"
        final_output = []
        
        with st.status("⛓️ Chain Executing...", expanded=True) as s:
            # GHOST RECON
            sub_path = find_executable("subfinder")
            if sub_path:
                s.write("📡 Firing Subfinder...")
                cmd = [sub_path, "-d", st.session_state.target, "-silent"]
                st.session_state.last_log += f"EXE: {' '.join(cmd)}\n"
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
                sub_out = res.stdout.strip() if res.stdout else ""
                final_output.append(f"--- [RECON] SUBDOMAINS ---\n{sub_out if sub_out else '[!] No Subdomains'}")
            
            # PROBE
            htx_path = find_executable("httpx")
            if htx_path:
                s.write("🔍 Firing Httpx...")
                input_data = sub_out if (sub_path and sub_out) else st.session_state.target
                cmd = f"echo '{input_data}' | {htx_path} -silent -sc -td -title"
                st.session_state.last_log += f"EXE: {cmd}\n"
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
                final_output.append(f"--- [PROBE] ACTIVE ---\n{res.stdout if res.stdout else '[!] No Hosts'}")

            # STRIKE
            # --- STEP 3: STRIKE (NUCLEI) ---
            nuc_path = find_executable("nuclei")
            if nuc_path:
                s.write("☢️ Firing Nuclei (Deep Scan)...")
                # -rl 5: Only 5 requests per second (prevents timeouts)
                # -concurrency 5: Low parallel tasks
                cmd = [nuc_path, "-u", st.session_state.target, "-silent", "-ni", "-rl", "5", "-c", "5", "-severity", "critical,high"]
                st.session_state.last_log += f"EXE: {' '.join(cmd)}\n"
                
                try:
                    # Increased timeout to 300s
                    res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    nuc_out = res.stdout.strip()
                    final_output.append(f"--- [STRIKE] VULNS ---\n{nuc_out if nuc_out else '[!] No Vulns'}")
                except subprocess.TimeoutExpired as e:
                    # Capture partial output if available
                    partial = e.stdout.decode() if e.stdout else "No partial data."
                    final_output.append(f"⚠️ STRIKE TIMEOUT: Scan exceeded 5m.\nPARTIAL RESULTS:\n{partial}")
                except Exception as e:
                    final_output.append(f"❌ Nuclei Error: {str(e)}")

# --- 6. TERMINAL ---
st.divider()
st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
