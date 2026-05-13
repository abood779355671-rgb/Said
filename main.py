import requests
from bs4 import BeautifulSoup
import time
import re
from flask import Flask
from threading import Thread

# --- [بيانات الوصول الخاصة بك] ---
BOT_TOKEN = '8603037725:AAHZYBqg6zZHKKTWH_hsFKwrsDdvFnjj0qM'
GROUP_ID = '-1003436015737'

# --- [قائمة المواقع المستهدفة (تغطية عالمية)] ---
SOURCES = [
    "https://receive-sms-free.cc/",
    "https://sms24.me/en/countries/gb",
    "https://sms24.me/en/countries/us",
    "https://sms-online.co/receive-free-sms",
    "https://getfreesmsnumber.com/",
    "https://receive-smss.com/",
    "https://www.receivesms.co/",
    "https://temporary-phone-number.com/"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# خادم الويب للبقاء حياً (Render Keep-Alive)
app = Flask('')
@app.route('/')
def home(): return "Multi-Source Sniper is Active!"

def run_web(): app.run(host='0.0.0.0', port=8080)

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": GROUP_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True})
    except: pass

def global_scanner():
    known_numbers = set()
    send_alert("⚙️ **تم تفعيل المحرك الشامل**\nجاري مراقبة 8 مصادر عالمية للأرقام...")
    
    while True:
        for url in SOURCES:
            try:
                print(f"🔍 فحص مصدر: {url}")
                response = requests.get(url, headers=HEADERS, timeout=15)
                if response.status_code == 200:
                    # استخراج الأرقام الدولية باستخدام Regex
                    raw_text = response.text
                    numbers = re.findall(r'\+\d{7,15}', raw_text)
                    
                    for num in numbers:
                        if num not in known_numbers:
                            # بناء رسالة تنبيه احترافية
                            alert = (
                                f"🎯 **رقم جديد مرصود!**\n\n"
                                f"🔢 الرقم: `{num}`\n"
                                f"🌐 المصدر: {url.split('/')[2]}\n"
                                f"🔗 [رابط السحب المباشر]({url})\n\n"
                                f"⚡ استعمله الآن قبل الجميع!"
                            )
                            send_alert(alert)
                            known_numbers.add(num)
                time.sleep(2) # فاصل بسيط بين موقع وآخر لتجنب الحظر
            except:
                continue
        
        print("💤 دورة الفحص انتهت. استراحة قصيرة...")
        time.sleep(120) # إعادة الفحص الشامل كل دقيقتين

if __name__ == "__main__":
    Thread(target=run_web).start()
    global_scanner()
