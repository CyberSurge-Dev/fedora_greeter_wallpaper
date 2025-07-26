#!/usr/bin/env python3

import os
import random
import subprocess
import sys

def choose_random_image (directory, extensions=None):
    if extensions is None:
        extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff')

    # List all files in the directory that match the allowed extensions
    image_files = [file for file in os.listdir(directory)
                   if file.lower().endswith(extensions)
                   and os.path.isfile(os.path.join(directory, file))]

    if not image_files:
        raise FileNotFoundError("No image files found in the directory.")

    # Randomly select an image file
    selected_file = random.choice(image_files)
    return os.path.join(directory, selected_file)

# Example usage
if __name__ == "__main__":
    GRESOURCE_P = "/usr/share/gnome-shell/"
    GRESOURCE_PATH = "/usr/share/gnome-shell/gnome-shell-theme.gresource"
    WORKDIR = "./workdir"
    OUTPUT = "./gnome-shell-theme.gresource"
    BKGS = "./wallpapers"
    BACKUP = "./backup/"
    BACKGROUND_PATH = WORKDIR + "/output/org/gnome/shell/theme/background"
    
    try:
        image_path = choose_random_image(BKGS)
        
        # Create Backup
        subprocess.run([
            "cp", "-r",
            GRESOURCE_P,
            BACKUP
        ], check=True)
        
        
        # Extract .gresource File to working directory output
        subprocess.run(["./gresource-extract.py", GRESOURCE_PATH, "-o", WORKDIR+"/output"], check=True)
        print("[✓] gresource file: " + GRESOURCE_PATH + "Extracted Successfully to " + WORKDIR + "/output")
        
        # Copy the background into the directory
        subprocess.run([
            "cp",
            image_path, BACKGROUND_PATH
        ], check=True)
        print("[✓] Background " + image_path + " copied to " + BACKGROUND_PATH)
        
        # Re-compile gresource file  
        subprocess.run([
            "./gresource-recompile.py",
            WORKDIR + "/output",
            OUTPUT
        ], check=True)
        print("[✓] Recompile Successful")
        
        # Replace original gresource file
        subprocess.run([
            "cp",
            OUTPUT,
            GRESOURCE_PATH
        ], check=True)
        
        print("[✓] .gresource replaced")
        
    except Exception as e:
        print("Error:", e)
