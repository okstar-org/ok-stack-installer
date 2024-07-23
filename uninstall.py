#!/bin/python3

import os
import subprocess
import platform
from platform import OsInfo


def downDepends(o: OsInfo):
    print("Destory ...")
    os.chdir("depends")
    if(o.isDeb()):
        subprocess.run(['docker-compose', 'down'])
        return False
    elif(o.isDnf()):
        subprocess.run(['podman-compose', 'down'])
        return False

    return True

def uninstall():
    result = downDepends(platform.getOs())
    if(result):
        print("Uninstall failed.")

uninstall()
print("Uninstall is completed.")