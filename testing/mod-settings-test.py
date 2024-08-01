import json
import sys
import time

sys.path.append("./")
from FactorioAPI.Data.IO.read import readBool, readVersionString

from FactorioAPI.Data.Files.modSettings import (
    readModSettings,
    readPropertyTree,
    writeModSettings,
)

from FactorioAPI.Data.Utils import getFileHash


file = "./testing/mod-settings.dat"
with open(file, "rb") as f:
    start = time.time()
    settings = readModSettings(f)
    stop = time.time()
    print(f"Parsing took {stop-start:.5f} seconds")

with open("./testing/mod-settings.json", "w") as f:
    f.write(json.dumps(settings, indent=4))

with open("./testing/mod-settings-2.dat", "wb") as f:
    writeModSettings(f, settings)

ogHash = getFileHash(file)
newHash = getFileHash("./testing/mod-settings-2.dat")
try:
    assert ogHash == newHash
except AssertionError:
    print("Hashes don't match")
    print("Original: " + ogHash)
    print("New     : " + newHash)
    with open("./testing/mod-settings-2.dat", "rb") as f:
        with open(file, "rb") as f2:
            match = True
            while match:
                match = f.read(1) == f2.read(1)
            print("UnMatched at byte " + str(f.tell()))

# with open("./testing/mod-settings-2.json","w") as f:
#     f.write(json.dumps(readModSettings("./testing/mod-settings-2.dat"),indent=4))
