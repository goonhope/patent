@echo off
title       =========CPCһ��������winrar��=========
echo    =================================
echo     ��ʾ���ļ��追����updatPackageĿ¼������Ա����
echo    ==========goonhope@gmail.com=========

::��ȡ�ļ�Ŀ¼
set root=%~dp0
set cpc="C:\Program Files (x86)\gwssi\CPC�ͻ���\"
cd %root%

::�ж�Ŀ¼����
echo %root% | find "updatpackage" /i >nul 2>nul
if %errorlevel% equ 0 (
for %%i in (*.zip) do ( echo winrar x %%i %cpc% /o+ || echo 7z x -y %%i -o%cpc% || echo @info:  �޽�ѹ��� )
for %%i in (*.exe) do echo call %%i) else (echo �ļ�����updatPackageĿ¼)

pause
