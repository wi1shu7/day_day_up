@echo off

REM 切换到当前目录
cd /d %~dp0

REM 调用 Python 脚本 getToc.py，并将输出结果输出到控制台
python getToc.py --print

REM 等待用户按任意键退出
pause