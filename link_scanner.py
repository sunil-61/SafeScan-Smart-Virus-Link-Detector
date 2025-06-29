# link_scanner.py

import re

# Basic suspicious patterns (customizable)
suspicious_patterns = [
    r"(free|bonus|offer|click|win)[\-_.]?(now|gift|money|cash)",
    r"login\.(?![a-z]*\.(com|net|org))",  # fake login subdomains
    r"(account|security|bank)[\-_.]?(alert|warning)",
    r"(bit\.ly|tinyurl\.com|t\.co|goo\.gl)",  # shortened URLs
    r"[^\s]+@[^\.]+\.(ru|cn|tk|top|xyz)"      # sketchy TLDs or email traps
]

def is_suspicious_url(url):
    url = url.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, url):
            return True
    return False

