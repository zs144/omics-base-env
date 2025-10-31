"""
check_packages.py
Check which packages from a requirements.txt or environment.yml are missing.
"""

import importlib
import sys
import yaml
from pathlib import Path
from tqdm import tqdm

def parse_requirements(req_file):
    packages = []
    with open(req_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # take only package name (before == or >=)
                pkg = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                packages.append(pkg)
    return packages


def parse_environment(yml_file):
    with open(yml_file) as f:
        env = yaml.safe_load(f)
    packages = []
    for dep in env.get("dependencies", []):
        if isinstance(dep, str):
            pkg = dep.split("=")[0].strip()
            packages.append(pkg)
        elif isinstance(dep, dict) and "pip" in dep:
            for pip_pkg in dep["pip"]:
                pkg = pip_pkg.split("==")[0].strip()
                packages.append(pkg)
    return packages


def check_import(packages):
    missing = []
    for pkg in tqdm(packages, desc="Checking packages", ncols=100):
        try:
            importlib.import_module(pkg)
        except Exception:
            missing.append(pkg)
    return missing


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_packages.py <requirements.txt|environment.yml> <output_fp>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    output_fp = Path(sys.argv[2])
    if not file_path.exists():
        print(f"{file_path} not found")
        sys.exit(1)

    if file_path.suffix == ".txt":
        pkgs = parse_requirements(file_path)
    elif file_path.suffix in [".yml", ".yaml"]:
        pkgs = parse_environment(file_path)
    else:
        print("Unsupported file type")
        sys.exit(1)

    missing = check_import(pkgs)
    if missing:
        print("Missing packages:")
        with open(output_fp, "w") as f:
            for m in missing:
                print(f" - {m}")
                f.write(m + "\n")
    else:
        print("All packages import successfully!")