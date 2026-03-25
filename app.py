import streamlit as st
import subprocess
import os
import requests
import zipfile
import tarfile
import shutil
import io

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="SMALLVILLE T2 V9.9", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; } [data-testid='stSidebar'] { background-color: #0a0a0a; border-right: 1px solid #ff3131; } .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: scroll; white-space: pre-wrap; font-size: 12px; border-left: 5px solid #ff3131; } .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; } h1, h2, h3 { color: #ff3131 !important; }</style>", unsafe_allow_html=True)

BIN_DIR, LOOT_DIR, WORD_DIR = "/tmp/ruby_bin", "/tmp/ruby_loot", "/tmp/ruby_wordlists"
for d in [BIN_DIR, LOOT_DIR, WORD_DIR]: 
    if not os.path.exists(d): os.makedirs(d)

if 'term_logs' not in st.session_state: st.session_state.term_logs = "APEX ONLINE..."

# --- 2. THE ELITE FORGE ---
def forge_arsenal():
    status = st.status("🛠️ FORGING ELITE ARSENAL...", expanded=True)
    bins = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "ffuf": "https://github.com/ffuf/ffuf/releases/download/v2.1.0/ffuf_2.1.0_linux_amd64.tar.gz",
        "gau": "https://github.com/lc/gau/releases/download/v2.2.3/gau_2.2.3_linux_amd64.tar.gz",
        "aderyn": "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    }
    repos = {"arjun": "https://github.com/s0md3v/Arjun.git", "sqlmap": "https://github.com/sqlmapproject/sqlmap.git", "trufflehog": "https://github.com/trufflesecurity/trufflehog.git", "secretfinder": "https://github.com/m4ll0k/SecretFinder.git"}
    
    for name, url in bins.items():
        try:
            r = requests.get(url, timeout=25)
            if ".zip" in url:
                with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                    for f in z.namelist():
                        if f.endswith(name) and not f.endswith(('.md', '.txt')):
                            with open(os.path.join(BIN_DIR, name), "wb") as b: b.write(z.read(f))
            elif ".tar" in url:
                ext = ".tar.gz" if ".gz" in url else ".tar.xz"
                t_p = f"/tmp/c{ext}"
                with open(t_p, "wb") as f: f.write(r.content)
                subprocess.run(["tar", "-xvf", t_p, "-C", BIN_DIR], capture_output=True)
                for root, _, files in os.walk(BIN_DIR):
                    if name in files and root != BIN_DIR: shutil.move(os.path.join(root, name), os.path.join(BIN_DIR, name))
            p = os.path.join(BIN_DIR, name); os.chmod(p, 0o755)
            status.write(f"✅ {name.upper()}")
        except: status.write(f"❌ {name.upper()} FAIL")
    
    for name, url in repos.items():
        try:
            tp = os.path.join(BIN_DIR, name)
            if not os.path.exists(tp): subprocess.run(["git", "clone", "--depth", "1", url, tp], check=True)
            status.write(f"✅ {name.upper()} REPO")
        except: status.write(f"❌ {name.upper()} REPO FAIL")
    
    # Bug-Hunting Wordlist
    with open(f"{WORD_DIR}/discovery.txt", "w") as w: w.write("admin\napi\nv1\n.env\nconfig\nbackup\n.git\nlogin\nportal\nswagger\nroot\ndatabase\nphpinfo")
    status.update(label="ELITE FORGE COMPLETE", state="complete")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🔴 COMMAND")
    sel_bat = st.selectbox("🎯 BATTERY", ["Web2 (Recon)", "Web3 (Chain)", "Fuzzing/Secrets"], key='active_bat')
    if st.button("🔌 PRIME OMNI-ARSENAL", use_container_width=True): forge_arsenal()
    if st.button("💀 WIPE WORKSPACE", use_container_width=True):
        for d in [BIN_DIR, LOOT_DIR, WORD_DIR]: shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        st.rerun()
    
    st.divider()
    st.subheader("📚 WORDLISTS")
    up_file = st.file_uploader("Upload .txt", type="txt")
    if up_file:
        with open(os.path.join(WORD_DIR, up_file.name), "wb") as f: f.write(up_file.getbuffer())
    
    st.divider()
    st.subheader("🛡️ ROE PROTECTION")
    st.text_area("🟢 GREEN ZONE", key='in_scope', value="example.com")
    st.text_area("🔴 RED ZONE", key='out_scope', value=".gov, .mil")

# --- 4. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 9.9")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

tgt = st.session_state.get('target_val', '').strip().lower()
grn = [x.strip().lower() for x in st.session_state.in_scope.split(",") if x.strip()]
red = [x.strip().lower() for x in st.session_state.out_scope.split(",") if x.strip()]
auth = any(d in tgt for d in grn) if tgt else False
deny = any(d in tgt for d in red) if tgt else False

with t1:
    st.subheader(f"DEPLOY: {sel_bat}")
    st.text_input("SET TARGET", key="target_val", placeholder="target.com")
    if not tgt: st.info("Waiting for Target...")
    elif deny: st.error("🛑 RED ZONE INTERLOCK")
    elif not auth: st.warning("⚠️ UNAUTHORIZED")
    else:
        st.success("✅ AUTHORIZED")
        if st.button("🔥 INITIATE STRIKE"):
            st.status(f"Executing {sel_bat} Battery against {tgt}...")

with t2:
    st.subheader("SYSTEM INTEGRITY")
    tools = ["subfinder", "httpx", "katana", "nuclei", "ffuf", "gau", "aderyn", "arjun", "sqlmap", "trufflehog", "secretfinder"]
    cols = st.columns(4)
    for i, name in enumerate(tools):
        ready = os.path.exists(os.path.join(BIN_DIR, name))
        cols[i % 4].write(f"{'✅' if ready else '❌'} {name.upper()}")

with t3:
    st.subheader("📋 COLLECTED INTEL & REPORTING")
    loot_files = os.listdir(LOOT_DIR)
    if loot_files:
        c1, c2, c3 = st.columns([2, 1, 1])
        sel_loot = c1.selectbox("View Loot", loot_files)
        
        # Zip Download
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "x") as l_zip:
            for f in loot_files: l_zip.write(os.path.join(LOOT_DIR, f), f)
        c2.download_button("📦 ZIP ALL", buf.getvalue(), file_name="loot.zip")
        
        # One-Click Report Mockup
        if c3.button("📄 GEN REPORT"):
            with open(os.path.join(LOOT_DIR, "vulnerability_report.md"), "w") as rep:
                rep.write(f"# Bug Bounty Report: {tgt}\n\n## Summary\nAutomated findings from Smallville v9.9.\n\n## Tool Output\n{sel_loot} contains critical discovery data.")
            st.toast("Report Generated in Loot!")

        with open(os.path.join(LOOT_DIR, sel_loot), 'r') as f: st.code(f.read())
    else: st.info("No loot found.")

with t4:
    st.subheader("⌨️ TERMINAL")
    cols = st.columns(4)
    if cols[0].button("🔍 RECON"): st.session_state.c_input = f"subfinder -d {tgt} -o {LOOT_DIR}/subs.txt"
    if cols[1].button("🧪 NUCLEI"): st.session_state.c_input = f"nuclei -u {tgt} -o {LOOT_DIR}/vulns.txt"
    if cols[2].button("⚡ FFUF"): st.session_state.c_input = f"ffuf -u https://{tgt}/FUZZ -w {WORD_DIR}/discovery.txt"
    if cols[3].button("🔗 WEB3"): st.session_state.c_input = f"aderyn {tgt}"

    st.markdown(f'<div class="terminal">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        cmd = c_in
        for b in ["subfinder", "nuclei", "ffuf", "gau", "aderyn", "httpx", "katana"]:
            if b in c_in and not c_in.startswith("/tmp"): cmd = c_in.replace(b, f"{BIN_DIR}/{b}")
        if "sqlmap" in c_in: cmd = f"python3 {BIN_DIR}/sqlmap/sqlmap.py " + c_in.replace("sqlmap", "")
        
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {cmd}\n{res.stdout}{res.stderr}"
        st.rerun()

with t5:
    st.subheader("🔍 DEBUG")
    st.write(f"Bin: `{BIN_DIR}` | Wordlists: `{WORD_DIR}`")
    if st.button("🔎 DEEP SCAN"):
        files = [os.path.join(r, f) for r, d, f in os.walk(BIN_DIR) for f in f]
        st.code("\n".join(files) if files else "Empty")
