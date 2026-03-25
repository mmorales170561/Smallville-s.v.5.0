import streamlit as st
import subprocess
import os
import shutil

# --- 1. HUD CONFIG ---
st.set_page_config(page_title="RUBY-OPERATOR v7.5", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff3131; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff3131; }
    .terminal { background-color: #000; color: #00ff00; padding: 15px; border: 1px solid #333; height: 300px; overflow-y: scroll; white-space: pre-wrap; font-size: 11px; border-left: 5px solid #ff3131; }
    .stButton>button { background-color: #ff3131 !important; color: #000 !important; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    h1, h2, h3 { color: #ff3131 !important; }
    </style>
    """, unsafe_allow_html=True)

BIN_DIR = "/tmp/ruby_bin"
if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)

# --- 2. GLOBAL RESOLVER ---
def resolve_tool_path(name):
    """
    Scans /tmp/ruby_bin for the actual executable.
    Handles 'arjun' vs 'arjun.py' and subdirectories.
    """
    # 1. Check if it's already in the system PATH (like python3 or git)
    sys_path = shutil.which(name)
    if sys_path: return sys_path

    # 2. Deep scan the workspace
    for root, _, files in os.walk(BIN_DIR):
        for f in files:
            # Look for exact match, .py match, or directory-based match
            if f == name or f == f"{name}.py" or (name == "sqlmap" and f == "sqlmap.py"):
                full_path = os.path.join(root, f)
                os.chmod(full_path, 0o755)
                return full_path
    return None

def run_shell(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"CRITICAL ERROR: {str(e)}"

# --- 3. MAIN HUD ---
st.title("🏹 SMALLVILLE S.V. 7.5")
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📊 MATRIX", "📟 HUD", "🛠️ TERMINAL", "🔍 DEBUG"])

with t2:
    st.subheader("OMNI-BATTERY INTEGRITY")
    ARSENAL = {
        "Web2": ["subfinder", "httpx", "katana", "nuclei"],
        "Web3": ["aderyn", "arjun"],
        "AI Agent": ["trufflehog", "sqlmap"]
    }
    
    for cat, tools in ARSENAL.items():
        st.write(f"### {cat}")
        cols = st.columns(4)
        for i, name in enumerate(tools):
            exe_path = resolve_tool_path(name)
            ready = exe_path is not None
            color = "#00ff00" if ready else "#555"
            with cols[i % 4]:
                st.markdown(f"<span style='color:{color}'>{'✅' if ready else '❌'} {name.upper()}</span>", unsafe_allow_html=True)
                if ready: st.caption(f"Linked: ...{exe_path[-25:]}")

with t5:
    st.subheader("⚡ TACTICAL RECOVERY CONSOLE")
    st.info(f"Arjun Cloned: {os.path.exists(os.path.join(BIN_DIR, 'arjun_git'))}")
    
    if st.button("🔎 RE-SCAN & FIX PERMISSIONS"):
        st.rerun()

    st.divider()
    if st.button("🔎 DEEP SCAN DIRECTORY"):
        all_files = []
        for r, d, f in os.walk(BIN_DIR):
            for file in f: all_files.append(os.path.join(r, file))
        st.code("\n".join(all_files) if all_files else "Workspace Empty.")

with t4:
    st.subheader("⌨️ MANUAL OVERRIDE")
    st.markdown("**Arjun Usage:** `python3 /tmp/ruby_bin/arjun_git/arjun.py -u [URL]`")
    cmd_in = st.text_input("CMD >", placeholder="ls -la /tmp/ruby_bin/arjun_git")
    if st.button("🚀 EXECUTE"):
        st.code(run_shell(f"cd {BIN_DIR} && {cmd_in}"))
