@echo off
echo 需安装 ImageMagick & ghostscript,并加入path；本文件放到pdf文件目录运行(a4)
for %%i in (*.pdf) do magick convert -density 300 -quality 100 %%i %%~ni_%03d.jpg
echo sleep 5s && timeout /t 5 /nobreak >nul
::ping -n 10 127.0.0.1 > nul or choice /N /C y /T 5 /D y >nul
::获取缩放比例
for /f "tokens=3 delims=x " %%i in ('magick identify *.jpg') do set /a scale=620*100/%%i && cls
if not exist done md done 
::for %%i in (*.jpg) do magick convert -resize 25% %%i done\%%i
for %%i in (*.jpg) do magick convert -resize %scale%% %%i done\%%i
::for %%i in (%%~dp0*.jpg) do magick convert -resize %scale%% %%~fi %%~dp0done\%%~nxi
