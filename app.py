import streamlit as st
import subprocess
import os
import json
import requests
from bs4 import BeautifulSoup

# --- 1. THE POLICY INTELLIGENCE MODULE ---
class H1Scraper:
    def __init__(self, handle):
        self.handle = handle
        self.url = f"https://hackerone.com/{handle}"
        self.headers = {"Accept": "application/json"}

    def get_scope(self):
        try:
            # H1 often provides a JSON version of the page if the Accept header is set
            response = requests.get(self.url, headers=self.headers, timeout=10)
            data = response.json()
            
            # Extracting the 'Structured Scopes'
            scope_items = data.get("structured_scopes", [])
            in_scope = []
            for item in scope_items:
                if item.get("eligible_for_bounty"):
                    in_scope.append(item.get("asset_identifier"))
            return in_scope
        except Exception as e:
            return [f"Error fetching scope: {str(e)}"]

# --- 2. UPDATED SIDEBAR (AUTO-PARSER) ---
with st.sidebar:
    st.title("🛡️ ROE & POLICY")
    h1_handle = st.text_input("H1 Program Handle", placeholder="e.g. 'starbucks'")
    
    if st.button("📖 READ & FOLLOW POLICY"):
        if h1_handle:
            scraper = H1Scraper(h1_handle)
            found_scope = scraper.get_scope()
            # Automatically update the Whitelist session state
            st.session_state.whitelist = ", ".join(found_scope)
            st.success(f"Loaded {len(found_scope)} Bounty-Eligible Assets!")
        else:
            st.error("Enter a handle first.")

    st.divider()
    # These now sync with the scraper results
    whitelist = st.text_area("🟢 WHITELIST", value=st.session_state.get('whitelist', ''))
    blacklist = st.text_area("🔴 BLACKLIST", ".gov, logout, delete")

# --- 3. THE "FOLLOW EVERYTHING" LOGIC ---
def run_autonomous_strike(target, time_limit_hours=8):
    # This loop follows 'everything it says' by checking the instructions
    # found in the policy for each asset.
    start = datetime.now()
    end = start + timedelta(hours=time_limit_hours)
    
    st.info(f"Initiating Autonomous Strike on {target}...")
    
    while datetime.now() < end and st.session_state.is_running:
        # Step 1: Deep Parameter Discovery (Arjun)
        # Step 2: AI Agent Vulnerability Check (Garak)
        # Step 3: Secret Leakage (Trufflehog)
        # Step 4: High-Signal Vuln Scan (Nuclei)
        
        # [INTERNAL CHECK]: If target is no longer in scope, HALT.
        if not is_in_scope(target, st.session_state.whitelist.split(","), []):
            st.error("CRITICAL: Target fell out of scope. Emergency Halt.")
            break
            
        time.sleep(600) # Wait 10 mins before looping to check for new subdomains
