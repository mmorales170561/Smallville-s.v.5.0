import streamlit as st
import subprocess
import os

# --- VINTAGE UI ---
st.set_page_config(page_title="The Daily Planet", layout="wide")
st.markdown("<style>.stApp { background-color: #f4f1ea; font-family: 'Courier New'; }</style>", unsafe_allow_html=True)

# ... (Include your existing Authentication logic here) ...

# --- INVESTIGATION DESK ---
st.title("🗞️ THE DAILY PLANET: INVESTIGATIVE DESK")
target = st.text_input("PRIMARY TARGET")
in_scope = st.text_area("IN-SCOPE ASSETS")
out_scope = st.text_area("OUT-OF-SCOPE (PROTECTED)")

if st.button("FILE THE STORY"):
    with st.spinner("Clark Kent is investigating..."):
        try:
            # Set scope variables
            os.environ["IN_SCOPE"] = in_scope
            os.environ["OUT_SCOPE"] = out_scope
            
            # Execute and capture
            result = subprocess.check_output(f"source ./powers.sh && observer {target}", 
                                             shell=True, executable='/bin/bash', stderr=subprocess.STDOUT)
            
            output_text = result.decode('utf-8')
            st.code(output_text)
            
            # Generate Download Button
            st.download_button(
                label="📥 Download Daily Planet Report",
                data=output_text,
                file_name=f"Daily_Planet_Report_{target}.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"LEXCORP INTERFERENCE: {str(e)}")
