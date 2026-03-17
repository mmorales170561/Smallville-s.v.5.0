import streamlit as st
import subprocess
import os
import time

# --- 1. CLOUD ENVIRONMENT ---
BIN_PATH = "/tmp/bin"
CWD = os.getcwd()

if 'terminal_logs' not in st.session_state: 
    st.session_state['terminal_logs'] = "READY FOR MISSION..."

st.set_page_config(page_title="Smallville S.V. 5.0", layout="wide")

# --- 2. KRYPTONIAN UI ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-box { 
        background-color: #000; border: 1px solid #ff0000; padding: 20px; 
        color: #ff0000; font-family: 'Courier New', monospace;
        white-space: pre-wrap; height: 600px; overflow-y: auto; font-size: 14px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.5);
    }
    .status-panel { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 2px solid #333; }
    .online { background-color: rgba(0, 255, 65, 0.1); border-color: #00ff41 !important; color: #00ff41; }
    .offline { background-color: rgba(255, 0, 0, 0.1); border-color: #ff0000 !important; color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ARMORY VALIDATION ---
def check_armory():
    required = ["subfinder", "httpx", "naabu", "nuclei"]
    found = []
    if os.path.exists(BIN_PATH):
        found = [f for f in os.listdir(BIN_PATH) if os.path.isfile(os.path.join(BIN_PATH, f))]
    return all(tool in found for tool in required), found

ready, tools_found = check_armory()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if ready:
        st.markdown(f'<div class="status-panel online"><b>SYSTEMS ONLINE</b><br>{len(tools_found)} TOOLS READY</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-panel offline"><b>SYSTEMS OFFLINE</b><br>{len(tools_found)}/4 TOOLS FOUND</div>', unsafe_allow_html=True)
        if tools_found: st.write(f"Found: {', '.join(tools_found)}")

    if st.button("PRIME ELITE TOOLS", width="stretch"):
        with st.spinner("📥 Downloading Tech..."):
            os.makedirs(BIN_PATH, exist_ok=True)
            script_path = os.path.join(CWD, "powers.sh")
            subprocess.run(["sed", "-i", "s/\\r$//", script_path])
            subprocess.run(["chmod", "+x", script_path])
            # Prime the armory
            subprocess.run(["/bin/bash", script_path, "prime"], capture_output=True)
            st.rerun()

    st.divider()
    p1 = st.toggle("P1: CEREBRO", True)
    p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: HOOK", True)
    p4 = st.toggle("P4: STRIKE", True)

# --- 5. MAIN HUD ---
st.title("SUPER//MAN CONTROL CENTER")
col_in, col_term = st.columns([1, 2.2])

with col_in:
    st.subheader("Mission Brief")
    tn = st.text_input("🎯 TARGET NAME", key="tn")
    ru = st.text_input("🔗 ROOT DOMAIN", key="ru")
    is_scope = st.text_area("✓ IN-SCOPE", key="is", height=100)
    
    if st.button("FIRE RED KRYPTONITE GUN", width="stretch", type="primary"):
        if not ready:
            st.error("ARMORY EMPTY - RUN PRIME FIRST")
        elif tn and ru:
            # RESET LOGS
            st.session_state['terminal_logs'] = f"--- STRIKE INITIALIZED: {tn} ---\n"
            term_display = st.empty()
            
            # ENSURE PERMISSIONS ON TOOLS
            subprocess.run(f"chmod +x {BIN_PATH}/*", shell=True)

            env = os.environ.copy()
            env["PATH"] = f"{BIN_PATH}:{env.get('PATH', '')}"
            env.update({"RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                        "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                        "IN_SCOPE": str(is_scope)})

            script_path = os.path.join(CWD, "powers.sh")
            proc = subprocess.Popen(
                ["/bin/bash", script_path, "strike", str(ru), str(tn)],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, cwd=CWD, bufsize=1
            )

            while True:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None: break
                if line:
                    st.session_state['terminal_logs'] += line
                    term_display.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
            
            st.success("Target Engaged.")

with col_term:
    st.subheader("Live Tactical Feed")
    st.markdown(f'<div class="terminal-box">{st.session_state["terminal_logs"]}</div>', unsafe_allow_html=True)
