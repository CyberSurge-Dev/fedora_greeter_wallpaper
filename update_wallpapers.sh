#!/bin/bash

# Check if the script is being run as root (EUID = 0)
if (( $EUID != 0 )); then
    echo "[!] This script must be run as root."
    exit 1
fi

echo "[+] Copying wallpapers"

echo "[+] Removing existing wallpapers..."
rm -r -fr /usr/local/bin/greeter_wallpaper/wallpapers/*
echo "[+] Copying new wallpapers..."
cp -r ./wallpapers/* /usr/local/bin/greeter_wallpaper/wallpapers/
echo "[✓] Complete"
