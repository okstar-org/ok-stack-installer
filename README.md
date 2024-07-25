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
## 启动服务
```shell
# build参数可选，启动时重新构建镜像，用在修改docker-compose配置重新启动时
./startup.sh [--build]
```

## 配置服务

首次安装需要进行该步骤相关配置操作

### 配置Keycloak服务
- 登录：http://{kc_domain}:18080/admin/
- 输入帐号: `admin` 密码: `okstar` 登录后台.
- 到左上角，选择: `okstar`或者`ok-star`ream
- 到client列表, 选择`okstack`或者`ok-stack`
#### 配置 Authorization
- 点击`Authorization`菜单
- 找到`Resource`》`Default Resource`,点击`Create permission
```shell
Name      : Default Permissions
Policies  : Default Policy
Decision strategy: Unanimous
```
- 点击`Save`保存
- 左侧菜单，点击`Verify Profile`=》`Required Actions`，找到`Verify Profile`，关闭即可。

#### 配置 User Federation

- 点击左下角  `User Federation`，选择增加`LDAP`
> General options
```text
UI display name *   :ldap
Vendor *            :Other
```
> Connection and authentication settings
```text
Connection URL *    :ldap://apacheds:10389
Connection pooling  :On
Connection timeout  :10000
Bind type *         :simple
Bind DN *           :uid=admin,ou=system
Bind credentials *  :secret
# 可以点击Test测试是否成功
```

> LDAP searching and updating
```text
Edit mode *                 :WRITABLE
Users DN *                  :ou=users,dc=okstar,dc=org
Username LDAP attribute *   :uid
RDN LDAP attribute *        :uid
UUID LDAP attribute *   :entryUUID
User object classes *   :inetOrgPerson, organizationalPerson
Search scope        :Subtree
Read timeout        :10000
Pagination          :On
```

> Synchronization settings

```text
Import users        :On
Sync Registrations  :On
Periodic full sync  :On
Full sync period    :604800
Periodic changed users sync :On
Changed users sync period   :86400
```



至此，Keycloak认证服务器则配置完成

### 配置Openfire服务器
> 打开服务器地址 http://{meet_doamin}:9090/
- 第一步，选择合适的语言
- 第二步，服务器设置
  - 填入域名: meet.okstar.org
  - FQDN: meet.okstar.org
  - 限制管理控制台访问: 取消勾选
- 第三步，使用标准数据库
    - 选择MySQL数据库
    - 修改host和数据库名称其他不变，为：`db:3306/openfire`
    - 用户名:`root`，密码:`okstar`
- 第四步，设置LDAP服务器
    - 目录服务器 (LDAP)
    - 服务类型，选择“其他”
    - 设置连接，Protocol:`ldap`	主机:`apacheds`	端口:`10389`
    - 基础的DN:`ou=users,dc=okstar,dc=org`
    - 管理员DN:`uid=admin,ou=system`，密码: `secret`，点击测试显示成功即可
- 第五步，选择LDAP管理员
    - 第一项，输入`okstar`
    - 第二项，选择第一个选项：`The value provided above is a LDAP user.`
    - 第三项，点击`添加`列出用户即可，点击`完成`
- 第六步，登录到主界面
    - 输入管理员`okstar`和密码`okstar`。
    - 点击登录
- 第七步，上传插件
    - 克隆[REST-API-Client](https://github.com/okstar-org/ok-openfire-REST-API-Client)，构建得到插件包`rest-api-client-xx.jar`
    - 主界面，到一级菜单点击“插件”
    - 点击左侧“插件”，点击“浏览”选择对应插件，点击上传完成。
    - 到一级菜单，点击“服务器”=》“服务器设置”=》“REST API”。
    - 勾选：`Enabled - REST API requests will be processed.`
    - 勾选：`Secret key auth - REST API authentication over specified secret key.`
    - 复制保存起来：Secret key: `lqiKpoT.....`（后面用到）
    - 点击"save settings"保存设置


### 配置OkStack服务器
> 打开服务器地址 http://{stack_doamin}:1080/
    - 注册新帐号，登录成功之后。
    - 主界面，点击“系统管理”=》“基础设置”：
        - IM服务器地址:{meet_doamin}
        - IM服务器端口:5222
        - IM连接密钥: 为Secret key: `lqiKpoT.....`


## 停止服务
```shell
./shutdown.h
```

## 卸载项目

```shell
# 该卸载仅仅是移除容器
# mariadb数据可能因为权限无法删除需要手动执行（sudo）
./uninstall.sh

# 请删除相关本地缓存镜像,如下：
docker rmi okstarorg/ok-stack-backend
docker rmi depends-keycloak
docker rmi depends-apacheds

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

