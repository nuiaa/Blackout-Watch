# GridPing (Power Outage Monitor) ⚡

*🌍 [Türkçe sürüm için aşağıya kaydırın](#türkçe-sürüm)*

> A lightweight script that safely shuts down your PC during a power outage. By monitoring your router's network status, it eliminates the need for a direct data connection between your UPS/PSU and your computer.

Even if your PC is connected to an Uninterruptible Power Supply (UPS), detecting a power outage is difficult if the UPS cannot communicate directly with the PC (e.g., via USB). This system elegantly solves this by **monitoring your router's internet connection (ping)**. Since routers usually lose power immediately during an outage, the script indirectly but accurately detects blackouts and safely shuts down your computer.

## Features

- **🔌 UPS Friendly:** No need for a physical data cable between your UPS and PC.
- **🐈 Fun Audio Warnings:** Instead of boring system beeps, you get warned by a cat meowing sound (`kedi_sesi.wav`) when a blackout is detected.
- **👻 Silent Background Execution:** Runs completely in the background without any annoying CMD windows or popups.
- **🛡️ Fault Tolerance (Surge Protection):** Brief network drops or router restarts won't cause false alarms. It has a default tolerance window of 2 minutes.
- **📝 Detailed Logging:** Records the exact timestamps of power losses and restorations into `elektrik_log.txt`.
- **🧹 Singleton Lock:** Smart lock mechanism prevents the script from running multiple times accidentally.

## Installation & Usage

You need to have [Python](https://www.python.org/downloads/) installed on your system. *(Make sure to check "Add Python to PATH" during installation).*

1. Download the files to your computer.
2. Double-click the **`baslat.vbs`** file to start the monitor. 
   *(It will start running silently in the background.)*
3. If you want to stop the system, simply double-click the **`durdur.bat`** file.

### How to Test:
While the system is running, turn off your router (or unplug its power). As it approaches the tolerance limit, the system will warn you with cat meows and eventually shut down your computer safely.

## Advanced Settings

You can change the system's behavior by opening `takip.py` in a text editor:

```python
# ================= SETTINGS =================
MODEM_IP = "192.168.X.X"        # Your router's IP address (e.g. 192.168.1.1)
KONTROL_ARALIGI = 10            # Ping interval in seconds
BASARISIZ_DENEME_SINIRI = 12    # Tolerance before shutdown (10s x 12 = 2 minutes)
# ============================================
```

---
---

# Türkçe Sürüm 🇹🇷

> Bilgisayarınızı elektrik kesintilerinde güvenle kapatan hafif bir arka plan betiği. Yönlendiricinizin (modeminizin) ağ durumunu izleyerek, UPS/PSU'nuz ile bilgisayarınız arasında doğrudan bir veri bağlantısına olan ihtiyacı ortadan kaldırır.

Bilgisayarınız bir Kesintisiz Güç Kaynağına (UPS) bağlı olsa bile, UPS'in bilgisayarla doğrudan (USB vb. ile) haberleşemediği durumlarda elektrik kesintisini tespit etmek zordur. Bu sistem, **modeminizin ağ bağlantısını (ping)** izleyerek elektrik kesintilerini dolaylı yoldan, ama büyük bir kesinlikle tespit eder ve bilgisayarınızı güvenle kapatır.

## Özellikler

- **🔌 UPS Dostu:** UPS'iniz ile bilgisayarınız arasında veri kablosu olmasına gerek yoktur.
- **🐈 Eğlenceli Sesli Uyarılar:** Elektrik kesintisi tespit edildiğinde sıkıcı bip sesleri yerine bilgisayarınızdan kedi miyavlaması duyarsınız (`kedi_sesi.wav`).
- **👻 Arka Planda Sessizce Çalışır:** CMD penceresi veya rahatsız edici bir arayüz yoktur, tamamen arka planda izleme yapar.
- **🛡️ Hata Toleransı (Dalgalanma Koruması):** Anlık kopmalar veya modem yeniden başlatmaları yanlış alarm vermez. Varsayılan olarak 2 dakikalık bir tolerans süresi vardır.
- **📝 Detaylı Loglama:** Elektriğin tam olarak ne zaman gidip geldiğini `elektrik_log.txt` dosyasına kaydeder.
- **🧹 Çoklu Çalışma Koruması:** Sistemi yanlışlıkla birden fazla kez açsanız bile, kendi içinde tek bir kopya olarak çalışmasını sağlayan akıllı kilit (singleton lock) mekanizması vardır.

## Kurulum ve Kullanım

Sistemin çalışması için bilgisayarınızda [Python](https://www.python.org/downloads/) yüklü olmalıdır. *(Kurulum sırasında "Add Python to PATH" seçeneğini işaretlemeyi unutmayın.)*

1. Dosyaları bilgisayarınıza indirin.
2. Sistemi başlatmak için **`baslat.vbs`** dosyasına çift tıklayın. 
   *(Arka planda sessizce çalışmaya başlayacaktır.)*
3. Sistemi durdurmak isterseniz **`durdur.bat`** dosyasına çift tıklayın.

### Test Etmek İçin:
Sistem çalışırken modeminizi kapatın (veya fişini çekin). Belirlenen tolerans süresine yaklaştıkça sistem size miyavlama sesleriyle uyarı verecek ve sürenin sonunda bilgisayarınızı güvenli bir şekilde kapatacaktır.

## Ayarlar (Gelişmiş)

`takip.py` dosyasını bir metin editörü ile açarak sistemin davranışlarını değiştirebilirsiniz:

```python
# ================= AYARLAR =================
MODEM_IP = "192.168.X.X"        # Kendi modem IP'nizi buraya yazin (Orn: 192.168.1.1)
KONTROL_ARALIGI = 10            # Kaç saniyede bir kontrol edileceği
BASARISIZ_DENEME_SINIRI = 12    # Kapatılmadan önceki tolerans (10sn x 12 = 2 dakika)
# ===========================================
```

---
*Note: This system is optimized for Windows operating systems (Audio alerts and shutdown commands are Windows-specific).*
