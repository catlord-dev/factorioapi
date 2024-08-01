import io
import json
from typing import Any, Callable

from FactorioAPI.Data.IO.read import (
    hexed,
    readArray,
    readBool,
    readDouble,
    readFloat,
    readInt,
    readShort,
    readString,
    readVersionString,
)


def readArrayWithContext(
    f: io.BufferedReader | io.BytesIO,
    objectDecoder: Callable[[io.BufferedReader | io.BytesIO], Any],
    **kwargs,
) -> list:
    """Reads variable amount of bytes and interprets them as an array.
    For arrays whose length is stored as a short

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
        objectDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the object.

    Returns:
        list: The bytes read as an array.
    """
    arrayLength = readShort(f)
    array = []
    for i in range(arrayLength):
        array.append(objectDecoder(f, **kwargs))
    return array


def readShortArray(
    f: io.BufferedReader | io.BytesIO,
    objectDecoder: Callable[[io.BufferedReader | io.BytesIO], Any],
    **kwargs,
) -> list:
    """Reads variable amount of bytes and interprets them as an array.
    For arrays whose length is stored as a short

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
        objectDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the object.

    Returns:
        list: The bytes read as an array.
    """
    arrayLength = readShort(f)
    array = []
    for i in range(arrayLength):
        array.append(objectDecoder(f, **kwargs))
    return array


def readHeader(f: io.BufferedReader | io.BytesIO) -> dict:
    achType = readString(f, spaceOptimized=True)
    achsOfType = readShortArray(f, readHeaderSubojbect)
    return {"type": achType, "achs": achsOfType}


def readHeaderSubojbect(f: io.BufferedReader | io.BytesIO) -> dict:
    achName = readString(f, spaceOptimized=True)
    achIndex = readShort(f)
    return {"name": achName, "index": achIndex}


def readContent(
    f: io.BufferedReader | io.BytesIO, indexLink: dict
) -> bytes | int | float | list:
    index = readShort(f)
    # print(f.tell(), index)
    data = None
    match indexLink[str(index)]:
        case "build-entity-achievement":
            data = hexed(f.read(4))
        case "combat-robot-count":
            data = readInt(f)
        case "construct-with-robots-achievement":
            data = [readInt(f), hexed(f.read(4))]
        case "deconstruct-with-robots-achievement":
            data = readInt(f)
        case "deliver-by-robots-achievement":
            data = hexed(f.read(8))
        case "dont-build-entity-achievement":
            data = hexed(f.read(4))
        case "dont-craft-manually-achievement":
            data = hexed(f.read(8))
        case "dont-use-entity-in-energy-production-achievement":
            data = readDouble(f)
        case "finish-the-game-achievement":
            data = hexed(f.read(4))
        case "group-attack-achievement":
            data = hexed(f.read(4))
        case "kill-achievement":
            data = readDouble(f)
        case "player-damaged-achievement":
            data = [readFloat(f), readBool(f)]
        case "produce-achievement":
            data = readDouble(f)
        case "produce-per-hour-achievement":
            data = readDouble(f)
        case "research-achievement":
            data = hexed(f.read(4))
        case "train-path-achievement":
            data = readDouble(f)
        case "EOF":
            data = "EOF"
        case _:
            raise ValueError(f"Unknown achievement type: {indexLink[str(index)]}")
    return {"index": index, "content": data}


def readAchievements(f: io.BufferedReader | io.BytesIO) -> dict:
    achievements = dict()
    achievements["version"] = readVersionString(f)
    readBool(f)  # docs don't talk about this but it's just like mod settings
    achievements["header"] = readShortArray(f, readHeader)
    indexLink = {}
    for achs in achievements["header"]:
        achType = achs["type"]
        for ach in achs["achs"]:
            indexLink[ach["index"]] = achType
    print(json.dumps(indexLink, indent=4))
    achievements["content"] = readShortArray(f, readContent, indexLink=indexLink)


# print("meow")


# arrays use short rather than int for length

# version sting
# random false bool
# array of length 17, that should be of type string
# space optimized string that says "achievement"
# array of length 1 , unknown of type, assuming string
# space optimized string that says "so-long-and-thanks-for-all-the-fish"
# 2 bytes (short ?, array?) &\u00 , would be 38 if short
# space optimized string that says "build-entity-achievement"
