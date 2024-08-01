import json
import sys
import time

# sys.path.append("./")
from FactorioAPI.Data.IO.read import readBool, readVersionString
from FactorioAPI.Data.Files.achievements import (
    readAchievements,
    readArrayWithContext,
    readShortArray,
    readHeader,
    readContent,
)

f = open("./testing/achievements.dat", "rb")

achs = readAchievements(f)

with open("./testing/achievements.json", "w") as outfile:
    outfile.write(json.dumps(achs, indent=4))
