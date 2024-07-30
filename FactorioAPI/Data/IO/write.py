import io
from typing import Callable

import numpy as np


def writeBool(f: io.BufferedWriter | io.BytesIO, value: bool) -> None:
    """Writes a Boolean value to a file-like object or bytes buffer as 1 byte.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (bool): The value to write.
    """
    f.write(b"\x01" if value else b"\x00")


def writeByte(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an integer value to a file-like object or bytes buffer as 1 byte.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(1, "little", signed=True))


def writeUByte(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an unsigned integer value to a file-like object or bytes buffer as 1 byte.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """

    f.write(value.to_bytes(1, "little", signed=False))


def writeShort(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an integer value to a file-like object or bytes buffer as 2 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(2, "little", signed=True))


def writeUShort(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an unsigned integer value to a file-like object or bytes buffer as 2 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(2, "little", signed=False))


def writeInt(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an integer value to a file-like object or bytes buffer as 4 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(4, "little", signed=True))


def writeUInt(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an unsigned integer value to a file-like object or bytes buffer as 4 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(4, "little", signed=False))


def writeLong(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an integer value to a file-like object or bytes buffer as 8 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(8, "little", signed=True))


def writeULong(f: io.BufferedWriter | io.BytesIO, value: int) -> None:
    """Writes an unsigned integer value to a file-like object or bytes buffer as 8 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
    """
    f.write(value.to_bytes(8, "little", signed=False))


def writeFloat(f: io.BufferedWriter | io.BytesIO, value: float) -> None:
    """Writes a float value to a file-like object or bytes buffer as 4 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (float): The value to write.
    """
    f.write(np.float32(value).tobytes())


def writeDouble(f: io.BufferedWriter | io.BytesIO, value: float) -> None:
    """Writes a double value to a file-like object or bytes buffer as 8 bytes.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (float): The value to write.
    """
    f.write(np.float64(value).tobytes())


def writeSpaceOptimizedNumber(
    f: io.BufferedWriter | io.BytesIO, value: int, forceNo=False
) -> None:
    """Writes a space optimized integer value to a file-like object or bytes buffer.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (int): The value to write.
        forceNo (bool, optional): Whether to force no space optimization. Defaults to False.
    """
    if value < 255 and not forceNo:
        writeUByte(f, value)
    else:
        writeUInt(f, value)


def writeString(
    f: io.BufferedWriter | io.BytesIO, value: str, spaceOptimize: bool = False
) -> None:
    """Writes a string value to a file-like object or bytes buffer.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (str): The value to write.
        spaceOptimize (bool, optional): Whether to use space optimization. Defaults to False.
    """
    writeSpaceOptimizedNumber(f, len(value), not spaceOptimize)
    f.write(value.encode())


def writeArray(
    f: io.BufferedWriter | io.BytesIO,
    value: list,
    valueWriter: Callable[[io.BufferedWriter | io.BytesIO, object], None],
    spaceOptimize: bool = False,
) -> None:
    """Writes an array value to a file-like object or bytes buffer.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (list): The value to write.
        valueWriter (Callable[[io.BufferedWriter | io.BytesIO, object], None]): A function that writes a value to a file-like object or bytes buffer.
        spaceOptimize (bool, optional): Whether to use space optimization. Defaults to False.
    """
    writeSpaceOptimizedNumber(f, len(value), not spaceOptimize)
    for v in value:
        valueWriter(f, v)


def writeDict(
    f: io.BufferedWriter | io.BytesIO,
    value: dict,
    keyWriter: Callable[[io.BufferedWriter | io.BytesIO, object], None],
    valueWriter: Callable[[io.BufferedWriter | io.BytesIO, object], None],
    spaceOptimize: bool = False,
) -> None:
    """Writes a dict value to a file-like object or bytes buffer.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (dict): The value to write.
        keyWriter (Callable[[io.BufferedWriter | io.BytesIO, object], None]): A function that writes a key to a file-like object or bytes buffer.
        valueWriter (Callable[[io.BufferedWriter | io.BytesIO, object], None]): A function that writes a value to a file-like object or bytes buffer.
        spaceOptimize (bool, optional): Whether to use space optimization. Defaults to False.
    """
    writeSpaceOptimizedNumber(f, len(value), not spaceOptimize)
    for k, v in value.items():
        keyWriter(f, k)
        valueWriter(f, v)


def writeVersionString(f: io.BufferedWriter | io.BytesIO, value: list | str) -> None:
    """Writes a version string value to a file-like object or bytes buffer.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        value (list | str): The value to write.
    """
    if isinstance(value, str):
        value = value.split(".")
    for v in value:
        writeUShort(f, v)


# import io
# from typing import Any, Callable
# import numpy as np

# """
# readArray's objectDecoder arg, due to how an array has a object type and depending on the object there is an unkown amount of bytes between each object, because it could be
# different objects, also because arrays are sometimes used with object based types and those objects could contain strings and other stuff, i am just gonna have it take in a
# function and let it deal with it, maybe later once i got a reader and writer for all the data types, including objects, i will setup a dict with enums and stuff and make it
# easy but for now, i'm doing it like this

# same thing above but for the dict

# this was made based on the documentation at https://wiki.factorio.com/Data_types
# and thank you very much to whoever made it for it is so nice, whether it be the factorio devs or a random person

# """


# def readBool(f: io.BufferedReader | io.BytesIO) -> bool:
#     """Reads a single byte and interprets it as a boolean value.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         bool: True if the byte read is b'\x01', otherwise False.
#     """
#     return f.read(1) == b'\x01'

# def readByte(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads a single byte and interprets it as an integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The byte read as an integer.
#     """
#     return int.from_bytes(f.read(1),"little",signed=True)

# def readUByte(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads a single byte and interprets it as an unsigned integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The byte read as an unsigned integer.
#     """
#     return int.from_bytes(f.read(1),"little",signed=False)


# def readShort(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads 2 bytes and interprets them as a signed integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as a signed integer.
#     """
#     return int.from_bytes(f.read(2),"little",signed=True)

# def readUShort(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads 2 bytes and interprets them as an unsigned integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as an unsigned integer.
#     """
#     return int.from_bytes(f.read(2),"little",signed=False)

# def readInt(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads 4 bytes and interprets them as a signed integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as a signed integer.
#     """
#     return int.from_bytes(f.read(4),"little",signed=True)

# def readUInt(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads 4 bytes and interprets them as an unsigned integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as an unsigned integer.
#     """
#     return int.from_bytes(f.read(4),"little",signed=False)

# def readLong(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads 8 bytes and interprets them as a signed integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as a signed integer.
#     """
#     return int.from_bytes(f.read(8),"little",signed=True)

# def readULong(f: io.BufferedReader | io.BytesIO) -> int:
#     """Reads 8 bytes and interprets them as an unsigned integer.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as an unsigned integer.
#     """
#     return int.from_bytes(f.read(8),"little",signed=False)

# def readFloat(f: io.BufferedReader | io.BytesIO) -> float:
#     """Reads 4 bytes and interprets them as a float.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         float: The bytes read as a float.
#     """
#     return np.frombuffer(f.read(4), dtype=np.float32, count=1)[0]

# def readDouble(f: io.BufferedReader | io.BytesIO) -> float:
#     """Reads 8 bytes and interprets them as a float.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         float: The bytes read as a float.
#     """
#     return np.frombuffer(f.read(8), dtype=np.float64, count=1)[0]

# def readOptimizedNumber(f: io.BufferedReader | io.BytesIO) -> float:
#     """Reads variable amount of bytes and interprets them as a int.
#     some types use a space optimized number format for how many bytes they are, this is a helper function to make it easier
#     check out space optimized on https://wiki.factorio.com/Data_types for more info
#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         int: The bytes read as a int.
#     """
#     number = readUByte(f)
#     if number == 255:
#         f.seek(f.tell() - 1)
#         number = readUInt(f)
#     return number


# def readString(f: io.BufferedReader | io.BytesIO,spaceOptimized = False) -> str:
#     """Reads variable amount of bytes and interprets them as a string.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         str: The bytes read as a string.
#     """
#     # print(f.tell())
#     if spaceOptimized:
#         dataLength = readOptimizedNumber(f)
#     else:
#         dataLength = readUInt(f)
#     return f.read(dataLength).decode("utf-8")

# def readArray(f: io.BufferedReader | io.BytesIO, objectDecoder: Callable[[io.BufferedReader | io.BytesIO], Any],spaceOptimized = False) -> list:
#     """Reads variable amount of bytes and interprets them as an array.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
#         objectDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the object. check the docstring at the top of the file for more info (me rambling)

#     Returns:
#         list: The bytes read as an array.
#     """
#     if spaceOptimized:
#         arrayLength = readOptimizedNumber(f)
#     else:
#         arrayLength = readUInt(f)
#     array = []
#     for i in range(arrayLength):
#         array.append(objectDecoder(f))
#     return array

# def readDict(f: io.BufferedReader | io.BytesIO, keyDecoder: Callable[[io.BufferedReader | io.BytesIO], Any], valueDecoder: Callable[[io.BufferedReader | io.BytesIO], Any],spaceOptimized = False) -> dict:
#     """Reads variable amount of bytes and interprets them as a dictionary.
#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
#         keyDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the key. check the docstring at the top of the file for more info (me rambling)
#         valueDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the value. check the docstring at the top of the file for more info (me rambling)

#     Returns:
#         list: The bytes read as an array.
#     """
#     if spaceOptimized:
#         dictLength = readOptimizedNumber(f)
#     else:
#         dictLength = readUInt(f)
#     dict = {}
#     for i in range(dictLength):
#         key = keyDecoder(f)
#         value = valueDecoder(f)
#         dict[key] = value
#     return dict

# def readVersionString(f: io.BufferedReader | io.BytesIO) -> list[int]:
#     """Reads variable amount of bytes and interprets them as a version string.

#     Args:
#         f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

#     Returns:
#         list[int]: list of the major, minor, patch, and dev version
#     """
#     major = readUShort(f)
#     minor = readUShort(f)
#     patch = readUShort(f)
#     dev = readUShort(f)
#     return [major,minor,patch,dev]
