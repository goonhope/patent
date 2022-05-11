@echo off
echo    =====================CPC一键升级======================
echo          提示：文件需拷贝到updatPackage目录并管理员运行
echo    ===============goonhope@gmail.com====================

::获取目录
set root=%~dp0
set cpc="C:\Program Files (x86)\gwssi\CPC客户端\"
set oldpath=%PATH%
echo %PATH% | find "winrar" /i >nul || PATH %PATH%;"C:\Program Files\WinRAR";"C:\Program Files\7-Zip"

::判断更新 if %errorlevel% equ 0
cd %root%
echo %root% | find "updatpackage" /i >nul 2>nul && (
for %%i in (*.zip) do (winrar x %%i %cpc% /o+ ||7z x -y %%i -o%cpc% || echo @info:  无解压软件 )
for %%i in (*.exe) do call %%i
) || echo @info: 拷贝到updatPackage目录在运行
pause

::注册组件
cd %cpc%
for %%i in (*.ocx gwssiSys.dll) do regsvr32 /s %%i
pause

::赋权运行
::(cacls %cpc% /e /g users:f
attrib %cpc%* -s -h -r /s
cd %root:updatPackage=%
call OffLineUpdate.exe)
