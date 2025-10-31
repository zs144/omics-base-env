"""
sort_packages.py
Reorder packages in a requirements.txt or environment.yml alphabetically.
"""

import sys
import yaml
from pathlib import Path

def parse_requirements(req_file):
    packages = []
    with open(req_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                packages.append(line)
    return packages

def write_requirements(req_file, packages, output_file=None):
    if output_file is None:
        output_file = req_file
    with open(output_file, "w") as f:
        for pkg in packages:
            f.write(pkg + "\n")

def parse_environment(yml_file):
    with open(yml_file) as f:
        env = yaml.safe_load(f)

    base_packages = []
    pip_packages = []

    for dep in env.get("dependencies", []):
        if isinstance(dep, str):
            base_packages.append(dep)
        elif isinstance(dep, dict) and "pip" in dep:
            pip_packages.extend(dep["pip"])

    return env, base_packages, pip_packages

def write_environment(yml_file, env, base_packages, pip_packages, output_file=None):
    env["dependencies"] = base_packages
    if pip_packages:
        env["dependencies"].append({"pip": pip_packages})

    if output_file is None:
        output_file = yml_file

    with open(output_file, "w") as f:
        yaml.dump(env, f, sort_keys=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sort_packages.py <requirements.txt|environment.yml> [output_file]")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not file_path.exists():
        print(f"{file_path} not found")
        sys.exit(1)

    if file_path.suffix == ".txt":
        pkgs = parse_requirements(file_path)
        python_pkgs = [p for p in packages if p.lower().startswith("python=")]
        other_pkgs = [p for p in packages if not p.lower().startswith("python=")]
        pkgs_sorted = python_pkgs + sorted(other_pkgs, key=str.lower)
        write_requirements(file_path, pkgs_sorted, output_file)
        print(f"Sorted requirements written to {output_file or file_path}")
    elif file_path.suffix in [".yml", ".yaml"]:
        env, base_pkgs, pip_pkgs = parse_environment(file_path)
        print(base_pkgs)
        python_pkgs = [p for p in base_pkgs if p.lower().startswith("python=")]
        other_pkgs = [p for p in base_pkgs if not p.lower().startswith("python=")]
        base_pkgs_sorted = python_pkgs + sorted(other_pkgs, key=str.lower)
        pip_pkgs_sorted = sorted(pip_pkgs, key=str.lower)
        write_environment(file_path, env, base_pkgs_sorted, pip_pkgs_sorted, output_file)
        print(f"Sorted environment written to {output_file or file_path}")
    else:
        print("Unsupported file type")
        sys.exit(1)