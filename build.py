# this is more for formating and stuff than building but it may in the future be used to build the library


import subprocess
import time

start = time.time()
subprocess.run(["black", "./"])
print(f"Formatting Took {time.time() - start:.5f} seconds")
