#!/bin/python3

import os
import subprocess
import platform
from platform import OsInfo

def stopDepends(o: OsInfo):
    print("Shutdown ...")
    os.chdir("depends")
    if(o.isDeb()):
        subprocess.run(['docker-compose', 'stop'])
        return False
    elif(o.isDnf()):
        subprocess.run(['podman-compose', 'stop'])
        return False
    return True


def shutdown():
    result = stopDepends(platform.getOs())
    if(result):
        print("Stop failed.")

shutdown()