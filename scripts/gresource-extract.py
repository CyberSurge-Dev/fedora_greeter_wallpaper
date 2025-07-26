#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from pathlib import Path

def get_resource_list(gresource_file):
    try:
        result = subprocess.run(
            ['gresource', 'list', gresource_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        resources = result.stdout.strip().splitlines()
        return resources
    except subprocess.CalledProcessError as e:
        print(f"Failed to list resources: {e.stderr}")
        sys.exit(1)

def extract_resource(gresource_file, resource_path, output_dir):
    try:
        result = subprocess.run(
            ['gresource', 'extract', gresource_file, resource_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        output_path = Path(output_dir) / resource_path.lstrip('/')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(result.stdout)
        print(f"Extracted: {resource_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract {resource_path}: {e.stderr}")

def main():
    parser = argparse.ArgumentParser(description='Extract all resources from a .gresource file.')
    parser.add_argument('file', help='Path to the .gresource file')
    parser.add_argument('-o', '--output', help='Output directory', default='extracted_gresource')

    args = parser.parse_args()
    gresource_file = args.file
    output_dir = args.output

    if not os.path.isfile(gresource_file):
        print(f"Error: File not found - {gresource_file}")
        sys.exit(1)

    resources = get_resource_list(gresource_file)
    if not resources:
        print("No resources found.")
        sys.exit(1)

    for resource_path in resources:
        extract_resource(gresource_file, resource_path, output_dir)

if __name__ == '__main__':
    main()

