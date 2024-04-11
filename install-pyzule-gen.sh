#!/bin/bash
PZ_DIR=${HOME}/.config/pyzule

if [ ! -d "${PZ_DIR}" ]; then
    echo "[*] ${PZ_DIR} does not exist. Creating..."
    mkdir -p "${PZ_DIR}"
fi

if [ ! -d "${PZ_DIR}/venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv "${PZ_DIR}/venv"
fi

source "${PZ_DIR}/venv/bin/activate"

echo "[*] Installing dependencies..."
pip install orjson Pillow &> /dev/null

echo "[*] Installing pyzule-gen..."
sudo curl -so /usr/local/bin/pyzule-gen https://raw.githubusercontent.com/asdfzxcvbn/pyzule-gen/main/pyzule-gen.py

if [ "$(uname)" == "Linux" ]; then
    sudo sed -i "1s|.*|#\!${PZ_DIR}/venv/bin/python|" /usr/local/bin/pyzule-gen
else
    sudo sed -e "1s|.*|#\!${PZ_DIR}/venv/bin/python|" -i "" /usr/local/bin/pyzule-gen
fi

echo "[*] Fixed interpreter path!"
sudo chmod +x /usr/local/bin/pyzule-gen

echo "[*] pyzule-gen is ready to use!"
echo "[*] Done!"
