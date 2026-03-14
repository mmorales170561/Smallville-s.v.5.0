import streamlit as st
import subprocess
import os

# --- SYSTEM PROVISIONING (Run once) ---
if not os.path.exists("/tmp/bin/subfinder"):
    with st.status("🏗️ Constructing Fortress of Solitude..."):
        subprocess.run(["mkdir", "-p", "/tmp/bin"], check=True)
        # Install Go
        subprocess.run(["wget", "-q", "-O", "/tmp/go.tar.gz", "https://go.dev/dl/go1.22.0.linux-amd64.tar.gz"], check=True)
        subprocess.run(["tar", "-C", "/tmp", "-xzf", "/tmp/go.tar.gz"], check=True)
        # Install Tools
        env = os.environ.copy()
        env["PATH"] += ":/tmp/go/bin"
        env["GOBIN"] = "/tmp/bin"
        subprocess.run(["/tmp/go/bin/go", "install", "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], env=env)
        subprocess.run(["/tmp/go/bin/go", "install", "github.com/projectdiscovery/httpx/cmd/httpx@latest"], env=env)
        st.rerun()

os.environ["PATH"] += os.pathsep + "/tmp/bin"

# --- LOGIN GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🛡️ ACTION COMICS: ACCESS REQUIRED")
    p1 = st.text_input("SECRET CODE", type="password")
    if p1 == "superman":
        u = st.text_input("ID")
        p2 = st.text_input("KEY", type="password")
        if u == "clarkkent" and p2 == "smallville":
            if st.button("AUTHORIZE"):
                st.session_state['auth'] = True
                st.rerun()
    st.stop()

# --- DASHBOARD ---
st.title("🗞️ THE DAILY PLANET")
target = st.text_input("TARGET DOMAIN")
if st.button("RUN RECON"):
    with st.spinner("Investigating..."):
        try:
            # We call the tool directly now
            result = subprocess.check_output(["subfinder", "-d", target], stderr=subprocess.STDOUT)
            st.code(result.decode())
        except Exception as e:
            st.error(f"Error: {e}")
