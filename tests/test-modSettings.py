import io
import sys
import time

sys.path.append("./")

# read and write the mod settings to make sure it is the same
from FactorioAPI.Data.Files.modSettings import readModSettings, writeModSettings
from FactorioAPI.Utils import getDataHash, getFileHash


modSettingsFile = "./tests/mod-settings.dat"
print("Testing Mod Settings IO")
start = time.time()
with open(modSettingsFile, "rb") as f:
    modSettings = readModSettings(f)

ogHash = getFileHash(modSettingsFile)

newData = io.BytesIO()
writeModSettings(newData, modSettings)
newData.seek(0)
newHash = getDataHash(newData.read())
stop = time.time()

try:
    assert ogHash == newHash
    print("Hashes match")
except AssertionError:
    print("Hashes don't match")
    print("Original: " + ogHash)
    print("New     : " + newHash)
print(f"Test took {stop-start:.5f} seconds")
