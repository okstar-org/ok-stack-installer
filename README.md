# OkStackInstaller 部署文档
OkStackInstall 为 OkStack 系统部署参考文档，基于Python，Docker，DockerCompose实现。

## 准备条件
- 公网服务器1台（2核4G100G存储）
- 开放端口
    - 18443
    - 9090
    - 5222
- 公网域名1个以及子域名，如下：
    - 一级域名，okstar.org
    - 二级域名，kc.okstar.org    18443
    - 二级域名，meet.okstar.org  5222
    - 二级域名，stack.okstar.org 80

## 系统依赖
- Docker24+
- DockerCompose 2.19+
- Python3+
- Linux


## 安装项目
- 克隆代码
```shell
git clone https://github.com/okstar-org/ok-stack-installer.git
```

- 执行安装
```shell
cd ok-stack-installer
chmod a+x *.sh
./install.sh
```

## 配置服务


## 启动服务
```shell
# build参数可选，启动时重新构建镜像，用在修改docker-compose配置重新启动时
./startup.sh [--build]
```

## 停止服务
```shell
./shutdown.h
```

## 卸载项目
```shell
./uninstall.sh
# 删除本项目
sudo rm -rf ok-stack-installer
```

## 更新系统
```shell
# 重置版本
git reset --hard
# 拉取最新代码
git pull origin main
```

