import os
import time
import platform
import subprocess
import logging
import logging.handlers
import socket
import sys
import atexit

# ================= AYARLAR =================
MODEM_IP = "192.168.1.1" 
KONTROL_ARALIGI = 10 
BASARISIZ_DENEME_SINIRI = 12 # 10 sn x 12 = 2 dakika tolerans
# ===========================================

# İşletim sistemi bir kez hesaplanır (çalışırken değişmez)
IS_WINDOWS = platform.system().lower() == 'windows'

# Loglama Ayarları: Aynı klasörde 'elektrik_log.txt' dosyası oluşturur.
# RotatingFileHandler: Max 1 MB, en fazla 3 eski dosya saklanır (elektrik_log.txt.1, .2, .3)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DOSYASI = os.path.join(SCRIPT_DIR, "elektrik_log.txt")

logger = logging.getLogger("elektrik_takip")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    LOG_DOSYASI, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(handler)

# Windows için CMD ekranı gizleme ayarı (bir kez oluşturulur, her ping'de tekrar kullanılır)
_startupinfo = None
if IS_WINDOWS:
    _startupinfo = subprocess.STARTUPINFO()
    _startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    _startupinfo.wShowWindow = 0  # SW_HIDE

def ping_test(ip):
    try:
        komut = ['ping', '-n' if IS_WINDOWS else '-c', '1']
        
        # Modem kapandığında hemen sonuç almak için zaman aşımı sürelerini düşük tutuyoruz
        if IS_WINDOWS:
            komut.extend(['-w', '1000', ip])
        else:
            komut.extend(['-W', '1', ip])
            
        sonuc = subprocess.run(
            komut,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            startupinfo=_startupinfo,  # Windows'ta pencere açılmasını engeller
            timeout=5  # Ping takılırsa 5 saniye sonra zaman aşımına uğrar
        )
        return sonuc.returncode == 0
    except subprocess.TimeoutExpired:
        logger.warning("Ping zaman asimina ugradi (5 sn)")
        return False
    except Exception as e:
        logger.error(f"Ping atarken hata olustu: {e}")
        return False

def sistemi_kapat():
    logger.warning("Elektrik kesintisi kesinlesti (Tolerans suresi asildi). Sistem kapatiliyor!")
    
    # Son logların diske yazıldığından emin ol (kapanma anında kaybolmasın)
    for h in logger.handlers:
        h.flush()
    
    if IS_WINDOWS:
        # Onay istemeden ve beklemeden bilgisayarı anında kapatır (/f ile zorlar, /t 0 ile süreyi sıfırlar).
        subprocess.run(
            ['shutdown', '/s', '/f', '/t', '0'],
            startupinfo=_startupinfo
        )
    else:
        subprocess.run(
            ['shutdown', '-h', '+1', 'Elektrik kesintisi sebebiyle sistem kapatiliyor!']
        )

def sesli_uyari():
    # Sadece Windows'ta çalışır, PC başındaysanız kedi sesi ile uyarır
    if IS_WINDOWS:
        try:
            import winsound
            wav_path = os.path.join(SCRIPT_DIR, "kedi_sesi.wav")
            if os.path.exists(wav_path):
                winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                winsound.Beep(1000, 500) # Ses dosyası yoksa bip ile uyar
        except Exception:
            pass

def main():
    # --- Çoklu Kopya Engelleme (Singleton Lock) ---
    global _lock_socket
    try:
        _lock_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _lock_socket.bind(("127.0.0.1", 60321))
    except socket.error:
        # Port doluysa (zaten çalışıyorsa) bu kopyayı anında sessizce sonlandır
        sys.exit(0)
    
    # Program kapandığında soketi temizle (portu serbest bırak)
    def temizle():
        try:
            _lock_socket.close()
        except Exception:
            pass
    atexit.register(temizle)
    # ----------------------------------------------

    logger.info("--- Elektrik kesintisi takip sistemi BASLATILDI ---")
    print("Elektrik kesintisi takip sistemi baslatildi. Loglar:", LOG_DOSYASI)
    
    # Aşama 1: PC ilk açıldığında modemin açılmasını ve ilk bağlantıyı bekle
    while not ping_test(MODEM_IP):
        time.sleep(5)
    logger.info("Modem ile ilk baglanti kuruldu. Izleme dongusu basliyor...")

    basarisiz_deneme = 0
    kesinti_durumu = False # Sadece ilk koptuğunda log/ses atmak için

    # Aşama 2: Arka plan izleme döngüsü
    while True:
        if ping_test(MODEM_IP):
            if kesinti_durumu:
                # Modem geri geldiyse logla ve durumu sıfırla
                gecen_sure = basarisiz_deneme * KONTROL_ARALIGI
                logger.info(f"Modem baglantisi geri geldi! Kesinti/Dalgalanma suresi: ~{gecen_sure} saniye.")
                kesinti_durumu = False
                
            basarisiz_deneme = 0 # Bağlantı başarılı, sayacı sıfırla
        else:
            basarisiz_deneme += 1 # Bağlantı yok, sayacı artır
            
            if not kesinti_durumu:
                logger.warning("Modem baglantisi KOPTU! Dalgalanma veya elektrik kesintisi olabilir. Sayac baslatildi.")
                kesinti_durumu = True
                sesli_uyari()
                
            # Kapanmaya 30 saniye kala (3 deneme) tekrar uyar
            kalan_deneme = BASARISIZ_DENEME_SINIRI - basarisiz_deneme
            if kalan_deneme == 3:
                sesli_uyari()
                
            # Sınır aşıldıysa kapat
            if basarisiz_deneme >= BASARISIZ_DENEME_SINIRI:
                sesli_uyari()  # Son bir kez daha uyar
                sistemi_kapat()
                break
                
        time.sleep(KONTROL_ARALIGI)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Beklenmeyen bir çökme olursa logla ki bilgisayar sessizce korumasız kalmasın
        logger.critical(f"Takip sistemi beklenmeyen bir hata ile COKTU: {e}", exc_info=True)
        sys.exit(1)
