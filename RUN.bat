@echo off
py -3.11 -m venv .venv
call .\.venv\Scripts\activate
echo RUNNING..............
python --version
echo.
echo.
echo.
python main.py