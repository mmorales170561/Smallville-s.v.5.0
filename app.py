import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
import time
from datetime import datetime

# --- 1. SAFE PDF IMPORT ---
PDF_ENABLED = False
try:
    from fpdf import FPDF
    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False

# --- 2. GLOBAL STATE INITIALIZATION ---
INITIAL_STATE = {
    'target': "example.com",
    'last_log': "SYSTEM ONLINE. AWAITING COMMANDS...",
    'in_scope': "example.com",
    'out_scope': ".gov, .mil, localhost",
    'battery_type': "Web2",
    'scan_results': []
}

for key, val in INITIAL_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 3. HUD CONFIGURATION ---
st.set_page_config(page_title="RUBY-OPERATOR v5.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 500px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    .stButton>button:hover { background-color: #ff5555 !important; }
    .status-ready { color: #00ff00; font-weight: bold; }
    .status-missing { color: #555; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 4. THE ARSENAL REGISTRY ---
ARSENAL = {
    "RECON": ["subfinder", "amass", "httpx", "waybackurls", "gau", "assetfinder"],
    "WEB/FUZZ": ["ffuf", "arjun", "katana", "dalfox", "dirsearch"],
    "EXPLOIT": ["nuclei", "sqlmap", "commix", "tplimap"],
    "AI/SECRETS": ["trufflehog", "gitleaks", "garak", "pyrit"]
}

TOOL_URLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.3/nuclei_3.2.3_linux_amd64.zip",
    "waybackurls": "https://github.com/tomnomnom/waybackurls/releases/download/v0.1.0/waybackurls-linux-amd64.tgz",
    "gau": "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz",
    "amass": "https://github.com/owasp-amass/amass/releases/download/v4.2.0/amass_linux_amd64.zip",
    "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
    "trufflehog": "https://github.com/trufflesecurity/trufflehog/releases/download/v3.63.11/trufflehog_3.63.11_linux_amd64.tar.gz",
    "sqlmap": "https://github.com/sqlmapproject/sqlmap/tarball/master",
    "gitleaks": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.2/gitleaks_8.18.2_linux_x64.tar.gz"
}

# --- 5. CORE ENGINES ---
def find_exe(name):
    for root, _, files in os.walk(BIN_DIR):
        if name in files:
            p = os.path.join(root, name)
            os.chmod(p, 0o755)
            return p
    return shutil.which(name)

def fabricate_core(tool_name):
    if tool_name not in TOOL_URLS: return False
    url = TOOL_URLS[tool_name]
    try:
        r = requests.get(url, stream=True, timeout=15)
        ext = ".zip" if "zip" in url or "master" in url else ".tar.gz"
        pkg_path = f"/tmp/{tool_name}{ext}"
        with open(pkg_path, 'wb') as f: f.write(r.content)
        if "zip" in ext:
            with zipfile.ZipFile(pkg_path, 'r') as z: z.extractall(BIN_DIR)
        else:
            with tarfile.open(pkg_path, "r:gz") as t: t.extractall(path=BIN_DIR)
        os.remove(pkg_path)
        return True
    except: return False

def is_authorized(target):
    target = target.lower().strip()
    if not target: return False, "🎯 Awaiting Sector..."
    out_list = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
    in_list = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
    for forbidden in out_list:
        if forbidden in target: return False, f"🛑 FORBIDDEN: {forbidden}"
    for allowed in in_list:
        if allowed in target: return True, "✅ AUTHORIZED"
    return False, "⚠️ OUT OF SCOPE"

def generate_pdf_report(target, t_type, content):
    if not PDF_ENABLED: return None
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", "B", 16)
    pdf.cell(200, 10, txt="SMALLVILLE S.V. 5.0 - STRIKE DOSSIER", ln=True, align='C')
    pdf.set_font("Courier", "", 10)
    pdf.cell(200, 10, txt=f"TARGET: {target} | CLASS: {t_type} | DATE: {datetime.now()}", ln=True, align='C')
    pdf.ln(10)
    clean_text = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 5, txt=clean_text)
    report_path = f"/tmp/report_{int(time.time())}.pdf"
    pdf.output(report_path)
    return report_path

# --- 6. SIDEBAR: THE COMMAND DECK ---
with st.sidebar:
    st.title("🔴 COMMAND")
    st.session_state.battery_type = st.radio("ENVIRONMENT", ["Web2", "Web3", "AI Agent"])
    
    st.divider()
    st.subheader("🛡️ SCOPE (ROE)")
    st.session_state.in_scope = st.text_area("🟢 GREEN ZONE", st.session_state.in_scope)
    st.session_state.out_scope = st.text_area("🔴 RED ZONE", st.session_state.out_scope)
    
    st.divider()
    if st.button("🔌 PRIME FULL ARSENAL"):
        with st.status("Fabricating 22+ Tools...", expanded=True) as s:
            for tool in TOOL_URLS.keys():
                s.write(f"📥 Fetching {tool}...")
                fabricate_core(tool); time.sleep(0.2)
            s.update(label="Arsenal Ready.", state="complete")
        st.rerun()

    if st.button("💀 BURN INSTANCE"):
        shutil.rmtree(BIN_DIR, ignore_errors=True)
        st.session_state.last_log = "MEMORY PURGED."
        st.rerun()

# --- 7. MISSION CONTROL ---
st.title("🏹 SMALLVILLE S.V. 5.0")
auth, msg = is_authorized(st.session_state.target)

tabs = st.tabs(["🚀 STRIKE OPS", "📊 ARSENAL MATRIX", "📟 LIVE HUD"])

with tabs[0]:
    st.header(f"🔫 {st.session_state.battery_type.upper()} ENGAGEMENT")
    st.session_state.target = st.text_input("🎯 TARGET SECTOR", st.session_state.target)
    
    if auth:
        st.success(f"{msg} | Interlock Released.")
        if st.button("🔥 INITIATE FULL AUTO-STRIKE"):
            st.session_state.last_log = f"🚀 [INIT] {st.session_state.battery_type} STRIKE AUTHORIZED...\n"
            final_out = []
            with st.status("⛓️ Chain Executing...", expanded=True) as s:
                # RECON PHASE
                s.write("📡 Running Recon Cluster...")
                sub_b = find_exe("subfinder")
                if sub_b:
                    res = subprocess.run([sub_b, "-d", st.session_state.target, "-silent"], capture_output=True, text=True)
                    final_out.append(f"--- [RECON] ---\n{res.stdout}")
                
                # TARGET SPECIFIC PHASE
                if "Web2" in st.session_state.battery_type:
                    s.write("☢️ Firing Nuclei Strike...")
                    nuc_b = find_exe("nuclei")
                    if nuc_b:
                        res = subprocess.run([nuc_b, "-u", st.session_state.target, "-silent", "-ni"], capture_output=True, text=True)
                        final_out.append(f"--- [VULNS] ---\n{res.stdout}")
                
                elif "AI Agent" in st.session_state.battery_type:
                    s.write("🧠 Probing Model Secrets...")
                    tru_b = find_exe("trufflehog")
                    if tru_b:
                        res = subprocess.run([tru_b, "github", "--repo", st.session_state.target], capture_output=True, text=True)
                        final_out.append(f"--- [SECRETS] ---\n{res.stdout}")

                st.session_state.last_log = "\n\n".join(final_out)
                s.update(label="Strike Complete.", state="complete")
    else:
        st.error(msg)

with tabs[1]:
    st.header("📋 STATUS MATRIX")
    cols = st.columns(4)
    for i, (cat, tools) in enumerate(ARSENAL.items()):
        with cols[i]:
            st.subheader(cat)
            for t in tools:
                ready = find_exe(t) is not None
                color = "#00ff00" if ready else "#555"
                st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {t.upper()}</span>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown(f'<div class="terminal">{st.session_state.last_log}</div>', unsafe_allow_html=True)
    if PDF_ENABLED and len(st.session_state.last_log) > 50:
        report = generate_pdf_report(st.session_state.target, st.session_state.battery_type, st.session_state.last_log)
        with open(report, "rb") as f:
            st.download_button("📄 DOWNLOAD REPORT", f, file_name=f"Strike_{st.session_state.target}.pdf")
