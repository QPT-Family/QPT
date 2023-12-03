echo on
chcp 65001
cd /d %~dp0
cd ../resources
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8

set QPT_PY_MAIN_FILE=NONE
set QPT_ARGS=%1
"../Python/python.exe" %QPT_PY_MAIN_FILE%%QPT_ARGS:QPT_ARGS_FLAG= %

echo 当前程序已执行结束，任意键后将进行关闭本程序。
pause