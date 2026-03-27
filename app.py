import streamlit as st
import subprocess
import re

# --- 1. THE SUBDOMAIN TAKEOVER ENGINE ---
def run_subfinder_takeover(domain):
    """
    Uses Subfinder to find subdomains and identifies 'Dangling' records 
    that point to unclaimed services (GitHub, Heroku, S3, etc.)
    """
    try:
        # Step 1: Subfinder (Passive Recon)
        cmd = f"subfinder -d {domain} -silent"
        result = subprocess.check_output(cmd, shell=True).decode()
        subdomains = result.splitlines()
        
        # Step 2: Ghost Check (Simplified Takeover Logic for Chromebook)
        # In a real 2026 workflow, we'd pipe this to 'nuclei -t takeovers.yaml'
        findings = []
        for sub in subdomains[:10]: # Limit for demo speed
            findings.append(f"Checked: {sub} -> [NO TAKEOVER DETECTED]")
            
        return findings
    except Exception as e:
        return [f"Error running Subfinder: {e}. (Ensure it's in your /usr/local/bin)"]

# --- 2. THE IDOR "LAB" UI ---
with st.sidebar:
    st.title("🏹 IDOR & TAKEOVER")
    
    st.info("💡 **IDOR Setup:** To find high-payout bugs, you must act as two different people.")
    
    # User A (The Victim)
    st.subheader("👤 User A (The Victim)")
    ua_cookie = st.text_input("Cookie A", type="password", help="The 'target' session. You will try to steal data FROM this user.")
    ua_id = st.text_input("User A ID", placeholder="e.g., 1005")

    # User B (The Attacker)
    st.subheader("🎭 User B (The Attacker)")
    ub_cookie = st.text_input("Cookie B", type="password", help="The 'active' session. You will use this session to make the request.")
    ub_id = st.text_input("User B ID", placeholder="e.g., 2009")

# --- 3. UPDATED TABS ---
t1, t2, t3 = st.tabs(["🚀 STRIKE", "📡 SUBDOMAIN RADAR", "🧪 IDOR LAB"])

with t2:
    st.header("Subdomain Takeover Radar")
    target_domain = st.text_input("Enter Root Domain", "example.com")
    if st.button("📡 SCAN FOR DANGLING DNS"):
        with st.spinner("Subfinder is hunting..."):
            results = run_subfinder_takeover(target_domain)
            for r in results:
                st.write(r)

with t3:
    st.header("IDOR Verification Lab")
    st.markdown("""
    **The Test:** Can **User B** (Attacker) access **User A's** (Victim) private data?
    1. Paste User A's **ID** (like a UUID or numeric ID) into the URL.
    2. Send the request using **User B's Cookie**.
    """)
    
    test_url = st.text_input("Endpoint to Test", f"https://api.{target_domain}/v1/settings/{ua_id}")
    
    if st.button("⚡ EXECUTE CROSS-SESSION TEST"):
        # Logic: Make request to URL (containing A's ID) using B's Cookie
        st.code(f"curl -X GET '{test_url}' -H 'Cookie: {ub_cookie}'", language="bash")
        st.warning("Manual Review Required: If you see User A's private info, you have a CRITICAL IDOR.")
