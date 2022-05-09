@echo off
title       =========CPC一键升级（winrar）=========
echo    =================================
echo     提示：文件需拷贝到updatPackage目录并管理员运行
echo    ==========goonhope@gmail.com=========

::获取文件目录
set root=%~dp0
set cpc="C:\Program Files (x86)\gwssi\CPC客户端\"
cd %root%

::判断目录更新
echo %root% | find "updatpackage" /i >nul 2>nul
if %errorlevel% equ 0 (
for %%i in (*.zip) do ( echo winrar x %%i %cpc% /o+ || echo 7z x -y %%i -o%cpc% || echo @info:  无解压软件 )
for %%i in (*.exe) do echo call %%i) else (echo 文件不在updatPackage目录)

pause
