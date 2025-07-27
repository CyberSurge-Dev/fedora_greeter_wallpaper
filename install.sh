#!/bin/bash

# Check if the script is being run as root (EUID = 0)
if (( $EUID != 0 )); then
    echo "[!] This script must be run as root."
    exit 1
fi


echo "[+] Greeter Wallpaper Installer..."

update_css () {
	if grep -q "Greeter Wallpaper" "$1"; then
		echo "[!] css already edited: $1"
	else
		echo "[+] added css to $1"
		cat <<EOF >> "$1"
/* 'Greeter Wallpaper' CSS additions */

.login-dialog { background: transparent; }
#lockDialogGroup {
  background-image: url('resource:///org/gnome/shell/theme/background');
  background-position: center;
  background-size: cover;
}
EOF
	fi
}

echo "[+] Downloading dependencies"
# Dependencies
dnf install glib2-devel

echo "[+] Creating directories for scripts"
mkdir /usr/local/bin/greeter_wallpaper
mkdir /usr/local/bin/greeter_wallpaper/backup
mkdir /usr/local/bin/greeter_wallpaper/wallpapers
mkdir /usr/local/bin/greeter_wallpaper/workdir
mkdir ./output

echo "[+] Copying scripts"
cp -r ./scripts/* /usr/local/bin/greeter_wallpaper/

echo "[+] Copying wallpapers"

rm -r /usr/local/bin/greeter_wallpaper/wallpapers/*
cp -r ./wallpapers/* /usr/local/bin/greeter_wallpaper/wallpapers/

# >> The risky shit <<
echo "[+] Extracting gnome-shell-theme.gresource"
chmod +x "./scripts/gresource-extract.py"
python ./scripts/gresource-extract.py "/usr/share/gnome-shell/gnome-shell-theme.gresource" -o "./output"

if [ -f "./output/org/gnome/shell/theme/gdm.css" ]; then
	update_css "./output/org/gnome/shell/theme/gdm.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell-dark.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell-dark.css"
fi
if [ -f "./output/org/gnome/shell/theme/gdm3.css" ]; then
	update_css "./output/org/gnome/shell/theme/gdm3.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell-high-contrast.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell-high-contrast.css"
fi
if [ -f "./output/org/gnome/shell/theme/gnome-shell-light.css" ]; then
	update_css "./output/org/gnome/shell/theme/gnome-shell-light.css"
fi

# Re compile .gresource


chmod +x "./scripts/gresource-recompile.py"
python ./scripts/gresource-recompile.py ./output ./gnome-shell-theme.gresource

cp ./gnome-shell-theme.gresource /usr/share/gnome-shell/gnome-shell-theme.gresource

# set up the service
echo "[+] Copying service file to /etc/systemd/system/"
cp ./resources/greeter_wallpaper.service /etc/systemd/system/
echo "[+] Enabling the greeter_wallpaper.service"
systemctl daemon-reload
systemctl enable greeter_wallpaper.service

# Clean up
echo "Cleaning up..."
chmod +x /usr/local/bin/greeter_wallpaper/*
rm -r ./output
rm ./gnome-shell-theme.gresource
echo "[✓] Greeter_wallpaper is installed."
echo "[✓] It is recommended to restart now."
