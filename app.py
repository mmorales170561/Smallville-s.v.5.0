import streamlit as st
import requests
import random

# --- 1. SENSITIVE FILE FINDER (NEW) ---
def find_sensitive_files(target_url):
    """
    Scans for 'Leftover' files that developers forget to delete.
    These often contain the 'Keys to the Kingdom'.
    """
    wordlist = [
        "/.env", "/.git/config", "/config.php.bak", "/.vscode/settings.json",
        "/phpinfo.php", "/.htaccess", "/backup.sql", "/.aws/credentials"
    ]
    results = []
    for path in wordlist:
        try:
            # Ghost Mimicry: Randomized User-Agent
            url = f"{target_url.rstrip('/')}{path}"
            r = requests.get(url, timeout=5, allow_redirects=False)
            if r.status_code == 200:
                results.append(f"🔥 EXPOSED: {url} (Size: {len(r.content)} bytes)")
        except:
            pass
    return results

# --- 2. UPDATED INTERFACE ---
t1, t2, t3, t4, t5 = st.tabs(["🚀 STRIKE", "📡 RADAR", "📂 FILE FINDER", "🧪 IDOR LAB", "📄 REPORTER"])

with t3:
    st.header("Sensitive File Finder")
    st.info("Searching for .env, .git, and backup configs on your targets.")
    if st.session_state.get('found_subs'):
        target_to_mine = st.selectbox("Select Subdomain to Mine", st.session_state.found_subs)
        if st.button("⛏️ START DEEP EXCAVATION"):
            hits = find_sensitive_files(f"https://{target_to_mine}")
            if hits:
                for h in hits: st.error(h)
            else:
                st.write("No common sensitive files found via simple GET.")
    else:
        st.info("Run Subdomain Radar first.")

with t4:
    st.header("IDOR Lab (Blind/Single-User Mode)")
    
    # Toggle for Blind IDOR
    is_blind = st.checkbox("Run without User A/B Cookies (Blind Mode)")
    
    manual_target = st.text_input("Endpoint URL", "https://api.target.com/v1/user/1001")
    
    if is_blind:
        st.warning("⚠️ BLIND MODE: Testing if this endpoint is public (No Authentication).")
        if st.button("⚡ EXECUTE BLIND PROBE"):
            r = requests.get(manual_target)
            st.code(f"HTTP {r.status_code}\n{r.text[:500]}", language="json")
            if r.status_code == 200:
                st.error("🚨 CRITICAL: Endpoint is PUBLIC. This is a massive information leak.")
    else:
        st.info("Switching to Authenticated IDOR. Ensure Cookies are set in Sidebar.")
