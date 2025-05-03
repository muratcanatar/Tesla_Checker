# Tesla Stok Takip ve Telegram Bildirim Botu

Bu Python scripti, [Tesla Türkiye Model Y stok sayfası](https://www.tesla.com/tr_tr/inventory/new/my)'nı düzenli olarak kontrol eder. Yeni araç stoğu tespit edildiğinde Telegram üzerinden anında bildirim gönderir. Ayrıca her kontrol zamanını ve sonucu bir log dosyasına kayıt eder.

---

## 🔧 Özellikler

-  Her 5 dakikada bir otomatik kontrol
-  Selenium + BeautifulSoup ile dinamik sayfa verisi çekimi
-  Zaman damgalı log kaydı: `log_history.jsonl`
-  Telegram uyarıları:
  - Yeni araç geldiğinde
  - Stok tamamen boş olduğunda

---

## 💻 Kurulum

### 1. Gerekli kütüphaneleri yükle:

pip install selenium webdriver-manager beautifulsoup4 schedule requests

### 2. Telegram botu oluştur:
@BotFather üzerinden /newbot komutuyla bir bot oluştur

Sana verilen Bot Token değerini kaydet

### 3. Chat ID’ni al:
@userinfobot ile sohbet başlat

Sana özel chat ID’yi al

### 4. tesla_stock_bot.py içinde aşağıdaki alanları doldur:

BOT_TOKEN = "senin_bot_tokenin"
CHAT_ID = "senin_chat_idin"

##### Log Dosyası
Script her çalıştırmada log_history.jsonl dosyasına şunu yazar:

{"timestamp": "2025-05-03 17:22:10", "stock": ["stok boş"]}
veya:
{"timestamp": "2025-05-03 17:27:10", "stock": ["Model Y Performance", "₺1.970.000"]}
