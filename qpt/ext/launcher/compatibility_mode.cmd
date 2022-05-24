echo on
cd /d %~dp0
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set PYTHONPATH=Python/Lib/site-packages;Python/Lib;Python
set PATH=Python/Lib/site-package;Python/Lib;Python/Scripts;Python;%PATH%
set QPT_RUN_CODE_S1="import sys;sys.path.append('./Python');sys.path.append('./Python/Lib');sys.path.append('./Python/Lib/site-packages');sys.path.append('./Python/Scripts');from qpt.run import module;module.run('"
set QPT_RUN_CODE_M1=%1
set QPT_RUN_CODE_E1="')"
set QPT_RUN_CODE_1=%QPT_RUN_CODE_S1%%QPT_RUN_CODE_M1%%QPT_RUN_CODE_E1%
cls
"./Python/python.exe" -c %QPT_RUN_CODE_1%
pause
