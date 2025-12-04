@echo off
title [2] Kontrol Paneli GUI

:: Batch dosyasinin bulundugu klasore gec
cd /d "%~dp0"

echo =======================================================
echo    RADAR KONTROL PANELI (GUI)
echo =======================================================
echo.
echo Kontrol GUI'si aciliyor. Ana uygulama (radar_app.py) calisiyor olmali!
echo.

:: Python uygulamasini calistir. 'start' ve 'pythonw' kullanarak siyah CMD penceresinin cikmasini engelleriz.
start "" python radar_gui_control.py

echo.
echo Kontrol paneli baslatma komutu gonderildi.
echo Bu pencereyi simdi kapatabilirsiniz.
pause
exit