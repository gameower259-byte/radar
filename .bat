@echo off
title [1] Ana Radar Uygulamasi (SERVER)
cls

:: Batch dosyasinin bulundugu klasore gec
cd /d "%~dp0"

echo =======================================================
echo    ANA RADAR GORSELLESTIRICI VE KILITLEME SERVER
echo =======================================================
echo LUTFEN BU PENCEREYI KAPATMAYIN.
echo Uygulama acilmazsa, hata mesajini kontrol edin.
echo.

:: Python uygulamasini calistir
python radar_app.py

:: Hata olsa da olmasa da pencerenin kapanmasini engelle
echo.
echo =======================================================
echo Uygulama Durdu. Hata varsa yukarida gorunur. Devam etmek icin bir tusa basin...
pause