# OkStackInstaller 部署文档
OkStackInstall 为 OkStack 系统（[前端](https://github.com/okstar-org/ok-stack-ui)、[后端](https://github.com/okstar-org/ok-stack-backend)）部署脚本，基于Python，Docker，DockerCompose实现。参考本文档即可完成OkStack系统的搭建，耗费时间大约在1小时！

## 准备条件
- 公网服务器1台（X64架构、2核、4G、100G存储）
- 目前支持系统如下：
    - Deb系：Ubuntu 22.04+, Debian 10+
    - Dnf系：Fedora 39+, CentOS 9+, Rocky 9+, Redhat 9+, Circle 9+, Alibaba(OpenAnolis Edition) 3+, OpenCloudOS 8.8

- 公网域名1个域名以及子域名，列如：
    - 一级域名，okstar.org
    - 二级域名，kc.okstar.org    端口：18080
    - 二级域名，meet.okstar.org  端口：5222
    - 二级域名，stack.okstar.org 端口：1080
> 如有防火墙，请开放相关所需端口。
> 针对云服务器内存较低情况，请设置swap交换分区配置swappiness=100，具体操作请询问GPT！


## 系统依赖
> 具体请参考相关操作系统命令或者官方文档
- Docker24+ Or latest Podman 
- DockerCompose 2.19+ Or latest PodmanCompose
- Python3+



## 安装项目
> 由于大陆网络不可言语的问题，安装时无法下载请多次重试！

- 克隆代码
```shell
git clone https://github.com/okstar-org/ok-stack-installer.git
```

- 执行安装
> 请使用root用户或者sudo执行命令，否则可能会出现莫名其妙的问题！
```shell
cd ok-stack-installer
chmod a+x *.sh

# 请安装指定版本，有beta、latest和指定版本格式：v{VERSION}
./install.sh ok-stack-{ce|ee}:beta       #开发/企业测试版
./install.sh ok-stack-{ce|ee}:latest     #开发/企业最新版本
./install.sh ok-stack-{ce|ee}:v{VERSION} #开发/企业指定版本，版本号请参考：https://github.com/okstar-org/ok-stack-backend/releases
```
## 启动服务
```shell
# build参数可选，启动时重新构建镜像，用在修改docker-compose配置重新启动时
./startup.sh [--build]
```

## 配置服务

首次安装需要进行该步骤相关配置操作

### 配置Keycloak服务
- 登录：http://{kc_domain}:8080/admin/
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
- 左侧菜单，点击`Authentication`=》`Required Actions`，找到`Verify Profile`，关闭即可。

#### 配置 User Federation（Settings）

> 点击左下角  `User Federation`，选择增加`LDAP`

- General options
```text
UI display name *   :ldap
Vendor *            :Other
```
- Connection and authentication settings
```text
Connection URL *    :ldap://apacheds:10389
Connection pooling  :On
Connection timeout  :10000
Bind type *         :simple
Bind DN *           :uid=admin,ou=system
Bind credentials *  :secret
# 可以点击Test测试是否成功
```

- LDAP searching and updating
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
- Synchronization settings

```text
Import users        :On
Sync Registrations  :On
Periodic full sync  :On
Full sync period    :604800
Periodic changed users sync :On
Changed users sync period   :86400
```
#### 配置字段映射（Mappers）

> 配置用户属性字段到ldap存储的映射，请按照如下字段列表配置：
User Model Attribute为 `user-attribute-ldap-mapper`，其它字段默认就行。

| Name *      |Mapper type * | LDAP Attribute * |
| ----------- | ----------- |  ----------- |
| Telephone number  |   telephone   |telephoneNumber
| Initials          |   initials    |initials
| Display name      |   nickname    |displayName
| description       |   description |description
| Province          |   province    |st
| City              |   city        |l
| Address           |   address     |streetAddress


至此，Keycloak认证服务器则配置完成

### 配置Openfire服务器
> 打开服务器地址 http://{meet_doamin}:9090/
- 第一步，选择合适的语言
- 第二步，服务器设置
  - 填入域名: meet.okstar.org
  - FQDN: meet.okstar.org
  - 限制管理控制台访问: **取消勾选**(否则设置成功之后无法登录)
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
    - 用户映射和组映射
    ```
    - 全名          {cn}{sn}
    - 头像          {photo}
    - 昵称                  {displayName}
    ==== 家庭 《====清空
    ==== 商业 ====
    - 街道地址              {streetAddress} 	
    - 城市 	                {l}
    - 州/省 	                {st}
    - 邮政编码 	            {postalCode}
    - 国家/地区              {co} 	
    - 职位名称 	            {title}
    - 部门 	                {departmentNumber}
    - 电话号码 	            {telephoneNumber}
    - 手机号码 	            {mobile}
    - 传真 	                {facsimileTelephoneNumber}
    - 寻呼机 	            {pager}
    ```
    - 点击继续即可
- 第五步，选择LDAP管理员
    - 第一项，输入`okstar`
    - 第二项，选择第一个选项：`The value provided above is a LDAP user.`
    - 第三项，点击`添加`列出用户即可，点击`完成`
- 第六步，登录到主界面
    - 输入管理员`okstar`和密码`okstar`。
    - 点击登录
- 第七步，上传插件
    - 克隆[REST-API-plugin](https://github.com/okstar-org/ok-openfire-restAPI-plugin.git)，构建得到插件包` restAPI-openfire-plugin-assembly.jar`
    - 主界面，到一级菜单点击“插件”
    - 点击左侧“插件”，点击“浏览”选择对应插件，点击上传完成。
    - 到一级菜单，点击“服务器”=》“服务器设置”=》“REST API”。
    - 勾选：`Enabled - REST API requests will be processed.`
    - 勾选：`Secret key auth - REST API authentication over specified secret key.`
    - 复制保存起来：Secret key: `lqiKpoT.....`（后面用到）
    - 点击"save settings"保存设置

### 配置OkStack服务器
- 打开服务器地址 http://{stack_doamin}:1080/
- 注册新帐号，登录成功之后。
- 主界面，点击“组织架构”=》“部门管理”：
    - 输入正确的组织信息：“名称”、“位置“、”URL“，保存即可。
    - 大约过一会儿，刷新显示完整的”编号“、”认证编号“，本过程正确完成。

- 主界面，点击“系统管理”=》“基础设置”：
    - IM服务器地址:{meet_doamin}
    - IM服务器管理端口:9090
    - IM连接密钥: 为Secret key: `lqiKpoT.....`
    - 刷新查看输入效果（无需保存）

### 登录系统
- OkStack 管理服务，请访问：https://{stack_domain}:1080
- IM 管理服务，请访问：http://{meet_doamin}:9090/
- KC 认证服务，请访问：http://{kc_domain}:8080/admin/
- 客户端，下载地址：
    - Github下载地址：https://github.com/okstar-org/ok-msg-desktop/releases
    - Snap：https://snapcraft.io/ok-msg
    - Flatpak：https://flathub.org/apps/org.okstar.ok-msg
    - 打开程序，选择``


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
- 更新项目
```shell
# 重置版本
git reset --hard
# 拉取最新代码
git pull origin main
```
- 执行安装
> 请参考上面的安装部分

- 删除原来容器和镜像，如下：

```shell
# 删除原来容器
docker rm depends_ok-stack_1
docker rm depends_ok-openfire_1
docker rm depends_db_1
docker rm depends_keycloak_1
docker rm depends_apacheds_1
# 删除镜像
docker rmi okstarorg/ok-stack-backend
docker rmi okstarorg/ok-openfire
docker rmi quay.io/keycloak/keycloak
docker rmi mariadb:10.6.15 #注意版本
docker rmi depends_apacheds
```
- 启动服务即可


## 配置Nginx反向代理 

### 为 OkStack
```
    location / {
        proxy_cache off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://localhost:1080/;
    }

```

### 为 Keycloak
文件：depends/docker-compose.yml
```yaml
    - KC_HOSTNAME_STRICT=false
    - KC_PROXY_ADDRESS_FORWARDING=true
    - KC_PROXY_HEADERS=xforwarded
```

Nginx 配置
```
listen 443;
    listen [::]:443;
    server_name kc.okstar.org.cn;
    location / {
        proxy_cache off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_pass http://localhost:8080/;
    }
```

## 配置存储服务
本系统采用minio，配置信息位于`depends/docker-compose.yml`可根据需要仔细调整，初始内容如下：
```yml
  minio:
    image: "quay.io/minio/minio"
    restart: unless-stopped
    environment:
      MINIO_ACCESS_KEY: "minio"
      MINIO_SECRET_KEY: "minio1234567#"
    volumes:
      - ${DATA_DIR}/minio/data:/data
    ports:
      - 7001:7001
      - 7002:7002
    command: server -address ":7001" --console-address ":7002" /data  
    privileged: true
```
### 配置访问权限
- 访问管理后台`http://{host}:7002/`，输入配置的用户和密码
- 创建名称为`ok-stack`的Bucket，配置`Access Policy`为`Public`
- 进入`Access Keys`菜单，创建`Access key`和`Secret Key`,并且两个备份保存。

### 配置Nginx代理
> 为了便于浏览器域名访问，可以nginx配置如下：
```conf
server {
    listen 443;
    listen [::]:443;
    server_name s3.{host}; # 域名

    location / {
        proxy_cache off;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://localhost:7001/;
    }
}
```

### 后台配置Minio关联
- 进入`ok-stack`后台管理，`系统管理`/`集成设置`。
- 定位到`Minio 设置`菜单，参考如下配置。
```
访问Url：https://s3.{host}
写入Url：http://{host}:7001

# 写入对应Access Key和Secret Key
Access Key：frCFnmZZRlxq5FzssHmE
Secret Key：**********

```
- 保存即可。