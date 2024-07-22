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


## Clone 本项目
    
    git clone git@github.com:okstar-org/ok-stack-installer.git

## 执行安装
    chmod a+x install.sh
    ./install

## 配置系统
- Keycloak
- Openfire

