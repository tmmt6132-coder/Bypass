import requests, re, urllib3, time, threading, random, os, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# 🌐 CONFIGURATION
# ===============================
GITHUB_USER = "tmmt6132-coder"
REPO_NAME = "Bypass"
# keys.txt ထဲမှာ ID,YYYY-MM-DD ပုံစံနဲ့ သိမ်းရပါမယ်
URL_TO_KEYS = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/keys.txt"

def get_system_id():
    """စက်တစ်ခုချင်းစီအတွက် Unique ID ထုတ်ပေးခြင်း"""
    try:
        import hashlib
        # User ID နဲ့ Username ကိုသုံးပြီး ဖုန်းတစ်လုံးစီအတွက် ID တစ်ခုတည်းထွက်အောင်လုပ်ခြင်း
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
        # GitHub ကနေ list ကို ဆွဲယူမယ် (Cache မငြိအောင် v parameter ထည့်ထားသည်)
        response = requests.get(f"{URL_TO_KEYS}?v={random.randint(1,9999)}", timeout=10)
        
        if response.status_code != 200:
            print("\033[91m[!] Error: မူရင်း Key စာရင်းကို ချိတ်ဆက်၍မရပါ။\033[0m")
            return False
        
        lines = response.text.strip().splitlines()
        authorized = False
        expiry_info = ""

        for line in lines:
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
            print(f"\n\033[92m[✓] အသုံးပြုခွင့်ရရှိပါသည် (Access Granted)\033[0m")
            print(f"[*] သက်တမ်းကုန်ဆုံးရက်: {expiry_info}")
            time.sleep(1.5)
            return True
        else:
            # စာရင်းထဲမှာ ID မရှိရင် ဒီစာသားကို ပြပါမယ်
            print(f"\n\033[93m[!] Status: တန်းစီဇယားတွင် စောင့်ဆိုင်းနေဆဲဖြစ်သည် (Pending)\033[0m")
            print(f"------------------------------------------")
            print(f"သင့် ID: \033[92m{sys_id}\033[0m ကို Admin ထံသို့ ပေးပို့ပါ။")
            print(f"Admin က အတည်ပြုပေးပြီးမှ သုံး၍ရပါမည်။")
            print(f"------------------------------------------")
            return False
            
    except Exception as e:
        print(f"\033[91m[!] Connection Error: {e}\033[0m")
        return False

# ===============================
# 🚀 CORE ENGINE (BYPASS LOGIC)
# ===============================
def start_bypass_engine():
    # အရင်ကပေးထားတဲ့ Bypass Logic အပြည့်အစုံကို ဒီနေရာမှာ ထည့်ပါ
    print("\n\033[96m[*] Ruijie/Captive Portal Engine Loading...\033[0m")
    # ပုံစံအသစ် Banner ပြခြင်း
    print(f"\033[94m[+] Engine Version: 2.5 (Premium)\033[0m")
    
    # ဤနေရာတွင် logic များ ဆက်လက်ရေးသားရန်...
    # (ဥပမာ- start_process() function တစ်ခုလုံးကို ဒီမှာ ပြန်ကူးထည့်နိုင်ပါတယ်)

if __name__ == "__main__":
    if check_remote_approval():
        start_bypass_engine()
    else:
        print(f"\n\033[90m[#] Exit code: 0.1\033[0m")
        sys.exit()
            
