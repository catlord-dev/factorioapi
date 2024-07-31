import io
from typing import Any, Callable

from FactorioAPI.Data.IO.read import readArray, readBool, readString, readUShort, readVersionString

def readShortArray(
    f: io.BufferedReader | io.BytesIO,
    objectDecoder: Callable[[io.BufferedReader | io.BytesIO], Any]
) -> list:
    """Reads variable amount of bytes and interprets them as an array.
    For arrays whose length is stored as a 

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
        objectDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the object.

    Returns:
        list: The bytes read as an array.
    """
    arrayLength = readUShort(f)
    array = []
    for i in range(arrayLength):
        array.append(objectDecoder(f))
    return array

def readHeader(f: io.BufferedReader | io.BytesIO) -> dict:
    print("Type      :",readString(f,spaceOptimized=True)) # name
    print("String id :",readString(f,spaceOptimized=True)) # name
    print("index     :",readUShort(f,spaceOptimized=True)) # name

def readContent(f: io.BufferedReader | io.BytesIO) -> dict:
    pass

def readAchievements(f: io.BufferedReader | io.BytesIO) -> dict:
    achievements = dict()
    achievements["version"] = readVersionString(f)
    readBool(f) # docs don't talk about this but it's just like mod settings
    achievements["header"] = readArray(f, readHeader)
    achievements["content"] = readArray(f, readContent)
    
    
print("meow")


# arrays use short rather than int for length

#version sting
# random false bool
# array of length 17, that should be of type string
#space optimized string that says "achievement"
#array of length 1 , unknown of type, assuming string
# space optimized string that says "so-long-and-thanks-for-all-the-fish"
# 2 bytes (short ?, array?) &\u00 , would be 38 if short
# space optimized string that says "build-entity-achievement"
