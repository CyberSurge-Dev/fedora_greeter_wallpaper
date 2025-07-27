# Gnome GDM Greeter Background Switcher
A simple script and service to automatically change the Gnome GDM login screen background on each power cycle (Similar to how it is done with windows). This script has been tested to work on the latest version of fedora workstation (as of writing, version 42), it has not been tested on any other distrubutions, so use at your own risk.

<img width="2880" height="1920" alt="Screenshot from 2025-07-26 15-52-27" src="https://github.com/user-attachments/assets/ce4d5303-c671-4123-a41b-bec89d0f48a5" />

## Setup 
Download/clone the repository, and open the directory in your terminal.
Run the following commands:
```
chmod +x ./install.sh
sudo ./install.sh
```
After this, ``restart your computer`` and if everything worked correctly, you should see a randomly selected wallpaper from the wallpaperfolder as your background.

## Change wallpapers
Simply put your new wallpapers in the wallpaper directory and run the following commands in terminal (ensure you are in the directory with the update_wallpapers.sh script).
```
chmod +x ./update_wallpapers.sh
sudo ./update_wallpapers.sh
```
## Other stuff
if you find that your wallpaper no longer shows up after a system update, simply run the install script again and the issue should go away. There is no issue with having to run the script mutliple times, unless you run into package errors or python errors.
