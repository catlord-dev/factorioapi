# this is more for formating and stuff than building but it may in the future be used to build the library
# looks like i can use it for building now :)

import os
from shutil import rmtree
import subprocess
import time

from dotenv import load_dotenv

load_dotenv()

start = time.time()
subprocess.run(["black", "./"])
print(f"Formatting Took {time.time() - start:.5f} seconds")
start = time.time()
# rmtree("./dist")
subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"])
print(f"Building Took {time.time() - start:.5f} seconds")


# subprocess.run(
#     [
#         "twine",
#         "upload",
#         "-p",
#         os.getenv("testPyPi"),
#         "--repository",
#         "testpypi",
#         "dist/*",
#         "--skip-existing",
#         "--non-interactive",
#     ]
# )

subprocess.run(
    [
        "twine",
        "upload",
        "-p",
        os.getenv("realPyPi"),
        "dist/*",
        "--skip-existing",
        "--non-interactive",
    ]
)
