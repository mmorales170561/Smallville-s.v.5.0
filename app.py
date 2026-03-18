import streamlit as st
# ... (imports remain the same) ...

# --- 6. MAIN HUD ---
with col_in:
    st.subheader("📝 Mission Brief")
    mission_name = st.text_input("🎯 MISSION NAME", f"S.V_{datetime.now().strftime('%H%M')}")
    target_url = st.text_input("🔗 TARGET URL(S)", "syfe.com, x.com")
    h1_user = st.text_input("🆔 H1 USERNAME", placeholder="super__man")
    
    with st.expander("🛡️ Rules of Engagement", expanded=True):
        in_scope = st.text_area("✓ IN-SCOPE", "syfe.com", height=60)
        out_scope = st.text_area("✗ OUT-SCOPE", "api.syfe.com", height=60)

    if st.button("FIRE RED KRYPTONITE GUN", type="primary", use_container_width=True):
        st.session_state.logs = f"--- MISSION: {mission_name} START ---\n"
        
        env = os.environ.copy()
        env.update({
            "PATH": f"{BIN_PATH}:{env.get('PATH', '')}",
            "H1_USER": h1_user if h1_user else "Smallville-User",
            "RUN_P1": "1" if p1 else "0", "RUN_P2": "1" if p2 else "0",
            "RUN_P3": "1" if p3 else "0", "RUN_P4": "1" if p4 else "0",
            "RUN_P6": "1" if p6 else "0",
            "FORCE_ROOT": "1" if force_root else "0",
            "RUN_STEALTH": "1" if stealth else "0",
            "OUT_SCOPE_LIST": out_scope.replace("\n", ","),
            "IN_SCOPE_LIST": in_scope.replace("\n", ",")
        })
        # ... (rest of the subprocess logic) ...
