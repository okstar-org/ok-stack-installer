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

def run_command(command):
    """运行shell命令并捕获其输出和错误"""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        raise
def DebsetupDocker():
    # Step 1: 安装必要的一些系统工具
    print("Step 1: Installing necessary system tools...")
    commands = [
        "sudo apt-get update",
        "sudo apt-get install -y ca-certificates curl gnupg"
    ]
    for cmd in commands:
        run_command(cmd)
    # Step 2: 信任 Docker 的 GPG 公钥
    print("Step 2: Trusting Docker's GPG public key...")
    commands = [
        "sudo install -m 0755 -d /etc/apt/keyrings",
        f"curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        "sudo chmod a+r /etc/apt/keyrings/docker.gpg"
    ]
    for cmd in commands:
        run_command(cmd)
    # Step 3: 写入软件源信息
    print("Step 3: Writing repository information...")
    version_codename = subprocess.run(". /etc/os-release && echo \"$VERSION_CODENAME\"", shell=True, check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
    deb_line = f'deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu {version_codename} stable'
    with open("/tmp/docker.list", "w") as f:
        f.write(deb_line)
    run_command("sudo mv /tmp/docker.list /etc/apt/sources.list.d/docker.list")
    # Step 4: 安装Docker
    print("Step 4: Installing Docker...")
    commands = [
        "sudo apt-get update",
        "sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
    ]
    for cmd in commands:
        run_command(cmd)
    print("Docker installation completed successfully!")
    return True

def DnfsetupDocker():
    # Step 1: 安装必要的一些系统工具
    run_command("sudo yum install -y yum-utils")
    # Step 2: 添加软件源信息
    run_command("sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo")
    # Step 3: 安装Docker
    run_command("sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    # Step 4: 开启Docker服务
    run_command("sudo service docker start")

def setupDocker(o: OsInfo):
    print("Set up docker.")
    result = os.system("which docker")
    if (not result == 0):
        if(o.isDeb()):
            DebsetupDocker()
        elif(o.isDnf()):
            DnfsetupDocker()
        print("Set up docker is completed.")
    return True
