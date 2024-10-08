import requests

VERSION = "1.1.2"

APPLINK = "https://github.com/catlord-dev/factorioapi"

APPNAME = "FactorioAPI"

def getDefaultUserAgent(appName: str = APPNAME, appVersion: str = VERSION) -> str:
    return f"{appName}/{appVersion} (python-requests/{requests.__version__})"


def getDefaultHeaders(
    appLink: str = APPLINK, appName: str = APPNAME, appVersion: str = VERSION
) -> dict:
    return {
        "User-Agent": getDefaultUserAgent(appName, appVersion),
        "Accept-Encoding": requests.utils.DEFAULT_ACCEPT_ENCODING,
        "Accept": "application/json",
        "Connection": appLink,
    }


import hashlib


def getFileHash(path: str) -> str:
    return hashlib.sha512(open(path, "rb").read()).hexdigest()


def getDataHash(data: bytes) -> str:
    return hashlib.sha512(data).hexdigest()
