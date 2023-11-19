echo off
chcp 65001
cd /d %~dp0
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1
set PYTHONPATH=Python/Lib/site-packages;Python/Lib;Python
set PATH=Python/Lib/site-package;Python/Lib;Python/Scripts;Python;%PATH%
set PROMPT=(QPT_VENV) %PROMPT%
cls
echo QPT successful!
cmd /k
