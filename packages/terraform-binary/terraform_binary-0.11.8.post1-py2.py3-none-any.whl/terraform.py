"""Python wrapper for Hashicorp's Terraform pre-built binary."""

TERRAFORM_VERSION = "0.11.8"

__version__ = f"{TERRAFORM_VERSION}.post1"


import os
import stat
import sys
import urllib.request
import zipfile


def download(version=TERRAFORM_VERSION, platform="linux_amd64"):
    base_url = f"https://releases.hashicorp.com/terraform/{version}"
    file_name = f"terraform_{version}_{platform}.zip"
    download_url = f"{base_url}/{file_name}"

    download_directory = "downloads"
    extract_directory = "lib"
    target_file = f"{download_directory}/{file_name}"

    os.makedirs(download_directory, exist_ok=True)
    os.makedirs(extract_directory, exist_ok=True)

    urllib.request.urlretrieve(download_url, target_file)

    with zipfile.ZipFile(target_file) as terraform_zip_archive:
        terraform_zip_archive.extractall(extract_directory)

    executable_path = f"{extract_directory}/terraform"
    executable_stat = os.stat(executable_path)
    os.chmod(executable_path, executable_stat.st_mode | stat.S_IEXEC)


def main():
    args = [] if len(sys.argv) < 2 else sys.argv[1:]
    executable = os.path.join(
        os.path.dirname(__file__), 'lib/terraform',
    )
    os.execv(executable, ["terraform"] + args)
