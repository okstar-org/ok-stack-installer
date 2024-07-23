#!/bin/python3
import sys
import os
import subprocess
import platform
from platform import OsInfo

def upDepends(o: OsInfo, build: bool):
    print("Startup ...")
    os.chdir("depends")
    if(o.isDeb()):
        subprocess.run(['docker-compose', 'up', '-d', '--remove-orphans',  '--build' if build else ''])
        return False
    elif(o.isDnf()):
        subprocess.run(['podman-compose', 'up', '-d', '--remove-orphans',  '--build' if build else ''])
        return False
    return True


def start(build: bool):
    result = upDepends(platform.getOs(), build)
    if(result):
        print("Start failed.")

if(len(sys.argv) > 1 and sys.argv[1]=='--build'):
    start(True)
else:
    start(False)