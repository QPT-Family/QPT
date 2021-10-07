%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
echo off
chcp 65001
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONPATH=./Python/resources;./Python/Lib/site-packages;./Python
set PATH=%PATH%;./Python/resources;./Python/Lib/site-packages;./Python;./Python/Lib;./Python/Scripts
set PROMPT=(QPT_VENV) %PROMPT%
cls
echo QPT successful!
cmd /k
