import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def install_package(requirement):
    """Install or reinstall the package with the specified version if necessary."""
    try:
        # Check if the requirement is met
        pkg_resources.require(requirement)
        print(f"{requirement} is already installed and meets the requirement.")
    except (DistributionNotFound, VersionConflict):
        # Requirement is not met, install or reinstall the package
        print(f"Installing or updating {requirement}.")
        subprocess.run(["pip", "install", "--force-reinstall", requirement], check=True)


if __name__ == "__main__":
    with open("/tmp/requirements.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore empty lines and comments
                install_package(line)
