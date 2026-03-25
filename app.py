import streamlit as st
import subprocess
import os
import requests
import tarfile
import zipfile
import shutil
from fpdf import FPDF # New Import for PDF Generation

# --- 1. PDF GENERATION ENGINE ---
def generate_pdf(target, target_type, report_content):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Courier", "B", 16)
    pdf.cell(200, 10, txt="KRYPTONIAN ARSENAL: STRIKE REPORT", ln=True, align='C')
    pdf.set_font("Courier", "", 12)
    pdf.cell(200, 10, txt=f"TARGET: {target}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"ENVIRONMENT: {target_type}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Courier", "B", 12)
    pdf.cell(200, 10, txt="--- TERMINAL OUTPUT ---", ln=True, align='L')
    pdf.ln(5)
    
    pdf.set_font("Courier", "", 10)
    # Clean text to handle non-latin characters that might crash FPDF
    clean_text = report_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 5, txt=clean_text)
    
    report_path = f"/tmp/strike_report_{target}.pdf"
    pdf.output(report_path)
    return report_path

# --- 2. UPDATED STRIKE LOGIC ---
# (Inside your Strike Ops Tab, after the scan finishes...)

                st.session_state.last_log = "\n\n".join(final_output)
                s.update(label=f"{target_type} Strike Complete.", state="complete")
                
                # TRIGGER PDF GENERATION
                report_file = generate_pdf(st.session_state.target, target_type, st.session_state.last_log)
                
                # DISPLAY DOWNLOAD BUTTON
                with open(report_file, "rb") as f:
                    st.download_button(
                        label="📄 DOWNLOAD STRIKE DOSSIER (PDF)",
                        data=f,
                        file_name=f"Smallville_Report_{st.session_state.target}.pdf",
                        mime="application/pdf"
                    )
