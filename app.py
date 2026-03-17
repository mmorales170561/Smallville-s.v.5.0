def prime_armory():
    URLS = {
        "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip",
        "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.6.4/httpx_1.6.4_linux_amd64.zip",
        "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.2.9/nuclei_3.2.9_linux_amd64.zip",
        "katana": "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip",
        "airix": "https://github.com/projectdiscovery/airix/releases/download/v0.0.3/airix_0.0.3_linux_amd64.zip"
    }
    
    os.makedirs(BIN_PATH, exist_ok=True)
    status_area = st.sidebar.empty()
    
    for name, url in URLS.items():
        try:
            status_area.info(f"Downloading {name}...")
            response = requests.get(url, timeout=30)
            file_data = io.BytesIO(response.content)
            target_file = os.path.join(BIN_PATH, name)

            # --- STRATEGY 1: ZIP ---
            if zipfile.is_zipfile(file_data):
                with zipfile.ZipFile(file_data) as z:
                    for f in z.namelist():
                        if f.endswith(name):
                            with open(target_file, "wb") as b:
                                b.write(z.read(f))
            
            # --- STRATEGY 2: TAR/GZIP ---
            else:
                file_data.seek(0)
                try:
                    # Try as GZIP first, then as raw TAR
                    mode = "r:gz" if url.endswith("gz") else "r:"
                    with tarfile.open(fileobj=file_data, mode=mode) as t:
                        for member in t.getmembers():
                            if member.name.endswith(name):
                                content = t.extractfile(member).read()
                                with open(target_file, "wb") as b:
                                    b.write(content)
                except:
                    # --- STRATEGY 3: DIRECT BINARY ---
                    # If all else fails, the download itself IS the binary
                    file_data.seek(0)
                    with open(target_file, "wb") as b:
                        b.write(file_data.read())
            
            # Force Linux Execution Permissions
            if os.path.exists(target_file):
                os.chmod(target_file, 0o755)
                st.sidebar.success(f"✓ {name} Loaded")
            else:
                st.sidebar.error(f"✗ {name} Not Found in Archive")
                
        except Exception as e:
            st.sidebar.error(f"Err {name}: {e}")
    status_area.empty()
