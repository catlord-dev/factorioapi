import io
from FactorioAPI.Data.IO.read import readArray, readBool, readDict, readDouble , readString, readUByte, readVersionString
from FactorioAPI.Data.IO.write import writeArray, writeBool, writeDict, writeDouble, writeString, writeUByte, writeVersionString


def readPTString(f: io.BufferedReader | io.BytesIO,returnString: bool = False) -> str:
    """Reads variable amount of bytes and interprets them as a property tree string.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.
        returnString (bool, optional): If true, returns an empty string instead of None when there is no string. Defaults to False.

    Returns:
        str: The bytes read as a property tree string.
    """
    whyisthishere = readBool(f)
    if whyisthishere:
        if returnString:
            return ""
        return None
    return readString(f,spaceOptimized=True)

    
def readPropertyTree(f: io.BufferedReader | io.BytesIO) -> None | bool | float | str | list | dict:
    """Reads variable amount of bytes and interprets them as a property tree.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        None | bool | float | str | list | dict: The bytes read as a property tree.
    """
    # print(f.tell())
    dataType = readUByte(f)
    # print(f.tell())
    anyTypeFlag = readBool(f) # an internal factorio thing, who knows what it does
    # print(f.tell())
    if dataType == 0:
        return None
    elif dataType == 1:
        return readBool(f)
    elif dataType == 2:
        return readDouble(f)
    elif dataType == 3:
        return readPTString(f)
    elif dataType == 4:
        # print("cool")
        return readArray(f,readPropertyTree)
    elif dataType == 5:
        return readDict(f,readPTString,readPropertyTree)

def readModSettings(f: io.BufferedReader | io.BytesIO) -> dict:
    """Reads the mod settings from a file or bytes buffer.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        dict: The mod settings.
    """
    settings = {}
    version = readVersionString(f)
    readBool(f)
    settings["version"] = version
    settings.update(readPropertyTree(f))
    return settings


def writePTString(f: io.BufferedWriter | io.BytesIO, data: str, emtpyAsNone: bool = False) -> None:
    """ Writes a property tree string to a file.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        data (str): The property tree string to write.
        emtpyAsNone (bool, optional): If true, treats an empty string as None. Defaults to False.
    """
    if data is None or (data == "" and emtpyAsNone):
        writeBool(f,True)
        return
    writeBool(f,False)
    writeString(f,data,spaceOptimize=True)


def writePropertyTree(f: io.BufferedWriter | io.BytesIO, data: None | bool | float | int | str | list | dict) -> None:
    # print(type(data))
    if data is None:
        writeUByte(f,0)
        writeBool(f,False)
        return
    elif type(data) == bool:
        writeUByte(f,1)
        writeBool(f,False)
        writeBool(f,data)
    elif type(data) == float or type(data) == int:
        writeUByte(f,2)
        writeBool(f,False)
        writeDouble(f,data)
    elif type(data) == str:
        writeUByte(f,3)
        writeBool(f,False)
        writePTString(f,data)
    elif type(data) == list:
        writeUByte(f,4)
        writeBool(f,False)
        writeArray(f,data,writePropertyTree)
    elif type(data) == dict:
        writeUByte(f,5)
        writeBool(f,False)
        writeDict(f,data,writePTString,writePropertyTree)
        
def writeModSettings(f: io.BufferedWriter | io.BytesIO, data: dict) -> None:
    """Writes the mod settings to a file.

    Args:
        f (io.BufferedWriter | io.BytesIO): A file-like object or bytes buffer.
        data (dict): The mod settings to write.
    """
    
    writeVersionString(f,data.pop("version"))
    writeBool(f,False)
    writePropertyTree(f,data)