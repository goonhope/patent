@echo off
title   ===========CPC一键升级（直接）==========
echo     提示：文件需拷贝到更新包目录并管理员运行
echo    ============goonhope@qq.com===========

::获取目录
set root=%~dp0
set cpc="C:\Program Files (x86)\gwssi\CPC客户端\"
set cpca=%cpc:端\=端\*%
set cpcc=%cpc:端\=端\Conversion%

::赋权更新
cacls %cpc% /e /g %username%:f
attrib %cpca% -s -h -r /s
::rd /s /q cpcc
cd %root%
call OffLineUpdate.exe

::注册组件
cd %cpc%
for %%i in (*.ocx gwssiSys.dll) do regsvr32 /s %%i
pause
