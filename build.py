# this is more for formating and stuff than building but it may in the future be used to build the library
# looks like i can use it for building now :)

import subprocess
import time

start = time.time()
subprocess.run(["black", "./"])
print(f"Formatting Took {time.time() - start:.5f} seconds")
start = time.time()
subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"])
print(f"Building Took {time.time() - start:.5f} seconds")
