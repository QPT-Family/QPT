chcp 65001
cd /d %~dp0
cd ..
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set QPT_ARGS=%1
set QPT_ARGS=%QPT_ARGS:QPT_ARGS_FLAG= %
"./Python/python.exe" #QPT_MAIN_FILE_FALG#%QPT_ARGS%
echo 当前程序已执行结束，任意键后将进行关闭本程序。
pause
