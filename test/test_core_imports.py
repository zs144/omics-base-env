import yaml
import importlib
import pytest

# Path to your environment.yml
ENV_YML = "environment.yml"

def load_packages(env_file=ENV_YML):
    """
    Load packages from environment.yml, including pip section.
    Returns a list of package names.
    """
    with open(env_file, "r") as f:
        env = yaml.safe_load(f)

    packages = []

    # Conda dependencies
    for dep in env.get("dependencies", []):
        if isinstance(dep, str):
            # Just take the package name before '=' if version is specified
            pkg = dep.split("=")[0].strip()
            packages.append(pkg)
        elif isinstance(dep, dict) and "pip" in dep:
            for pip_pkg in dep["pip"]:
                pkg = pip_pkg.split("=")[0].strip()
                packages.append(pkg)
    return packages

@pytest.mark.parametrize("package", load_packages())
def test_import(package):
    """
    Try importing each package.
    """
    try:
        importlib.import_module(package)
    except ModuleNotFoundError:
        pytest.fail(f"Package '{package}' cannot be imported")