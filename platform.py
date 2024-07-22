#!/bin/python3

import subprocess  
import sys
from pathlib import Path
import os  

  

# 获取当前脚本的完整路径  

# 使用os.path.dirname获取当前脚本所在的目录  
DIR = os.path.dirname(__file__)  
print("DIR:", DIR)

aptOs = ["Ubuntu", "Debian"]
dnfOs = ["Fedora", "CentOS", "Rocky", "Redhat"]


class OS:
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
        return aptOs.index(self.name) >= 0
    
    def isDnf(self):
        return dnfOs.index(self.name) >= 0

def exit(code):
    sys.exit(code)

def isSupport(o: OS):
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
            os = OS() 
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


# def installJava(os):
#     print("Prepare for java.")

#     file='OpenJDK17U-jdk_' + os.arch + '_linux_hotspot_17.0.11_9.tar.gz'
#     if(Path(file).exists()):
#         print(f"Found java:{file}.")
#     else:
#         print(f"Download java:{file}")
#         result = subprocess.run(['curl', '-C','-', '-O','-L', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/'+file])
#         if(result.returncode != 0):
#             print(f"Download error:{result.returncode}")
#             return False

#     java_dir = DIR+'/jdk-17.0.11+9'
#     if(not Path(java_dir).exists()):
#         print(f"Extract java:{file}")    
#         result = subprocess.run(['tar', '-xzf', file])
#         if(result.returncode != 0):
#             print(f"Extract error:{result.returncode}")
#             return False

#     print(f"JAVA_HOME:{java_dir}")
#     return True

def setupDocker(o: OS):
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

def setupDepends(o: OS):
    print("cd depends")
    os.chdir("depends")
    if(o.isDeb()):
        subprocess.run(['docker-compose', 'up'])
        return False
    elif(o.isDnf()):
        subprocess.run(['podman-compose', 'up'])
        return False
    return True


o = getOs()
print(f"Os information: {o.toString()}")

if(not isSupport(o)):
    print("Your os was not supported!")
    exit(1)

# installedJava = installJava(o)
# if (not installedJava):
#     print(f"Install Java failed.")
#     exit(1)

installedDocker = setupDocker(o)
if (not installedDocker):
    print(f"Setup docker failed.")
    exit(1)

installedDepends = setupDepends(o)
if (not installedDepends):
    # build for depends
    print(f"Setup depends failed.")

# https://github.com/okstar-org/ok-stack-ui/releases/download/latest/ok-stack-ui.zip

