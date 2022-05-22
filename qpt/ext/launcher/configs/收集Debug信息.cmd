echo off
cd /d %~dp0
cd ..
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set PYTHONPATH=./Python/resources;./Python/Lib/site-packages;./Python
set PATH=%PATH%;./Python/resources;./Python/Lib/site-packages;./Python;./Python/Lib;./Python/Scripts
set PROMPT=(QPT_VENV) %PROMPT%
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)
cls
set /P VAR=该脚本会模拟您在点击启动程序时的所有操作，并记录下尽可能多的输出信息。因此在收集Debug信息前需要保证该文件下任何程序均出于全新未运行过的状态，若您在使用本Debug信息收集脚本前执行了本文件夹下的某些程序，请重新使用QPT打包后再启动这个收集脚本！需要注意的是，为了更好Debug该脚本会收集基本的系统和硬件信息，当然这些信息只会存储在configs目录下，其用途将由您决定。（按任意键同意收集）
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)

set QPT_CONFIGS=./configs/
echo "Step1: Collecting Python package installation list"
"./Python/python.exe" "-m" "pip" "list" > %QPT_CONFIGS%pip_list.txt

echo "Step2: Collecting system info"
Systeminfo > %QPT_CONFIGS%sys_info.txt

echo "Step3: Collecting CPU and GPU info"
wmic cpu > %QPT_CONFIGS%cpu_info.txt
(for /f "tokens=1,2 delims==" %%a in ('wmic path Win32_VideoController get AdapterRAM^,Name /value^|findstr "AdapterRAM Name"') do echo %%a:%%b) > %QPT_CONFIGS%gpu_info.txt

echo "Step4: Collecting env vars"
set > %QPT_CONFIGS%env_vars_info.txt

echo "Step5: Try running the QPT-Program"
set QPT_COLOR=False
set QPT_MODE=Debug
cls
"./Python/python.exe" -c "import sys;sys.path.append('./Python');sys.path.append('./Python/Lib/site-packages');sys.path.append('./Python/Scripts');import qpt.run as run" > %QPT_CONFIGS%Run_info.txt

echo "Step6: Collecting Python package installation list"
"./Python/python.exe" "-m" "pip" "list" > %QPT_CONFIGS%pip_list_final.txt

echo "All operations completed"
pause
