# --- 1. SIDEBAR RESTORATION ---
with st.sidebar:
    st.header("⚡ TACTICAL PHASES")
    p1 = st.toggle("P1: CEREBRO", value=True)
    p2 = st.toggle("P2: SHADOW", value=True)
    p3 = st.toggle("P3: KATANA", value=True)
    p4 = st.toggle("P4: STRIKE", value=True)
    p5 = st.toggle("P5: ARCHITECT (Repo)", value=True) # RESTORED
    p6 = st.toggle("P6: OLYMPUS", value=True)
    st.divider()
    stealth = st.toggle("🕵️ STEALTH MODE", value=False)

# --- 2. FIRE BUTTON UPDATE ---
    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        if tn and ru:
            # ... (Log setup)
            env.update({
                "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
                "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
                "RUN_P5": "1" if p5 else "0", "RUN_P6": "1" if p6 else "0",
                "RUN_STEALTH": "1" if stealth else "0",
                "GH_REPO": str(gh_repo),
                "IN_SCOPE": str(is_scope), 
                "OUT_SCOPE": str(os_scope)
            })
            # ... (Execution)
