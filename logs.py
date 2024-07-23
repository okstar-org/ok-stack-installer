#!/bin/python3

import os
import subprocess
import platform
from platform import OsInfo

def logsDepends(o: OsInfo):
    print("Show logs ...")
    os.chdir("depends")
    if(o.isDeb()):
        subprocess.run(['docker-compose', 'logs', '-f'])
        return False
    elif(o.isDnf()):
        subprocess.run(['podman-compose', 'logs', '-f'])
        return False
    return True


logsDepends(platform.getOs());