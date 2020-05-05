@echo off
echo 需安装 ImageMagick & ghostscript；本文件放到pdf文件目录运行(a4)
for %%i in (*.pdf) do magick convert -density 300 -quality 100 %%i %%~ni_%03d.jpg
echo sleep 5s && timeout /t 5 /nobreak >nul
::ping -n 10 127.0.0.1 > nul or choice /N /C y /T 5 /D y >nul
if not exist done md done 
for %%i in (*.jpg) do magick convert -resize 25% %%i done\%%i
