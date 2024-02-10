#!/bin/bash
PZ_DIR=${HOME}/.config/pyzule

if [ ! -d "${PZ_DIR}" ] || [ ! -x "$(command -v pyzule)" ]; then
    echo "[!] pyzule is not installed"
    exit 1
fi

echo "[*] installing pyzule-gen.."
sudo curl -so /usr/local/bin/pyzule-gen https://raw.githubusercontent.com/asdfzxcvbn/pyzule-gen/main/pyzule-gen.py
if [ "$(uname)" == "Linux" ]; then
    sudo sed -i "1s|.*|#\!${PZ_DIR}/venv/bin/python|" /usr/local/bin/pyzule-gen
else
    sudo sed -e "1s|.*|#\!${PZ_DIR}/venv/bin/python|" -i "" /usr/local/bin/pyzule-gen  # bsd sed is broken asf
fi
echo "[*] fixed interpreter path!"
sudo chmod +x /usr/local/bin/pyzule-gen
echo "[*] done!"
