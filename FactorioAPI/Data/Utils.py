import hashlib


def getFileHash(path: str) -> str:
    return hashlib.sha512(open(path, "rb").read()).hexdigest()


def getDataHash(data: bytes) -> str:
    return hashlib.sha512(data).hexdigest()
