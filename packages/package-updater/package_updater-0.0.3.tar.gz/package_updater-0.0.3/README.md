
# package_updater

---

This module allow any package/module/script to be updated with the latest release from github 

## Install

```shell
pip3 install package-updater
```

## Usage

```python
import sys
import package_updater

updater = package_updater.Update(
    package_name="Name of the package",
    current_version="1.1.2",
    repo="https://api.github.com/repos/superlevure/SRU_com/releases/latest"
    )

if sys.argv[1] == "--update":
    updater.update()
```

The module will :

- Check if a new version is avalaible 
- If so, backup the current version to a tar file 
- Download the new version 
- Extract it 
- Install it 