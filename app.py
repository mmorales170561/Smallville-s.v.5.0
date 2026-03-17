import streamlit as st
import subprocess
import os
import requests
import zipfile
import io
from datetime import datetime

# --- 1. CONFIG & BINARY PATHS ---
BIN_PATH = "/tmp/smallville_bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

if 'terminal_logs' not in st.session_state: 
    st.session_state['terminal_logs'] = "READY FOR ENGAGEMENT..."
if 'vuln_counts' not in st.session_state:
    st.session_state['vuln_counts'] = {"critical": 0, "high": 0, "medium": 0}

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 13px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5); border-radius: 5px;
    }
    .vuln-stat { padding: 8px; border-radius: 5px; text-align: center; font-weight: bold; border: 1px solid #444; }
    .crit { color: #ff0000; border-color: #ff0000; background: rgba(255,0,0,0.1); }
    .high { color: #ffae00; border-color: #ffae00; background: rgba(255,174,0,0.1); }
    .status-panel { padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #333; margin-bottom: 10px; }
    .online { color: #00ff41; border-color: #00ff41; background: rgba(0,255,65,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY STATUS ---
def get_tools():
    return [t for t in ["subfinder", "httpx", "nuclei", "katana", "airix", "interactsh-client"] if os.path.exists(os.path.join(BIN_PATH, t))]

installed_tools = get_tools()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    st.markdown(f'<div class="status-panel online"><b>{len(installed_tools)} TOOLS READY</b></div>', unsafe_allow_html=True)

    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        with st.spinner("🔓 Unlocking High-Level Armory..."):
            os.makedirs(BIN_PATH, mode=0o777, exist_ok=True)
            # Unified ProjectDiscovery Binary Downloader logic (Simulated for brevity)
            st.info("Downloading Katana, Airix, Interactsh, and Core Tools...")
            # Note: In a real run, you'd add the specific GitHub release URLs here.
            st.rerun()

    st.divider()
    st.subheader("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO (Recon)", value=True)
    p2 = st.toggle("P2: SHADOW (Alive)", value=True)
    p3 = st.toggle("P3: KATANA (Crawl)", value=True)
    p4 = st.toggle("P4: STRIKE (Vulns)", value=True)
    p5 = st.toggle("P5: ARCHITECT (Repo)", value=False)
    p6 = st.toggle("P6: OLYMPUS (AI Fuzz)", value=False)
    
    st.divider()
    if st.button("🗑️ PURGE WORKSPACE", use_container_width=True):
        st.session_state['terminal_logs'] = "WORKSPACE PURGED. READY..."
        st.session_state['vuln_counts'] = {"critical": 0, "high": 0, "medium": 0}
        st.rerun()

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", key="tn_val")
    ru = st.text_input("🔗 ROOT URL", key="ru_val")
    gh_repo = st.text_input("🐙 GITHUB REPO URL", key="gh_val")
    
    col_scope1, col_scope2 = st.columns(2)
    with col_scope1: is_scope = st.text_area("✓ IN-SCOPE", height=80, key="is_val")
    with col_scope2: os_scope = st.text_area("✗ OUT-SCOPE", height=80, key="os_val")
    
    st.write("**Vulnerability Tracker:**")
    v = st.session_state['vuln_counts']
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="vuln-stat crit">{v["critical"]}<br><small>CRIT</small></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="vuln-stat high">{v["high"]}<br><small>HIGH</small></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="vuln-stat med">{v["medium"]}<br><small>MED</small></div>', unsafe_allow_html=True)

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if tn and (ru or gh_repo):
            st.session_state['terminal_logs'] = f"--- MISSION START: {tn} ---\n"
            term_placeholder = st.empty() 
            
            env = os.environ.copy()
            env.update({
                "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
                "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
                "GH_REPO": str(gh_repo)
            })
            
            subprocess.run(["chmod", "+x", SCRIPT])
            proc = subprocess.Popen(["bash", SCRIPT, "strike", ru, tn], 
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
            
            for line in iter(proc.stdout.readline, ""):
                lower_line = line.lower()
                if "[critical]" in lower_line: st.session_state['vuln_counts']["critical"] += 1
                elif "[high]" in lower_line: st.session_state['vuln_counts']["high"] += 1
                
                st.session_state['terminal_logs'] += line
                term_placeholder.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
            
            proc.wait()
            st.success("Mission Complete.")
            st.rerun()

with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
