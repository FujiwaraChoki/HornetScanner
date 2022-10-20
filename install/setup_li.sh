#!/bin/bash

# Install requirement from requirements.txt
sudo pip3 install -r requirements.txt

pyinstaller --onefile ../src/main.py

# Move binary to bin folder (needs sudo permission)
sudo mv dist/main /bin/hornet

# Remove build folder
rm -rf build

# Remove dist folder
rm -rf dist

# Remove main.spec file
rm main.spec

