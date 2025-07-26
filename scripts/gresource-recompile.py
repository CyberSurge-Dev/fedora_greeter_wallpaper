#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

def infer_prefix_from_paths(resource_paths):
    """Infer longest common prefix from file paths, turned into a virtual resource prefix."""
    if not resource_paths:
        return "/"
    split_paths = [p.parts for p in resource_paths]
    common = []
    for parts in zip(*split_paths):
        if all(part == parts[0] for part in parts):
            common.append(parts[0])
        else:
            break
    return "/" + "/".join(common)

def generate_resources_xml(resource_dir, xml_path):
    # Collect all resource files
    resource_files = [p for p in resource_dir.rglob("*") if p.is_file() and p.name != "resources.xml"]
    if not resource_files:
        print("[!] No files found in input directory.")
        sys.exit(1)

    rel_paths = [f.relative_to(resource_dir) for f in resource_files]
    prefix = ""

    gresources = ET.Element("gresources")
    gresource = ET.SubElement(gresources, "gresource", attrib={"prefix": prefix})

    for rel_path in rel_paths:
        ET.SubElement(gresource, "file").text = str(rel_path)

    tree = ET.ElementTree(gresources)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"[+] Generated XML: {xml_path}")
    print(f"[+] Using prefix: {prefix}")

def recompile_gresource(xml_path, sourcedir, output_file):
    try:
        subprocess.run([
            "glib-compile-resources",
            str(xml_path),
            "--target=" + str(output_file),
            "--sourcedir=" + str(sourcedir)
        ], check=True)
        print(f"[✓] Successfully created: {output_file}")
    except subprocess.CalledProcessError as e:
        print("[!] Error during compilation:\n", e)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Recompile extracted gresource into a .gresource file.")
    parser.add_argument("input_dir", help="Directory containing extracted resources (with full paths like org/gnome/...)")
    parser.add_argument("output_file", help="Path to output .gresource file")

    args = parser.parse_args()
    input_dir = Path(args.input_dir).resolve()
    output_file = Path(args.output_file).resolve()
    xml_path = input_dir / "resources.xml"

    if not input_dir.exists():
        print(f"[!] Error: Input directory {input_dir} does not exist.")
        sys.exit(1)

    generate_resources_xml(input_dir, xml_path)
    recompile_gresource(xml_path, input_dir, output_file)

if __name__ == "__main__":
    main()

