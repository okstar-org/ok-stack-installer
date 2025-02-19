#!/bin/python3

import os
import subprocess
import platform
from platform import OsInfo


def downDepends(o: OsInfo):
    print("Destory ...")
    os.chdir("depends")
    subprocess.run(['docker-compose', 'down'])
    return True

def uninstall():
    result = downDepends()
    if (result):
        print("Uninstall ...")
    else:
        print("Uninstall failed.")

uninstall()
print("Uninstall is completed.")