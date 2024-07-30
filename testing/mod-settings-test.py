import json
import sys
import time
sys.path.append('./')
from FactorioAPI.Data.IO import read



settings = {}

file = "./testing/mod-settings.dat"
with open(file,"rb") as f:
    version = read.readVersionString(f)
    # print(f.tell())
    read.readBool(f)
    # print(f.tell())
    settings["version"] = version
    start = time.time()
    settings.update(read.readPropertyTree(f))
    stop = time.time()
    print(f"Parsing took {stop-start:.5f} seconds")
    
with open("./testing/mod-settings.json","w") as f:
    f.write(json.dumps(settings,indent=4))
