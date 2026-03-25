import streamlit as st
import subprocess
import os
import shutil

# --- 1. HUD & PATH INJECTION ---
st.set_page_config(page_title="SMALLVILLE V13.2", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

# CRITICAL: Inject the local bin path reported in your error
LOCAL_BIN = "/home/appuser/.local/bin"
BIN_DIR = "/tmp/ruby_bin"
if LOCAL_BIN not in os.environ["PATH"]:
    os.environ["PATH"] = f"{LOCAL_BIN}:{BIN_DIR}:" + os.environ["PATH"]

if 'term_logs' not in st.session_state: st.session_state.term_logs = "PATH REALIGNED. READY..."

# --- 2. THE STABILIZED FORGE ---
def forge_stabilized():
    status = st.status("🛠️ RESOLVING DEPENDENCY HELL...", expanded=True)
    
    # Force-installing the 'Golden versions' to stop Mindgard from breaking
    # We use openai < 2.0.0 to satisfy the Mindgard 0.108.1 requirement
    commands = [
        "pip install --upgrade pip",
        "pip install 'openai<2.0.0' 'transformers<5.0.0' 'rich<14.0.0' --break-system-packages",
        "pip install mindgard garak snyk-agent-scan promptfoo --break-system-packages"
    ]
    
    for cmd in commands:
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                status.write(f"✅ {cmd[:25]}... SUCCESS")
            else:
                status.write(f"⚠️ {cmd[:25]}... Check Logs")
        except Exception as e:
            status.write(f"❌ ERROR: {str(e)}")

    status.update(label="SYSTEM REALIGNED", state="complete")
    st.rerun()

# --- 3. THE HUD ---
with st.sidebar:
    st.title("🔴 COMMAND")
    if st.button("🔌 PRIME STABILIZED SYSTEM", use_container_width=True):
        forge_stabilized()
    st.divider()
    st.info(f"Active Path: {os.environ['PATH'][:50]}...")

t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "💰 LOOT", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("📊 ARSENAL INTEGRITY")
    # Matrix now checks the newly injected PATH
    tools = ["garak", "mindgard", "openai", "transformers", "snyk-agent-scan", "subfinder"]
    cols = st.columns(3)
    for i, name in enumerate(tools):
        # shutil.which checks the entire PATH we just injected
        ready = shutil.which(name) is not None
        status_icon = "🟢 ONLINE" if ready else "🔴 PATH MISSING"
        cols[i % 3].info(f"**{name.upper()}**\n\n{status_icon}")

with t4:
    st.subheader("⌨️ TERMINAL")
    st.markdown(f'<div style="background:#000;color:#00ff00;padding:10px;height:300px;overflow:auto;border-left:5px solid #ff3131;">{st.session_state.term_logs}</div>', unsafe_allow_html=True)
    c_in = st.text_input("CMD >", key="c_input")
    if st.button("🚀 EXECUTE"):
        res = subprocess.run(c_in, shell=True, capture_output=True, text=True)
        st.session_state.term_logs += f"\n$ {c_in}\n{res.stdout}{res.stderr}"
        st.rerun()
