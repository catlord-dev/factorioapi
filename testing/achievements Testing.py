import json
import sys
import time

sys.path.append("./")
from FactorioAPI.Data.IO.read import readBool, readVersionString
from FactorioAPI.Data.Files.achievements import (
    readArrayWithContext,
    readShortArray,
    readHeader,
    readContent,
)

f = open("./testing/achievements.dat", "rb")

achs = dict()
achs["version"] = readVersionString(f)
readBool(f)  # docs don't talk about this but it's just like mod settings
achs["header"] = readShortArray(f, readHeader)
indexLink = {}
for achs2 in achs["header"]:
    achType = achs2["type"]
    for ach in achs2["achs"]:
        indexLink[str(ach["index"])] = achType
indexLink["0"] = "EOF"
print(json.dumps(indexLink, indent=4))
achs["content"] = readArrayWithContext(f, readContent, indexLink=indexLink)

with open("./testing/achievements.json", "w") as outfile:
    json.dump(achs, outfile, indent=4)
