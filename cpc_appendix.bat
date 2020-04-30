@echo off
echo 需安装ImagicMagick & ghostscript,
md new
for %%i in (*.pdf) do magick convert -density 300 -quality 100 %%i %%~ni_%03d.jpg
echo sleep 5
ping 8.8.8.8 -n 10
if not exist done md done 
for %%i in (*.jpg) do magick convert -resize 25% %%i done\%%~ni.jpg
