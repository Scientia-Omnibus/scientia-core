import socket
from importlib.metadata import version
from itertools import zip_longest

import httpx


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except socket.error:
        return False


def get_local_version():
    return version("scientia-core")


def get_github_version(
    url: str = "https://api.github.com/repos/Scientia-Omnibus/scientia-core/releases/latest",
):
    headers = {"User-Agent": "scientia-core/1.0"}
    response = httpx.get(url, timeout=10, headers=headers)
    response.raise_for_status()

    data = response.json()
    version = data["tag_name"]
    return version


def compare_versions(local: str, github: str):
    """
    0 - ok
    1 - need update
    -1 - newer github version
    """
    local = local.lstrip("v")
    github = github.lstrip("v")
    v1, v2 = local.split("."), github.split(".")

    for f, s in zip_longest(v1, v2, fillvalue="0"):
        if int(f) < int(s):
            return -1
        if int(f) < int(s):
            return 1
    return 0
