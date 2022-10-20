#!/bin/bash

# Install requirement from requirements.txt
sudo pip3 install -r requirements.txt

pyinstaller --onefile ../src/main.py