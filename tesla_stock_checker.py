import os
import json
import time
import schedule
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# TELEGRAM BİLGİLERİNİ BURAYA GİR
BOT_TOKEN = "-------"
CHAT_ID = "-------"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Telegram mesajı gönderildi.")
        else:
            print("Telegram hatası:", response.text)
    except Exception as e:
        print("Telegram bağlantı hatası:", e)

def fetch_stock_items():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://www.tesla.com/tr_tr/inventory/new/my"
    print("Sayfa açılıyor...")
    driver.get(url)
    time.sleep(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all(["h1", "h2", "span", "div"])

    results = []
    for t in titles:
        text = t.get_text(strip=True)
        if "Model" in text or "₺" in text:
            results.append(text)

    return results

def load_previous_stock(path="stock_log.json"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_current_stock_with_timestamp(stock_list, path="log_history.jsonl"):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stock": stock_list
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def compare_stocks(old, new):
    return [item for item in new if item not in old]

def run_check():
    print("\n Stok kontrolü başlatıldı...")
    current_stock = fetch_stock_items()
    previous_stock = load_previous_stock()
    new_items = compare_stocks(previous_stock, current_stock)

    if not current_stock:
        print("Araç bulunamadı (stok boş). Zamanlı log yapılıyor.")
        save_current_stock_with_timestamp(["stok boş"])
        send_telegram("🔍 Tesla stok kontrolü yapıldı: Şu anda stokta araç bulunamadı.")
        return


    if new_items:
        print("Yeni araç(lar) bulundu:")
        message = "🚘 Yeni Tesla araçları tespit edildi:\n"
        for item in new_items:
            print("•", item)
            message += f"• {item}\n"
        send_telegram(message)
    else:
        print("Değişiklik yok, stok aynı.")

    save_current_stock_with_timestamp(current_stock)


schedule.every(5).minutes.do(run_check)

print("⏱Tesla stok takip botu başlatıldı. 5 dakikada bir kontrol edilecek.")
run_check()  


while True:
    schedule.run_pending()
    time.sleep(1)
