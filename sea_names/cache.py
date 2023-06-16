"""Module to download available sea name polygons to local system."""
import hashlib
import shutil
import sys
import tarfile

from argparse import ArgumentParser
from pathlib import Path

import appdirs
import requests

from sea_names.log import logger, setup_logging


URL = "https://files.axds.co/sea_names.tar.gz"
FILE_HASH = "723b4d16b02cb5c555ffb1f9d3324edecd2b9dadd55af17e1549232006054cd4"
CACHE_PATH = Path(appdirs.user_cache_dir("sea-names", "co.axiomdatascience"))
CACHE_FILE = CACHE_PATH / "sea_names.tar.gz"
CACHE_BOUNDS_FILE = CACHE_PATH / "sea_names/sea_names.box"


def extract_region_bounds():
    """Extracts the tarball of sea-name polygon info."""
    with tarfile.open(CACHE_FILE, mode="r:gz") as tf:
        tf.extract(member="sea_names/sea_names.box", path=CACHE_PATH)


def download_sea_names():
    """Download the latest sea_names cache."""
    CACHE_PATH.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading cache from {URL}")
    with requests.get(URL, stream=True) as r:
        with open(CACHE_FILE, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    shasum = sha256sum(CACHE_FILE)
    logger.info("Computing hash")
    if shasum != FILE_HASH:
        raise ValueError(
            "File hash is invalid. The file may have been updated, please check for the latest "
            "version of sea-names"
        )
    extract_region_bounds()


def sha256sum(filename) -> str:
    """Return the sha256 hash of the file."""
    hash_ctx = hashlib.sha256()
    buf = bytearray(128 * 1024)
    mv = memoryview(buf)
    with open(filename, "rb", buffering=0) as f:
        while n := f.readinto(mv):
            hash_ctx.update(mv[:n])

    return hash_ctx.hexdigest()


def main():
    """Force rebuilding of sea-names cache."""
    parser = ArgumentParser(description=main.__doc__)
    parser.parse_args()

    setup_logging()
    download_sea_names()
    return 0


if __name__ == "__main__":
    sys.exit(main())
