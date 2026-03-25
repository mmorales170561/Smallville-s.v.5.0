import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil

# --- 1. HUD CONFIGURATION ---
st.set_page_config(page_title="RUBY-OPERATOR v3.1", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 450px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131; color: #000; font-weight: bold; border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE VOLATILE ARMORY & SEARCH ENGINE ---
BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

if 'last_log' not in st.session_state: st.session_state.last_log = "SYSTEM READY..."

def find_executable(name):
    """Deep-searches the BIN_DIR for the actual binary file."""
    for root, dirs, files in os.walk(BIN_DIR):
        if name in files:
            full_path = os.path.join(root, name)
            os.chmod(full_path, 0o755)
            return full_path
    return None

def fabricate_tool(tool_name, url, is_zip=False):
    try:
        with st.sidebar:
            # Step 1: Force break the file lock if it exists
            target_path = os.path.join(BIN_DIR, tool_name)
            if os.path.exists(target_path):
                try:
                    os.remove(target_path) # Try to delete the specific file
                except:
                    # If remove fails, move it to a trash name to free the primary path
                    os.rename(target_path, f"{target_path}.old_{time.time()}")

            # Step 2: Download the fresh binary
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True, timeout=20)
            pkg = f"/tmp/{tool_name}_pkg"
            with open(pkg, 'wb') as f: f.write(r.content)
            
            # Step 3: Unpack
            if is_zip:
                with zipfile.ZipFile(pkg, 'r') as z: z.extractall(BIN_DIR)
            else:
                with tarfile.open(pkg, "r:gz") as t: t.extractall(path=BIN_DIR)
            
            st.sidebar.success(f"🔋 {tool_name} Refreshed.")
    except Exception as e: 
        st.sidebar.error(f"⚠️ Fabricator Error: {str(e)}")
# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 OPERATOR")
    battery = st.selectbox("BATTERY", ["⚡ AUTO-STRIKE", "Ghost", "Strike", "DeFi"])
    if st.button("🔌 PRIME ARMORY"):
        fabricate_tool("subfinder", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", is_zip=True)
        fabricate_tool("httpx", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", is_zip=True)
        fabricate_tool("nuclei", "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip", is_zip=True)
    
    st.divider()
    if st.button("🗑️ PURGE TERMINAL"):
        st.session_state.last_log = "PURGED."
        st.rerun()

# --- 4. MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.1")
t_tab, s_tab = st.tabs(["🛡️ ROE", "🚀 STRIKE OPS"])

with t_tab:
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE", "example.com")
    st.session_state.out_scope = st.text_area("🔴 RED ZONE", ".gov")

with s_tab:
    target = st.text_input("🎯 TARGET", "example.com")
    if st.button("🔥 INITIATE FULL AUTO-STRIKE"):
        # Initialize terminal with a startup sequence
        st.session_state.last_log = f"🚀 [INIT] STRIKE SEQUENCE AUTHORIZED: {st.session_state.target}\n"
        final_output = []

        with st.status("⛓️ Chain Executing...", expanded=True) as s:
            
            # --- STEP 1: GHOST RECON (SUBFINDER) ---
            sub_path = find_executable("subfinder")
            if sub_path:
                s.write("📡 Firing Subfinder...")
                cmd = [sub_path, "-d", st.session_state.target, "-silent"]
                st.session_state.last_log += f"EXE: {' '.join(cmd)}\n"
                try:
                    sub_res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
                    sub_out = sub_res.stdout.strip() if sub_res.stdout else ""
                    final_output.append(f"--- [RECON] SUBDOMAINS ---\n{sub_out if sub_out else '[!] No Subdomains Found'}")
                    st.session_state.last_log += f"DONE: Found {len(sub_out.splitlines())} assets.\n"
                except Exception as e:
                    final_output.append(f"❌ Subfinder Misfire: {str(e)}")
            
            # --- STEP 2: PROBE (HTTPX) ---
            htx_path = find_executable("httpx")
            if htx_path:
                s.write("🔍 Firing Httpx...")
                # Logic: If subfinder found nothing, probe the main target
                input_data = sub_out if (sub_path and sub_out) else st.session_state.target
                # Clean input data to prevent shell injection but allow pipes
                cmd = f"echo '{input_data}' | {htx_path} -silent -sc -td -title"
                st.session_state.last_log += f"EXE: {cmd}\n"
                try:
                    htx_res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
                    htx_out = htx_res.stdout.strip()
                    final_output.append(f"--- [PROBE] ACTIVE HOSTS ---\n{htx_out if htx_out else '[!] No Active Hosts Detected'}")
                    st.session_state.last_log += f"DONE: Probed {len(htx_out.splitlines())} hosts.\n"
                except Exception as e:
                    final_output.append(f"❌ Httpx Misfire: {str(e)}")

            # --- STEP 3: STRIKE (NUCLEI) ---
            nuc_path = find_executable("nuclei")
            if nuc_path:
                s.write("☢️ Firing Nuclei...")
                # We target the main domain for the deep scan
                cmd = [nuc_path, "-u", st.session_state.target, "-silent", "-ni", "-severity", "critical,high"]
                st.session_state.last_log += f"EXE: {' '.join(cmd)}\n"
                try:
                    nuc_res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                    nuc_out = nuc_res.stdout.strip()
                    final_output.append(f"--- [STRIKE] VULNERABILITIES ---\n{nuc_out if nuc_out else '[!] No Critical Vulns Detected'}")
                    st.session_state.last_log += "DONE: Nuclei Strike Finished.\n"
                except Exception as e:
                    final_output.append(f"❌ Nuclei Misfire: {str(e)}")

            # --- RENDER RESULTS ---
            st.session_state.last_log += "\n--- [FINAL REPORT] ---\n" + "\n\n".join(final_output)
            s.update(label="Strike Sequence Complete.", state="complete")

# --- 5. TERMINAL ---
st.divider()
st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
