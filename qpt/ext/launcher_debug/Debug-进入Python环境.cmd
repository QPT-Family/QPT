echo on
chcp 65001
cd /d %~dp0
set QPT_MODE=Debug
set PYTHONIOENCODING=utf-8
set PYTHONPATH=Python/Lib/site-packages;Python/Lib;Python
cls
"./Python/python.exe"
pause
