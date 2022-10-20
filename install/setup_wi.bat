@echo off

pip3 install -r requirements.txt

pyinstaller --onefile ../src/main.py