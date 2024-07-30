def readPTString(f: io.BufferedReader | io.BytesIO) -> str:
    """Reads variable amount of bytes and interprets them as a property tree string.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        str: The bytes read as a property tree string.
    """
    whyisthishere = readBool(f)
    if whyisthishere:
        return None
    return readString(f,spaceOptimized=True)

    
def readPropertyTree(f: io.BufferedReader | io.BytesIO) -> dict:
    """Reads variable amount of bytes and interprets them as a property tree.

    Args:
        f (io.BufferedReader | io.BytesIO): A file-like object or bytes buffer.

    Returns:
        dict: The bytes read as a property tree.
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
        return readArray(f,readPropertyTree)
    elif dataType == 5:
        return readDict(f,readPTString,readPropertyTree)