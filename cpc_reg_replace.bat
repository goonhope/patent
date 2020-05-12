@echo off
echo 文件放到cpc安装目录

::获取文件目录
set cpcdir=%~dp0
set cpczipdir=%cpcdir:CPC客户端\=%
for /f "tokens=*" %%i in ('dir  /b /s "%cpczipdir%"cpc.zip') do set cpczip=%%~fi
set update=%cpcdir:CPC客户端\=E系统(EES)升级程序\update\updateSipo.exe%
echo %cpczipdir% %cpczip%
pause

::组件升级
call "%update%"

::判断winrar是否安装并替换CPC
reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\ | find /i "rar">nul 2>nul
if %errorlevel% equ 0 (start winrar x "%cpczip%" /o+ ) else (echo replace manually)

::注册组件
::cd %~dp0
for %%i in (*.ocx) do  regsvr32 "%%~fi"
echo regsvr32 /s gwssiSys.dll

::错误时删除后台word进程
for /f "tokens=2 delims= " %%i in ('tasklist ^|find "winword" /i') do echo taskkill /pid %%i /f
pause
