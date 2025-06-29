# file_scanner.py

import hashlib
import os

# Example: Fake blacklist of known dangerous file hashes
blacklisted_hashes = {
    # Just for demo. Add real hashes if needed.
    "e99a18c428cb38d5f260853678922e03",  # fake md5
    "098f6bcd4621d373cade4e832627b4f6",
}

# File extensions commonly used for malware
suspicious_extensions = ['.exe', '.bat', '.vbs', '.scr', '.cmd', '.js', '.ps1']

def calculate_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        return None

def is_suspicious_file(file_path):
    _, ext = os.path.splitext(file_path)
    file_hash = calculate_md5(file_path)

    if file_hash in blacklisted_hashes:
        return "❌ File matches known malicious signature!"

    if ext.lower() in suspicious_extensions:
        return f"⚠️ Suspicious file extension detected: {ext}"

    return "✅ File appears safe."

