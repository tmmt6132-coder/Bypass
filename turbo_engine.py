import requests, re, urllib3, time, threading, random, os, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# SSL Warning ပိတ်ရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# 🌐 GITHUB REMOTE CONFIG
# ===============================
GITHUB_USER = "tmmt6132-coder"
REPO_NAME = "Bypass"
# keys.txt raw link
URL_TO_KEYS = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/keys.txt"

def get_system_id():
    """စက်တစ်ခုချင်းစီအတွက် Unique ID ထုတ်ပေးခြင်း"""
    try:
        import hashlib
        # Termux environment ID ကို ယူခြင်း
        combined = str(os.getuid()) + os.environ.get('USER', 'unknown')
        return hashlib.md5(combined.encode()).hexdigest()[:10].upper()
    except:
        return "GET-ID-ERR"

def check_remote_approval():
    os.system('clear' if os.name == 'posix' else 'cls')
    sys_id = get_system_id()
    
    print(f"\033[95m╔════════════════════════════════════════╗\033[0m")
    print(f"\033[95m║       TURBO ENGINE ACCESS CONTROL      ║\033[0m")
    print(f"\033[95m╚════════════════════════════════════════╝\033[0m")
    print(f"\n[📡] Your System ID: \033[92m{sys_id}\033[0m")
    print("[*] Status: Checking authorization...")

    try:
        # ⚡ ချက်ချင်း Update ဖြစ်စေရန် Cache ကို ကျော်သည့်စနစ် (Cache-Buster)
        # URL အနောက်မှာ အချိန် (Timestamp) ကို parameter အနေနဲ့ ထည့်လိုက်တာပါ
        timestamp_buster = f"?t={int(time.time())}"
        response = requests.get(URL_TO_KEYS + timestamp_buster, timeout=10)
        
        if response.status_code != 200:
            print("\033[91m[!] Error: GitHub နှင့် ချိတ်ဆက်၍မရပါ။ (Check keys.txt link)\033[0m")
            return False
        
        lines = response.text.strip().splitlines()
        authorized = False
        expiry_info = ""

        for line in lines:
            line = line.strip()
            if "," not in line or line.startswith("#"): continue
            
            parts = line.split(',')
            allowed_id = parts[0].strip()
            expiry_str = parts[1].strip()
            
            if sys_id == allowed_id:
                expiry_date = datetime.strptime(expiry_str, '%Y-%m-%d')
                if datetime.now() < expiry_date:
                    authorized = True
                    expiry_info = expiry_str
                    break
                else:
                    print(f"\n\033[91m[!] သင့် ID သည် သက်တမ်းကုန်ဆုံးသွားပါပြီ ({expiry_str})\033[0m")
                    return False

        if authorized:
            print(f"\n\033[92m[✓] ACCESS GRANTED! (အသုံးပြုခွင့်ရရှိပါသည်)\033[0m")
            print(f"[*] Expiry Date: {expiry_info}")
            time.sleep(1.5)
            return True
        else:
            print(f"\n\033[93m[!] Status: Pending (အတည်ပြုချက် စောင့်ဆိုင်းနေဆဲ)\033[0m")
            print(f"------------------------------------------")
            print(f"သင့် ID: \033[92m{sys_id}\033[0m ကို Admin ထံသို့ ပေးပို့ပါ။")
            print(f"------------------------------------------")
            return False
            
    except Exception as e:
        print(f"\033[91m[!] Connection Error: {e}\033[0m")
        return False

# ===============================
# 🚀 BYPASS LOGIC (CORE ENGINE)
# ===============================
def start_process():
    """Bypass Engine ၏ လုပ်ဆောင်ချက်များ"""
    print(f"\n\033[96m[*] Initializing Ruijie Turbo Engine v2.5...\033[0m")
    
    # ဤနေရာတွင် ယခင်ကပေးထားသော Bypass logic (Requests, Threads, SID Extraction) များကို ဆက်လက်ထည့်သွင်းပါ
    # ဥပမာ-
    while True:
        try:
            # Monitoring Network...
            print(f"\r\033[94m[*] Engine Running... Sending Turbo Pulses\033[0m", end="")
            time.sleep(5)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    if check_remote_approval():
        try:
            start_process()
        except KeyboardInterrupt:
            print(f"\n\033[91m[!] Turbo Engine Stopped.\033[0m")
    else:
        sys.exit()
        
