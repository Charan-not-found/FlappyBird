@echo off
py -3.11 -m venv .venv
call .\.venv\Scripts\activate
pip install -r requirements
deactivate
call RUN.bat