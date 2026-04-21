import requests, re, urllib3, time, threading, random, os, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# 🌐 REMOTE KEY CONFIG
# ===============================
# သင့် GitHub Username နဲ့ Repo နာမည်ကို ဒီနေရာမှာ အစားထိုးပါ
GITHUB_USER = "tmmt6132-coder"
REPO_NAME = "Bypass"
URL_TO_KEYS = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/keys.txt"

def get_system_id():
    try:
        import hashlib
        # စက်ရဲ့ unique အချက်အလက်ကို ယူခြင်း
        return hashlib.md5(os.uname().nodename.encode()).hexdigest()[:10].upper()
    except:
        return "USER-DEFAULT-01"

def check_remote_approval():
    os.system('clear' if os.name == 'posix' else 'cls')
    sys_id = get_system_id()
    
    print(f"\033[95m╔════════════════════════════════════════╗\033[0m")
    print(f"\033[95m║       REMOTE KEY APPROVAL SYSTEM       ║\033[0m")
    print(f"\033[95m╚════════════════════════════════════════╝\033[0m")
    print(f"\n[*] Your System ID: \033[92m{sys_id}\033[0m")
    print("[*] Checking access from server...")

    try:
        response = requests.get(URL_TO_KEYS, timeout=10)
        if response.status_code != 200:
            print("\033[91m[!] Server Error: မူရင်း Key ဖိုင်ကို ရှာမတွေ့ပါ။\033[0m")
            return False
        
        auth_data = response.text.splitlines()
        for line in auth_data:
            if line.startswith("#") or not line.strip(): continue
            
            # ID နဲ့ ရက်စွဲကို ခွဲထုတ်ခြင်း (ဥပမာ: ADMIN-TEST,2026-05-30)
            parts = line.split(',')
            if len(parts) == 2:
                allowed_id = parts[0].strip()
                expiry_str = parts[1].strip()
                
                if sys_id == allowed_id:
                    expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d')
                    if datetime.now() < expiry_date:
                        print(f"\n\033[92m[✓] ACCESS GRANTED!\033[0m")
                        print(f"[*] Expires on: {expiry_str}")
                        time.sleep(2)
                        return True
                    else:
                        print(f"\n\033[91m[!] STATUS: EXPIRED ({expiry_str})\033[0m")
                        return False

        print(f"\n\033[91m[!] STATUS: NOT AUTHORIZED\033[0m")
        print(f"[*] ကျေးဇူးပြု၍ Admin ဆီမှာ ID သွားပေးပါ။")
        return False
    except Exception as e:
        print(f"\033[91m[!] Connection Error: {e}\033[0m")
        return False

# ===============================
# 🚀 CORE ENGINE
# ===============================
def run_bypass_engine():
    # ဒီနေရာမှာ အရင်ကပေးထားတဲ့ Bypass Logic အပြည့်အစုံကို ထည့်ပါ
    print("\n\033[96m[+] Initializing Turbo Engine Logic...\033[0m")
    # start_process() logic များ ဤနေရာတွင် ရှိရမည်

if __name__ == "__main__":
    if check_remote_approval():
        run_bypass_engine()
    else:
        print("\n\033[93m[!] Program Terminated.\033[0m")
        sys.exit()
        
