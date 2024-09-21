#!/bin/python3
import sys
import os
import subprocess
import platform
from platform import OsInfo

def upDepends(o: OsInfo, build: bool):
    print("Startup ...")
    os.chdir("depends")


    cmd=['up', '-d', '--remove-orphans'];
    if (build):
        cmd = cmd + ['--build']

    if(o.isDeb()):
        result = subprocess.run(['docker compose' ]+cmd)
        return result.returncode == 0
    elif(o.isDnf()):
        result = subprocess.run(['podman-compose' ]+cmd)
        return result.returncode == 0
    return True


def start(build: bool):
    result = upDepends(platform.getOs(), build)
    if(not result):
        print("Start failed.")
    else:
        print("Started successfully.")

if(len(sys.argv) > 1 and sys.argv[1]=='--build'):
    start(True)
else:
    start(False)