chcp 65001
cd /d %~dp0
echo on
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set PROMPT=(QPT_VENV) %PROMPT%

set QPT_PY_MAIN_FILE=NONE
set QPT_ARGS=%1
"./Python/python.exe" %QPT_PY_MAIN_FILE%%QPT_ARGS:QPT_ARGS_FLAG= %

cls
pause
