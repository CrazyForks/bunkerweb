#!/usr/bin/env python3

from io import BytesIO
from os import getenv, sep
from os.path import join
from pathlib import Path
from re import MULTILINE, search
from shutil import rmtree
from sys import exit as sys_exit, path as sys_path
from tarfile import open as tar_open
from threading import Lock
from traceback import format_exc

for deps_path in [join(sep, "usr", "share", "bunkerweb", *paths) for paths in (("deps", "python"), ("utils",), ("db",))]:
    if deps_path not in sys_path:
        sys_path.append(deps_path)

from requests import RequestException, get

from logger import setup_logger  # type: ignore
from jobs import Job  # type: ignore

LOGGER = setup_logger("MODSECURITY.coreruleset-nightly", getenv("LOG_LEVEL", "INFO"))
status = 0
LOCK = Lock()

CRS_PATH = Path(sep, "var", "cache", "bunkerweb", "modsecurity", "crs")

try:
    # * Check if we're using the nightly version of the Core Rule Set (CRS)
    use_nightly_crs = False

    if getenv("MODSECURITY_CRS_VERSION", "3") == "nightly":
        use_nightly_crs = True
    elif getenv("MULTISITE", "no") == "yes":
        for first_server in getenv("SERVER_NAME", "").split(" "):
            if first_server and getenv(f"{first_server}_MODSECURITY_CRS_VERSION", getenv("MODSECURITY_CRS_VERSION", "3")) == "nightly":
                use_nightly_crs = True
                break

    if not use_nightly_crs:
        LOGGER.info("Core Rule Set (CRS) nightly is not being used, skipping download...")
        sys_exit(0)

    JOB = Job(LOGGER)

    LOGGER.info("Checking if Core Rule Set (CRS) nightly needs to be downloaded...")

    commit_hash = JOB.get_cache("commit_hash")

    resp = get("https://github.com/coreruleset/coreruleset/releases/tag/nightly", timeout=5)
    resp.raise_for_status()

    content = resp.text

    page_commit_hash = search(r"/coreruleset/coreruleset/commit/(?P<hash>[0-9a-f]{40})", content, MULTILINE)

    if page_commit_hash is None:
        LOGGER.error("Failed to find commit hash on Core Rule Set (CRS) nightly page.")
        sys_exit(2)

    page_commit_hash = page_commit_hash.group("hash")

    LOGGER.debug(f"Page commit hash: {page_commit_hash}")

    if commit_hash:
        LOGGER.debug(f"Current commit hash: {commit_hash.decode()}")

        if commit_hash.decode() == page_commit_hash:
            LOGGER.info("Core Rule Set (CRS) nightly is up to date.")
            sys_exit(0)

        LOGGER.info("Core Rule Set (CRS) nightly is outdated.")

    cached, err = JOB.cache_file("commit_hash", page_commit_hash.encode())
    if not cached:
        LOGGER.error(f"Failed to cache the Core Rule Set (CRS) nightly commit hash: {err}")
        status = 2

    LOGGER.info("Downloading Core Rule Set (CRS) nightly tarball...")

    file_content = BytesIO()
    try:
        with get("https://github.com/coreruleset/coreruleset/archive/refs/tags/nightly.tar.gz", stream=True, timeout=5) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=4 * 1024):
                if chunk:
                    file_content.write(chunk)
    except RequestException:
        LOGGER.exception("Failed to download Core Rule Set (CRS) nightly tarball.")
        sys_exit(2)

    file_content.seek(0)

    rmtree(CRS_PATH, ignore_errors=True)
    CRS_PATH.mkdir(parents=True, exist_ok=True)

    LOGGER.info("Extracting Core Rule Set (CRS) nightly tarball...")

    with tar_open(fileobj=file_content, mode="r:gz") as tar_file:
        try:
            tar_file.extractall(CRS_PATH, filter="data")
        except TypeError:
            tar_file.extractall(CRS_PATH)

    # * Rename the extracted folder to "crs-nightly"
    extracted_folder = next(CRS_PATH.iterdir())
    extracted_folder.rename(CRS_PATH.joinpath("crs-nightly"))

    # * Move and rename the example configuration file to "crs-setup-nightly.conf"
    example_conf = CRS_PATH.joinpath("crs-nightly", "crs-setup.conf.example")
    example_conf.rename(CRS_PATH.joinpath("crs-setup-nightly.conf"))

    cached, err = JOB.cache_dir(CRS_PATH)
    if not cached:
        LOGGER.error(f"Error while saving Core Rule Set (CRS) nightly data to db cache: {err}")
    else:
        LOGGER.info("Successfully saved Core Rule Set (CRS) nightly data to db cache.")

    status = 1
except SystemExit as e:
    status = e.code
except:
    status = 2
    LOGGER.error(f"Exception while running coreruleset-nightly.py :\n{format_exc()}")

sys_exit(status)
