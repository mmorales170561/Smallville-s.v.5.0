import streamlit as st
import subprocess
import requests
import re

# --- 1. CLOUD STORAGE SCANNER ---
def check_cloud_leak(subdomain):
    """
    Checks if a subdomain is actually a front for a misconfigured 
    Cloud storage bucket (S3, GCP, Azure).
    """
    cloud_signatures = {
        "AWS S3": ".s3.amazonaws.com",
        "GCP": ".storage.googleapis.com",
        "Azure": ".blob.core.windows.net",
        "Firebase": ".firebaseio.com"
    }
    
    results = []
    for provider, sig in cloud_signatures.items():
        # Heuristic: If the subdomain string contains a cloud provider signature
        if sig in subdomain.lower():
            try:
                # Test for "Public Listable" (The $5,000 mistake)
                test_url = f"https://{subdomain}/?delimiter=/"
                r = requests.get(test_url, timeout=5)
                if "ListBucketResult" in r.text or "PublicAccessBlock" not in r.text:
                    results.append(f"🚨 CRITICAL: Open {provider} Bucket found at {subdomain}")
                else:
                    results.append(f"🟡 {provider} detected, but appears private.")
            except:
                pass
    return results

# --- 2. UPDATED INTERFACE ---
t1, t2, t3, t4 = st.tabs(["🚀 STRIKE", "📡 SUBDOMAIN RADAR", "☁️ CLOUD SCRAPER", "🧪 IDOR LAB"])

with t2:
    st.header("Subdomain Radar")
    root_domain = st.text_input("Root Domain", placeholder="example.com")
    if st.button("📡 SCAN & EVALUATE"):
        # run subfinder...
        subs = ["dev-assets.example.com", "staging-db.s3.amazonaws.com", "backup.firebaseio.com"] # Example output
        st.session_state.found_subs = subs
        for s in subs:
            st.write(f"Found: `{s}`")

with t3:
    st.header("Cloud Storage Hunter")
    st.info("Scanning for misconfigured S3, Firebase, and Azure Blobs.")
    
    if 'found_subs' in st.session_state:
        if st.button("🔍 SCRAPE CLOUD PERMISSIONS"):
            for sub in st.session_state.found_subs:
                leaks = check_cloud_leak(sub)
                if leaks:
                    for leak in leaks:
                        st.warning(leak)
                else:
                    st.write(f"Checked {sub}: No leaks found.")
    else:
        st.info("Run the Subdomain Radar first to populate the target list.")

# --- 3. IDOR LAB (Refined) ---
with t4:
    st.header("IDOR Lab (User A vs User B)")
    # Clear explanation of the IDOR logic
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/IDOR_Logic.png/640px-IDOR_Logic.png", caption="IDOR Attack Vector")
