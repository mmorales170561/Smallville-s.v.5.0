import streamlit as st
import subprocess, os, requests, zipfile, tarfile, io, shutil

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. CONFIG & PATHS ---
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'full_output' not in st.session_state:
    st.session_state.full_output = ">> SYSTEM READY."

# --- 3. STORAGE MONITOR ---
def get_storage_usage():
    if not os.path.exists(BIN_PATH): return 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(BIN_PATH):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    
    # Storage Gauge
    usage = get_storage_usage()
    st.write(f"📊 Storage: **{usage}MB** / 2000MB")
    st.progress(min(usage / 2000, 1.0))

    if st.button("🔴 HARD RESET", use_container_width=True):
        if os.path.exists(BIN_PATH): shutil.rmtree(BIN_PATH)
        st.rerun()

    if st.button("PRIME GOD-MODE TOOLS", use_container_width=True):
        # Updated URLs: Katana and Airix often use .tar.gz on Linux
        URLS = {
            "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
            "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
            "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
            "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
            "airix": "https://github.com/projectdiscovery/airix/releases/download/v0.0.3/airix_0.0.3_linux_amd64.zip"
        }
        os.makedirs(BIN_PATH, exist_ok=True)
        for name, url in URLS.items():
            with st.spinner(f"Unlocking {name}..."):
                try:
                    r = requests.get(url, stream=True)
                    file_bytes = io.BytesIO(r.content)
                    
                    if url.endswith(".zip"):
                        with zipfile.ZipFile(file_bytes) as z:
                            for f in z.namelist():
                                if f.endswith(name):
                                    with open(os.path.join(BIN_PATH, name), "wb") as b:
                                        b.write(z.read(f))
                    
                    elif url.endswith(".tar.gz") or name in ["katana", "airix"]:
                        # Fallback for tar.gz or suspected tar files
                        try:
                            with tarfile.open(fileobj=file_bytes, mode="r:gz") as t:
                                for member in t.getmembers():
                                    if member.name.endswith(name):
                                        member.name = os.path.basename(member.name)
                                        t.extract(member, BIN_PATH)
                        except:
                            # If it's not a tar.gz, maybe it's a zip mislabeled or vice versa
                            st.error(f"Format mismatch for {name}. Check URL.")

                    os.chmod(os.path.join(BIN_PATH, name), 0o755)
                    st.success(f"✓ {name}")
                except Exception as e: st.error(f"Err {name}: {e}")

    st.divider()
    p1 = st.toggle("P1", True); p2 = st.toggle("P2", True)
    p3 = st.toggle("P3", True); p4 = st.toggle("P4", True)
    p5 = st.toggle("P5", True); p6 = st.toggle("P6", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN: GOD-MODE HUD")
col_in, col_term = st.columns([1, 2])

with col_in:
    tn = st.text_input("🎯 TARGET NAME", "x.com")
    ru = st.text_input("🔗 ROOT URL", "x.com")
    gh = st.text_input("🐙 GITHUB REPO")
    os_scope = st.text_area("✗ OUT-SCOPE (Exclude these)")

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.full_output = "--- MISSION START ---\n"
        env = os.environ.copy()
        env.update({"PATH": f"{BIN_PATH}:{env.get('PATH', '')}", "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0", "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0", "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0", "OUT_SCOPE": os_scope, "GH_REPO": gh})
        
        subprocess.run(["chmod", "+x", SCRIPT_PATH])
        with col_term:
            term_placeholder = st.empty()
            process = subprocess.Popen(["bash", SCRIPT_PATH, "strike", ru, tn], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, bufsize=1)
            for line in iter(process.stdout.readline, ""):
                st.session_state.full_output += line
                term_placeholder.code(st.session_state.full_output, language="bash")
            process.wait()

with col_term:
    st.code(st.session_state.full_output, language="bash")
