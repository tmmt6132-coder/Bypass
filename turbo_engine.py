import requests
import re
import urllib3
import time
import threading
import os
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIG (GITHUB RAW URL သေချာစစ်ပါ)
# ===============================
GITHUB_RAW_URL = "https://raw.githubusercontent.com/tmmt6132-coder/Bypass/main/keys.txt"

# --- COLORS ---
RED = "\033[91m"; GREEN = "\033[92m"; CYAN = "\033[96m"
YELLOW = "\033[93m"; MAGENTA = "\033[95m"; RESET = "\033[0m"

def get_system_key():
    """သင့်ဖုန်းရဲ့ Key ကို ထုတ်ယူခြင်း (e.g., u0_a321)"""
    try:
        import subprocess
        whoami = subprocess.check_output("whoami", shell=True).decode().strip()
        return whoami
    except:
        return os.environ.get('USER', 'unknown')

def check_approval():
    os.system('clear')
    my_key = get_system_key()
    
    print(f"{CYAN}╔════════════════════════════════════════╗")
    print(f"║      ADVANCED KEY & EXPIRY SYSTEM      ║")
    print(f"╚════════════════════════════════════════╝{RESET}")
    print(f"\n[*] Checking Key: {YELLOW}{my_key}{RESET}")

    try:
        # GitHub ကနေ key list ကို ဆွဲယူမယ်
        res = requests.get(GITHUB_RAW_URL, timeout=10)
        if res.status_code == 200:
            lines = res.text.strip().split('\n')
            
            for line in lines:
                if not line.strip(): continue
                
                # Line တစ်ကြောင်းလုံးမှာ သင့် Key (u0_a321) ပါသလား စစ်မယ်
                if my_key in line:
                    parts = line.split(':')
                    # ပုံမှန်အားဖြင့် format က Name:Date:Key ဆိုရင် parts[1] က Date ဖြစ်မယ်
                    expiry_str = parts[1] if len(parts) > 1 else "2030-01-01"

                    try:
                        expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d')
                        if datetime.now() < expiry_date:
                            print(f"{GREEN}[✓] ACCESS GRANTED!{RESET}")
                            print(f"{CYAN}[i] Expired on: {expiry_str}{RESET}")
                            time.sleep(2)
                            return True
                        else:
                            print(f"{RED}[X] KEY EXPIRED! ({expiry_str}){RESET}")
                            return False
                    except:
                        # Date format မှားနေရင်လည်း Key ပါရင် ပေးသုံးမယ်
                        return True
            
            print(f"{RED}[X] KEY NOT FOUND IN DATABASE!{RESET}")
            print(f"{YELLOW}Admin ကို သင့် Key ({my_key}) ပေးပြီး အခွင့်တောင်းပါ။{RESET}")
            return False
    except:
        print(f"{RED}[!] Server Connection Error!{RESET}")
        return False

def start_main():
    """ဒီနေရာမှာ Voucher Brute Force နဲ့ တခြား function တွေ ထည့်ပါ"""
    print(f"\n{MAGENTA}Starting Ruijie Bypass Engine...{RESET}")
    # ရှေ့မှာပေးခဲ့တဲ့ Brute force code များကို ဤနေရာတွင် ဆက်ရေးနိုင်သည်

if __name__ == "__main__":
    if check_approval():
        start_main()
        
