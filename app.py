import streamlit as st
import subprocess, os, requests, zipfile, io, shutil
from datetime import datetime

# --- 1. INITIALIZE ---
st.set_page_config(page_title="Smallville S.V. 5.7", layout="wide")
BIN_PATH = "/tmp/smallville_bin"
SCRIPT_PATH = os.path.join(os.getcwd(), "powers.sh")

if 'logs' not in st.session_state: st.session_state.logs = ">> SYSTEM READY."

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ WEAPON SYSTEM")
    if st.button("🚀 PRIME GOD-MODE TOOLS", use_container_width=True):
        # (Prime Armory logic same as v5.5)
        pass
    st.divider()
    p1 = st.toggle("P1: CEREBRO", True); p2 = st.toggle("P2: SHADOW", True)
    p3 = st.toggle("P3: KATANA", True); p4 = st.toggle("P4: STRIKE", True)
    p5 = st.toggle("P5: ARCHITECT", True); p6 = st.toggle("P6: OLYMPUS", True)
    stealth = st.toggle("🕵️ STEALTH MODE", True)

# --- 3. MAIN HUD ---
st.title("SUPER//MAN: VISIBLE AEGIS HUD")
col_in, col_term = st.columns([1.2, 2])

with col_in:
    st.subheader("🎯 Target Selection")
    target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com, bose.com", help="Separate multiple targets with commas")
    h1_user = st.text_input("🆔 H1 USERNAME", placeholder="hackerone_handle")

    # --- THE MISSING SECTION: SCOPE MANAGEMENT ---
    st.subheader("🛡️ Rules of Engagement")
    in_scope = st.text_area("✓ IN-SCOPE (Allowed)", "syfe.com\nbose.com", height=80, help="One domain per line")
    out_scope = st.text_area("✗ OUT-SCOPE (Forbidden)", "api.syfe.com\n*.staging.bose.com", height=80, help="One domain per line. Use * for wildcards.")

    # Precision Logic: Clean the lists
    targets = [t.strip() for t in target_url.split(",") if t.strip()]
    forbidden = [o.strip() for o in out_scope.split("\n") if o.strip()]
    
    # Check for direct overlap
    overlap = [t for t in targets if t in forbidden]
    
    if overlap:
        st.error(f"⚠️ TARGET BLOCKED: {', '.join(overlap)} is in your OUT-SCOPE list.")
        st.stop() # Prevents firing if there is a direct conflict

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION START: {datetime.now().strftime('%H:%M')} ---\n"
        env = os.environ.copy()
        env.update({
            "H1_USER": h1_user if h1_user else "User",
            "OUT_SCOPE_LIST": ",".join(forbidden),
            "IN_SCOPE_LIST": in_scope.replace("\n", ","),
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
            "RUN_STEALTH": "1" if stealth else "0"
        })
        
        process = subprocess.Popen(["bash", SCRIPT_PATH, "strike", target_url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True)
        term_placeholder = st.empty()
        for line in iter(process.stdout.readline, ""):
            st.session_state.logs += line
            term_placeholder.code(st.session_state.logs[-3000:], language="bash")
        process.wait()

with col_term:
    st.subheader("📟 Tactical Console")
    st.code(st.session_state.logs, language="bash")
