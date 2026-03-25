import streamlit as st
import subprocess
import os
import requests
import tarfile
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.6", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 350px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. THE ADERYN INJECTOR ---
def inject_aderyn():
    """Directly fetches the pre-compiled Aderyn binary."""
    # Using the universal x86_64-unknown-linux-musl for maximum compatibility
    url = "https://github.com/Cyfrin/aderyn/releases/download/aderyn-v0.6.8/aderyn-x86_64-unknown-linux-gnu.tar.xz"
    try:
        r = requests.get(url, stream=True)
        archive_path = os.path.join(BIN_DIR, "aderyn.tar.xz")
        with open(archive_path, "wb") as f:
            f.write(r.content)
        
        # Unpack .tar.xz
        with tarfile.open(archive_path, "r:xz") as tar:
            tar.extractall(path=BIN_DIR)
        
        # Move binary to root of BIN_DIR and set permissions
        # Note: Aderyn typically extracts into a folder named 'aderyn'
        for root, dirs, files in os.walk(BIN_DIR):
            if "aderyn" in files and root != BIN_DIR:
                shutil.move(os.path.join(root, "aderyn"), os.path.join(BIN_DIR, "aderyn"))
        
        os.chmod(os.path.join(BIN_DIR, "aderyn"), 0o755)
        os.remove(archive_path)
        return "SUCCESS: Aderyn injected into Foundry."
    except Exception as e:
        return f"FAILURE: {str(e)}"

# --- 3. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.6")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("SYSTEM INTEGRITY")
    # Check specifically for the aderyn binary
    aderyn_path = os.path.join(BIN_DIR, "aderyn")
    ready = os.path.exists(aderyn_path)
    color = "#00ff00" if ready else "#555"
    st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} ADERYN</span>", unsafe_allow_html=True)
    if ready: st.caption(f"Path: {aderyn_path}")

with t5:
    st.subheader("🛠️ FOUNDRY OVERRIDE")
    if st.button("💉 INJECT ADERYN BINARY"):
        result = inject_aderyn()
        st.code(result)
        st.rerun()

    if st.button("🔎 DEEP SCAN"):
        files = [os.path.join(r, f) for r, d, f in os.walk(BIN_DIR) for f in f]
        st.code("\n".join(files) if files else "Workspace Empty.")
