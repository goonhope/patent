@echo off
title       =========CPCһ��������ֱ�ӣ�=========
echo     ��ʾ���ļ��追�������°�Ŀ¼������Ա����
echo    ==========goonhope@qq.com==========

::��ȡĿ¼
set root=%~dp0
set cpc="C:\Program Files (x86)\gwssi\CPC�ͻ���\"

::��Ȩ����
cacls %cpc% /e /g users:f
attrib %cpc%* -s -h -r /s
::rd /s /q "%cpc%Conversion"
cd %root%
call OffLineUpdate.exe

::ע�����
cd %cpc%
for %%i in (*.ocx gwssiSys.dll) do regsvr32 /s %%i
pause