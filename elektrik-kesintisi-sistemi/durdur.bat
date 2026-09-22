@echo off
echo Elektrik kesintisi takip sistemi (takip.py) sonlandiriliyor...
powershell -Command "Get-CimInstance Win32_Process -Filter \"name='pythonw.exe' OR name='python.exe'\" | Where-Object { $_.CommandLine -match 'takip.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1
echo.
echo Islem tamamlandi. Eger sistem arka planda calisiyorsa su an kapatildi.
pause
