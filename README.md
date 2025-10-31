# 🧬 omix-base-env

![Python](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![GitHub stars](https://img.shields.io/github/stars/zs144/omix-base-env?style=social)

A lightweight, compatible Python base environment for single-cell and spatial omics analysis.

## 🌎 Overview

`omix-base-env` provides a unified, minimal environment that supports most modern omics tools (e.g., Scanpy, Squidpy, SpatialData) while minimizing disk usage and dependency conflicts. It’s ideal for researchers who frequently test or develop single-cell and spatial transcriptomics software.

## 🎯 Key Goals

* Reduce redundant conda environments.
* Ensure broad compatibility across popular omics packages.
* Simplify migration and reproducibility.
* Keep environment lightweight and stable.


## 📂 Folder Structure
```
omix-base/
│
├── environment.yml               # core base environment
├── optional-envs/                # tool-specific overlays
│   └── example.yml
├── scripts/
│   ├── sort_packages.py
│   └── check_packages.py
├── tests/
│   └── test_core_imports.py
├── README.md
├── TODO.md
├── CONTRIBUTING.md
└── LICENSE
```

## 📦 Installation

### Step 1: Clone the repo
```bash
git clone https://github.com/zs144/omix-base-env.git
cd omix-base-env
```

### Step 2: Create the environment
```bash
conda env create -f environment.yml
```

### Step 3: Activate it
```bash
conda activate omix-base-env
```

To use Mamba instead of Conda:
```bash
mamba env create -f environment.yml
conda activate omix-base-env
```

## ⚙️ Usage
### 1. Install Extra Packages

Some tools may require additional dependencies. You can find curated add-on environments in the `optional-envs/` folder.

#### Solution 1. Install extra packages from the overlay YAML
```bash
conda env update -f optional-envs/<example>.yml
```

### Solution 2. Install extra packages from the overlay requirements.txt
```bash
pip install -r requirements.txt
```

#### Solution 3. Install a single pip-only package in the base environment
```bash
conda activate omix-base
pip install some-pip-only-package
```

### 2. Compare with other environment
If you have another environment YAML file or requirement file, you can find which are missing in the current `omix-base-env` by running:
```bash
python check_packages.py <requirements.txt|environment.yml> <output_fp>
```
This will print out the missing packages and save them in a txt file.

## 🧪 Testing

Run the quick import tests to verify that core libraries are installed correctly:
```bash
pytest tests/test_core_imports.py
```

## 🤝 Contributing

We welcome community contributions! We will soon publish a short guide for contributing. Stay tuned!


## ⚖️ License

MIT License – see [LICENSE](./LICENSE) for details.


## 🔖 Citation

If this environment helps your research, please cite the repo:

Z. Sheng (2025). omix-base-env: A lightweight base environment for single-cell and spatial omics. github.com/zs144/omix-base-env