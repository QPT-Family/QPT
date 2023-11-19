echo on
chcp 65001
cd /d %~dp0
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONIOENCODING=utf-8
cls
"./Python/python.exe" "-m" "pip" "list"
pause
