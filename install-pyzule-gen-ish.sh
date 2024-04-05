#!/bin/ash

echo "[*] installing pyzule-gen.."
curl -so /usr/local/bin/pyzule-gen https://raw.githubusercontent.com/asdfzxcvbn/pyzule-gen/main/pyzule-gen-ish.py
chmod +x /usr/local/bin/pyzule-gen
echo "[*] done!"
