import streamlit as st
import subprocess
import os

# Define the paths
BIN_PATH = "/tmp/bin"
CWD = os.getcwd()
SCRIPT = os.path.join(CWD, "powers.sh")

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")
st.title("SUPER//MAN CONTROL CENTER")

# Sidebar for Priming
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("PRIME ELITE TOOLS"):
        with st.spinner("📥 Downloading..."):
            subprocess.run(["chmod", "+x", SCRIPT])
            subprocess.run(["bash", SCRIPT, "prime"])
            st.success("Tools Loaded!")

# Main HUD
tn = st.text_input("🎯 TARGET NAME")
ru = st.text_input("🔗 ROOT DOMAIN")

if st.button("FIRE RED KRYPTONITE GUN", type="primary"):
    if tn and ru:
        st.info("Strike Initialized...")
        term = st.empty()
        
        # Run the bash script and stream the output
        env = os.environ.copy()
        env["RUN_P1"] = "1"
        env["RUN_P4"] = "1"
        
        proc = subprocess.Popen(["bash", SCRIPT, "strike", ru, tn], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                text=True, env=env)
        
        full_output = ""
        while True:
            line = proc.stdout.readline()
            if not line and proc.poll() is not None: break
            if line:
                full_output += line
                term.code(full_output) # Red-style terminal display
        
        st.success("Mission Complete.")
