#!/bin/python3

import subprocess  
import sys
from pathlib import Path
import os  

import platform
from platform import OsInfo
  

o = platform.getOs()
print(f"Os information: {o.toString()}")

if(not platform.isSupport(o)):
    print("Your os was not supported!")
    exit(1)

installedDocker = platform.setupDocker(o)
if (not installedDocker):
    print(f"Setup docker failed.")
    exit(1)
