import io
from typing import Any, Callable
import numpy as np

"""
readArray's objectDecoder arg, due to how an array has a object type and depending on the object there is an unkown amount of bytes between each object, because it could be 
different objects, also because arrays are sometimes used with object based types and those objects could contain strings and other stuff, i am just gonna have it take in a 
function and let it deal with it, maybe later once i got a reader and writer for all the data types, including objects, i will setup a dict with enums and stuff and make it 
easy but for now, i'm doing it like this

same thing above but for the dict

this was made based on the documentation at https://wiki.factorio.com/Data_types
and thank you very much to whoever made it for it is so nice, whether it be the factorio devs or a random person

"""





def readBool(f: io.BufferedReader | io.BytesIO) -> bool:
    """Reads a single byte and interprets it as a boolean value.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        bool: True if the byte read is b'\x01', otherwise False.
    """
    return f.read(1) == b'\x01'

def readByte(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads a single byte and interprets it as an integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The byte read as an integer.
    """
    return int.from_bytes(f.read(1),"little",signed=True)

def readUByte(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads a single byte and interprets it as an unsigned integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The byte read as an unsigned integer.
    """
    return int.from_bytes(f.read(1),"little",signed=False)


def readShort(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads 2 bytes and interprets them as a signed integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as a signed integer.
    """
    return int.from_bytes(f.read(2),"little",signed=True)

def readUShort(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads 2 bytes and interprets them as an unsigned integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as an unsigned integer.
    """
    return int.from_bytes(f.read(2),"little",signed=False)

def readInt(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads 4 bytes and interprets them as a signed integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as a signed integer.
    """
    return int.from_bytes(f.read(4),"little",signed=True)

def readUInt(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads 4 bytes and interprets them as an unsigned integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as an unsigned integer.
    """
    return int.from_bytes(f.read(4),"little",signed=False)

def readLong(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads 8 bytes and interprets them as a signed integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as a signed integer.
    """
    return int.from_bytes(f.read(8),"little",signed=True)

def readULong(f: io.BufferedReader | io.BytesIO) -> int:
    """Reads 8 bytes and interprets them as an unsigned integer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as an unsigned integer.
    """
    return int.from_bytes(f.read(8),"little",signed=False)

def readFloat(f: io.BufferedReader | io.BytesIO) -> float:
    """Reads 4 bytes and interprets them as a float.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        float: The bytes read as a float.
    """
    return np.frombuffer(f.read(4), dtype=np.float32, count=1)[0]

def readDouble(f: io.BufferedReader | io.BytesIO) -> float:
    """Reads 8 bytes and interprets them as a float.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        float: The bytes read as a float.
    """
    return np.frombuffer(f.read(8), dtype=np.float64, count=1)[0]

def readOptimizedNumber(f: io.BufferedReader | io.BytesIO) -> float:
    """Reads variable amount of bytes and interprets them as a int.
    some types use a space optimized number format for how many bytes they are, this is a helper function to make it easier
    check out space optimized on https://wiki.factorio.com/Data_types for more info
    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        int: The bytes read as a int.
    """
    number = readUByte(f)
    if number == 255:
        f.seek(f.tell() - 1)
        number = readUInt(f)
    return number
    

def readString(f: io.BufferedReader | io.BytesIO,spaceOptimized = False) -> str:
    """Reads variable amount of bytes and interprets them as a string.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        str: The bytes read as a string.
    """
    # print(f.tell())
    if spaceOptimized:
        dataLength = readOptimizedNumber(f)
    else:
        dataLength = readUInt(f)
    return f.read(dataLength).decode("utf-8")

def readArray(f: io.BufferedReader | io.BytesIO, objectDecoder: Callable[[io.BufferedReader | io.BytesIO], Any],spaceOptimized = False) -> list:
    """Reads variable amount of bytes and interprets them as an array.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
        objectDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the object. check the docstring at the top of the file for more info (me rambling)

    Returns:
        list: The bytes read as an array.
    """
    if spaceOptimized:
        arrayLength = readOptimizedNumber(f)
    else:
        arrayLength = readUInt(f)
    array = []
    for i in range(arrayLength):
        array.append(objectDecoder(f))
    return array
    
def readDict(f: io.BufferedReader | io.BytesIO, keyDecoder: Callable[[io.BufferedReader | io.BytesIO], Any], valueDecoder: Callable[[io.BufferedReader | io.BytesIO], Any],spaceOptimized = False) -> dict:
    """Reads variable amount of bytes and interprets them as a dictionary.
    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
        keyDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the key. check the docstring at the top of the file for more info (me rambling)
        valueDecoder (Callable[[io.BufferedReader | io.BytesIO], Any]): A function that reads the value. check the docstring at the top of the file for more info (me rambling)

    Returns:
        list: The bytes read as an array.
    """
    if spaceOptimized:
        dictLength = readOptimizedNumber(f)
    else:
        dictLength = readUInt(f)
    dict = {}
    for i in range(dictLength):
        key = keyDecoder(f)
        value = valueDecoder(f)
        dict[key] = value
    return dict
    
def readVersionString(f: io.BufferedReader | io.BytesIO) -> list[int]:
    """Reads variable amount of bytes and interprets them as a version string.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        list[int]: list of the major, minor, patch, and dev version
    """
    major = readUShort(f)
    minor = readUShort(f)
    patch = readUShort(f)
    dev = readUShort(f)
    return [major,minor,patch,dev]


    

# def decodeVersion(f):
#     nums = []
#     for i in range(4):
#         nums.append(readUShort(f))
#     return nums

# def getTreeType(byte):
#     if byte == 0:
#         return None
#     elif byte == 1:
#         return "Bool"
#     elif byte == 2:
#         return "double"
#     elif byte == 3:
#         return "string"
#     elif byte == 4:
#         return "list"
#     elif byte == 5:
#         return "dict"
    
# def readBool(f):
#     return True if f.read(1) == b"\x01" else False

# def readByte(f):
#     return int.from_bytes(f.read(1),"little",signed=True)

# def readUByte(f):
#     val = f.read(1)
#     return int.from_bytes(val,"little",signed=False)

# def readShort(f):
#     return int.from_bytes(f.read(2),"little",signed=True)

# def readUShort(f):
#     val = f.read(2)
#     return int.from_bytes(val,"little",signed=False)

# def readInt(f):
#     return int.from_bytes(f.read(4),"little",signed=True)

# def readUInt(f):
#     return int.from_bytes(f.read(4),"little",signed=False)

# def readLong(f):
#     return int.from_bytes(f.read(8),"little",signed=True)

# def readULong(f):
#     return int.from_bytes(f.read(8),"little",signed=False)

# def readFloat(f):
#     # return np.float32(f.read(4))
#     return float(np.frombuffer(f.read(4),dtype=np.float32)[0])

# def readDouble(f):
#     # return np.float64(f.read(8))
#     # bytess= f.read(8)
#     # print(f"Bytes : {bytess}\nNumpy Conversion : {float(np.frombuffer(bytess,dtype=np.float64)[0])}\nAnd back : {np.float64(float(np.frombuffer(bytess,dtype=np.float64)[0])).tobytes()}\n")
#     return float(np.frombuffer(f.read(8),dtype=np.float64)[0])

# def readString(f):
#     boo = readBool(f)
#     if boo:
#         return None
#     length = readUByte(f)
#     return f.read(length).decode("utf-8")

# def readDict(f):
#     dic = dict()
#     # print(f.tell())
#     numElements = readUInt(f)
#     # print(f.tell())
#     for i in range(numElements):
#         key = readString(f)
#         value = readPropTree(f)
#         dic[key] = value
#     return dic

# def readList(f):
#     numElements = readUInt(f)
#     list = []
#     for i in range(numElements):
#         list.append(readPropTree(f))
#     return list

# def readPropTree(f):
#     treeType = readUByte(f)
#     readBool(f)
#     if treeType == 0:
#         return None
#     elif treeType == 1:
#         return readBool(f)
#     elif treeType == 2:
#         return readDouble(f)
#     elif treeType == 3:
#         return readString(f)
#     elif treeType == 4:
#         return readList(f)
#     elif treeType == 5:
#         return readDict(f)
    
# def readSettings(f):
#     settings = dict()
#     version = decodeVersion(f)
#     # print(f.tell())
#     # print(version)
#     settings["version"] = version
#     # print(f.tell())
#     readBool(f) # who knows why they have it as such
#     # print(f.tell())
#     settings.update(readPropTree(f))
#     return settings
#     # print(f.tell())