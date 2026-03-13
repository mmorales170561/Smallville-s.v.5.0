import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Smallville Suite", page_icon="🛡️", layout="wide")

st.title("🛡️ Smallville Suite: Elite Recon")

# 1. Cloud Provisioning: Install tools if they aren't in /tmp
if not os.path.exists("/tmp/bin/subfinder"):
    with st.status("🛠️ Provisioning Cloud Environment...", expanded=True) as status:
        st.write("Installing Go and Security Tools...")
        subprocess.run(["sh", "setup_cloud.sh"])
        status.update(label="✅ Environment Ready!", state="complete", expanded=False)

# 2. Update Path so Python can see the new tools
os.environ["PATH"] += os.pathsep + "/tmp/bin"

# 3. Sidebar Status
st.sidebar.header("System Status")
st.sidebar.success("Core: Online")
st.sidebar.info(f"Working Dir: {os.getcwd()}")

# 4. Main Interface
action = st.selectbox("Select Mission Power", ["observer", "kingpin", "automated_hunt"])
target = st.text_input("Target Domain", placeholder="e.g., paypal.com")

if st.button("🚀 Execute Power"):
    if not target and action != "kingpin":
        st.warning("Please enter a target domain.")
    else:
        with st.spinner(f"Engaging {action}..."):
            try:
                # We source powers.sh to access your functions directly
                cmd = f"source powers.sh && {action} {target}"
                result = subprocess.check_output(['/bin/bash', '-c', cmd], stderr=subprocess.STDOUT)
                st.subheader("Mission Output")
                st.code(result.decode('utf-8'))
            except Exception as e:
                st.error(f"Mission Interrupted: {str(e)}")
