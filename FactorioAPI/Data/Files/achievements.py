import io
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
        **kwargs: Arbitrary keyword arguments. These are passed to the objectDecoder function.

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


def readAchData(f: io.BufferedReader | io.BytesIO, achType: str, modded=False) -> dict:
    data = None
    match achType:
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
            if modded:
                data = "NoData"
            else:
                data = hexed(f.read(4))
        case "train-path-achievement":
            data = readDouble(f)
        case "achievement":
            data = "NoData"
        case "NoneType":
            data = "NoneType"
        case _:
            raise ValueError(f"Unknown achievement type: {achType}")
    return data


def readContent(f: io.BufferedReader | io.BytesIO, indexLink: dict) -> dict:
    index = readShort(f)
    # print(f.tell(), index)
    data = readAchData(f, indexLink[str(index)])
    return {"index": index, "content": data}


def readModdedContent(f: io.BufferedReader | io.BytesIO) -> dict:
    achType = readString(f, spaceOptimized=True)
    achName = readString(f, spaceOptimized=True)
    achData = readAchData(f, achType, modded=True)
    return {"type": achType, "name": achName, "data": achData}


def getIndexLink(achs: list) -> dict:
    indexLink = {}
    for achType in achs:
        achTypeName = achType["type"]
        for ach in achType["achs"]:
            indexLink[str(ach["index"])] = achTypeName
    indexLink["0"] = "NoneType"
    # index > ach type
    return indexLink


def getTracked(f: io.BufferedReader | io.BytesIO) -> list:
    """Reads a variable amount of bytes and interprets them as a series of shorts that represent tracked achievements
    Note: reads until the end of the file
    

    Args:
        f (io.BufferedReader | io.BytesIO): the file to read from

    Raises:
        ValueError: raises an error if the amount of bytes left is odd (shorts are 2 bytes)

    Returns:
        list: _description_
    """
    start = f.tell()
    f.read()
    space = f.tell()
    achsAmt = (space - start) / 2
    if int(achsAmt) != achsAmt:
        raise ValueError(
            "Tracked Achievement amount isn't able to be an integer, there is an odd amount of bytes, Malformed File?"
        )
    trackedAchs = []
    f.seek(start)
    for i in range(int(achsAmt)):
        trackedAchs.append(readShort(f))
    return trackedAchs


def readAchievements(f: io.BufferedReader | io.BytesIO, modded=False) -> dict:
    """
    Reads the achievements from the file assuming achievements.dat format.

    The returned dict is representive of the data of the file and it's structure,
    further data restructuring may be useful to make it more readable

    Args:
        f (io.BufferedReader | io.BytesIO): The file to read from.
        modded (bool, optional): Whether the file is modded. Defaults to False. if True then readModdedAchievements will be used

    Returns:
        dict: The achievement data
    """
    if modded:
        return readModdedAchievements(f)
    # format documentated at https://wiki.factorio.com/Achievement_file_format#File_Format
    # i had to update it since it was out of date at the time
    achievements = dict()
    achievements["version"] = readVersionString(f)
    achievements["randomBool"] = readBool(
        f
    )  # who knows why this exists, but mod settings also has it
    # achievement types,name and index , see https://wiki.factorio.com/Achievement_file_format#Achievement_Header_Info for more info
    achievements["header"] = readShortArray(f, readHeader)
    # make a dict to help link indexs to achievement types
    indexLink = getIndexLink(achievements["header"])
    # achievement index and data, see https://wiki.factorio.com/Achievement_file_format#Achievement_Content_Info for more info
    achievements["content"] = readShortArray(f, readContent, indexLink=indexLink)
    # what achivements are tracked using their index, see https://wiki.factorio.com/Achievement_file_format#File_Format for more info
    achievements["tracked"] = getTracked(f)
    return achievements


def readModdedAchievements(f: io.BufferedReader | io.BytesIO) -> dict:
    """
    Reads the achievements from the file assuming achievements-modded.dat format.

    The returned dict is representive of the data of the file and it's structure,
    further data restructuring may be useful to make it more readable

    Args:
        f (io.BufferedReader | io.BytesIO): The file to read from.

    Returns:
        dict: The achievement data
    """
    achievements = dict()
    # format documentated at https://wiki.factorio.com/Achievement_file_format#File_Format_2
    # i had to update it since it was out of date at the time, also WHY does modded have a slightly different format than normal, WHY.
    achievements["version"] = readVersionString(f)
    achievements["randomBool"] = readBool(
        f
    )  # who knows why this exists, but mod settings also has it

    achievements["header"] = readShortArray(f, readHeader)
    indexLink = getIndexLink(achievements["header"])
    # print(json.dumps(indexLink, indent=4))
    achievements["content"] = readArray(f, readModdedContent)
    achievements["tracked"] = getTracked(f)
    return achievements


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
