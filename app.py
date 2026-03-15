import streamlit as st
import subprocess
import os

# --- AUTH & TERMINAL THEME ---
# (Keep your existing styling logic here)

if st.button(">> EXECUTE_WATCHTOWER_HUNT"):
    # This empty container acts as our live console
    console = st.empty()
    
    with st.spinner(">> [BUSY] WATCHTOWER ENGAGED..."):
        try:
            # We run the command and read the output line by line
            process = subprocess.Popen(
                ["bash", "powers.sh", "automated_hunt", target],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Live Terminal Output
            live_log = ""
            for line in iter(process.stdout.readline, ''):
                live_log += line
                console.code(live_log) # The console updates in real-time!
            
            process.wait()
            st.success(">> [SUCCESS] SCAN COMPLETE.")
            
        except Exception as e:
            st.error(f">> [CRITICAL_FAILURE]: {str(e)}")
