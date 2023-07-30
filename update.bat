@echo off

REM 切换到当前目录
cd /d %~dp0

REM 调用 Python 脚本 getToc.py和setPart.py，并将输出结果输出到控制台
echo -----getToc.py-----
python getToc.py --print
echo -----setPart.py-----
python setPart.py

REM 等待用户按任意键退出
pause