# CuraPackageDeployer
Automatically build, deploy and distribute [Ultimaker Cura](https://github.com/Ultimaker/Cura) Toolbox packages.

## Introduction
Ultimaker has introduced a new set of tools to build and deploy [packages for Ultimaker Cura](https://github.com/Ultimaker/Cura/wiki/Creating-Packages).
These packages can extend the functionality and contents of Cura and users can install them via the Cura Toolbox.

One of the new tools available is a web API for managing and distributing these packages.
Besides a [user interface](https://contribute.ultimaker.com) consuming this API,
developers can also [use the API](https://api.ultimaker.com/docs/packages/) directly.

This library uses that API to automate the building and deployment of packages.
It's written in Python, so you can use it in your CI/CD system of your choice.

## Installation
Install the library in your plugin project using pip:

```bash
pip3 install CuraPackageDeployer
```

## Usage
The best way to use this library is to make a Python script and use the `CuraPackageDeployer` class from there:

```python
import logging
import sys
import time

from CuraPackageDeployer.Config import Config
from CuraPackageDeployer.CuraPackageDeployer import CuraPackageDeployer


class ExampleConfig(Config):
    """
    Example config file that extends the root config.
    """
    package_id = "CuraDrive"
    package_sources_dir = "/Users/chris/Code/Ultimaker/cura/CuraDrivePlugin/CuraDrive"
    tags = ["backups", "cloud", "restore", "configuration", "settings", "sync"]
    website = "https://ultimaker.com"
    release_notes = "Switched to the new Ultimaker Account functionality baked into Cura."
    access_token = "THIS_IS_A_SECRET!"


def main() -> int:
    config = ExampleConfig()
    deployer = CuraPackageDeployer(config)
    deployer.loadPluginSources()
    deployer.buildPlugin()
    deployer.deploy()
    time.sleep(3)  # Give the API some time to build the package.
    deployer.requestReview()
    return 0


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    exit_code = main()
    sys.exit(exit_code)
```

Then execute this script in your CI/CD system of choice.

### Docker
We recommend running the script in a Docker container to always have a suitable runtime environment.
An example Dockerfile could be:

```Dockerfile
FROM python:3.6-alpine AS base
WORKDIR /usr/src/app

RUN pip3 install CuraPackageDeployer

CMD ["python3", "example.py"]
ADD . .
```

## Contribute
To help improve this project, feel free to make issues or pull requests via GitHub.
