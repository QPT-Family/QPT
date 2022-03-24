chcp 65001
cd /d %~dp0
cd ..
set QPT_COLOR=False
set QPT_MODE=Run
cls
set PYTHONPATH=Python/Lib/site-packages;Python/Lib;Python
set PATH=Python/Lib/site-package;Python/Lib;Python/Scripts;Python;%PATH%
echo off
"./Python/python.exe" -c "import sys;sys.path.append('./Python');sys.path.append('./Python/Lib');sys.path.append('./Python/Lib/site-packages');sys.path.append('./Python/Scripts');import qpt.run as run"
