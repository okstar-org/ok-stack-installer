#!/bin/python3

import os
import subprocess  
import sys
from pathlib import Path

 
DIR = os.path.dirname(__file__)  
aptOs = ["Ubuntu", "Debian"]
dnfOs = ["Fedora", "CentOS", "Rocky", "Redhat", "Alibaba", "Circle", "OpenCloudOS"]

class OsInfo:
    name = ""
    kernel = ""
    arch = ""
    version = ""

    def __init__(self):
        pass

    def toString(self):  
        # 类的方法，用于显示对象的信息  
        return (f"Name: {self.name}, Version: {self.version}, Kernel: {self.kernel}, Arch: {self.arch}") 
    
    def isDeb(self):
        return self.name in aptOs
    
    def isDnf(self):
        return self.name in dnfOs

def exit(code):
    sys.exit(code)

def isSupport(o: OsInfo):
    if(o.isDeb()):
        return True
    elif(o.isDnf()):
        return True
    return False

def getOs():
    try:
        cmd = ['hostnamectl']
        # 调用hostnamectl命令并捕获其标准输出  
        result = subprocess.run(cmd, capture_output=True, text=True)  

        # 检查命令是否成功执行
        if result.returncode != 0:
            # 如果命令执行失败，打印错误信息  
            print(f"Error executing command: {result.stderr}")
            exit(1)
        else:
            os = OsInfo() 
            # 输出hostnamectl的结果  
            for line in result.stdout.splitlines():
                if line.strip().startswith("Operating System:"):
                    osNameVer = line.strip().split(": ")[1].strip()
                    arr = osNameVer.split(" ")
                    os.name = arr[0]
                    os.version = arr[1]
                elif line.strip().startswith("Kernel:"):
                    os.kernel = line.strip().split(": ")[1].strip()
                elif line.strip().startswith("Architecture:"):
                    arch = line.strip().split(": ")[1].strip()
                    if(arch == "x86-64" or arch == "x86_64" or arch == "amd64"):
                        os.arch="x64"
                    else:
                        os.arch="x86"
            return os
    except FileNotFoundError:
        print(f"Can not run command:{cmd}.")

def updateOs(os):
    if os.isDeb():
        result = subprocess.run(['apt', 'update'])
        if result.returncode != 0:
            return False
        result = subprocess.run(["apt", 'upgrade', '-y'])
        if result.returncode != 0:
            return False
    elif os.isDnf():
        result = subprocess.run(['dnf', 'update'])
        if result.returncode != 0:
            return False
    else:
        return False
    return True



def setupDocker(o: OsInfo):
    print("Set up docker.")
    result = os.system("which docker")
    if (not result == 0):
        if(o.isDeb()):
            result = subprocess.run(['apt', '-y', 'install', 'docker.io', 'docker-compose'])
            if(result.returncode != 0):
                print(f"Install docker is failed:{result.returncode}")
                return False
        elif(o.isDnf()):
            result = subprocess.run(['dnf', 'install', 'podman', 'podman-compose'])
            if(result.returncode != 0):
                print(f"Install docker is failed:{result.returncode}")
                return False
        print("Set up docker is completed.")
    return True