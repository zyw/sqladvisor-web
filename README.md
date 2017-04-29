# sqladvisor-web
美团SQLAdvisor SQL优化建议工具的Web版，告别命令行。
* 项目中使用的美团SQL分析工具是在CentOS上编译的，所以建议部署到CentOS上。
* 该项目是使用Python的Flask框架开发的。
* 使用CentOS自带的Python版本,版本号是2.7.5。
* 再部署前建议先看一下[美团的分析工具文档](https://github.com/Meituan-Dianping/SQLAdvisor)

# 系统搭建

## 1、安装git、wget和Mysql

```
sudo yum install git
sudo yum install wget
```
CentOS 7安装Mysql需要先现在Mysql的rpm文件。
```
wget http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm
rpm -ivh mysql57-community-release-el7-9.noarch.rpm
sudo yum install mysql-community-server
```
配置Mysql
```
mysql_secure_installation
```
执行上面命令设置root密码。
```
sudo systemctl enable mysqld
```
设置开机启动。

重启数据库
```
sudo systemctl mysqld restart
```
进入Mysql创建``sqladvisor``数据库

## 2、配置项目
```
git clone https://github.com/zyw/sqladvisor-web.git
```
下载项目。
```
cd sqladvisor-web
```
为了不报下面异常
```
root@pts/4 $ pip install MySQL-python
Collecting MySQL-python
  Using cached MySQL-python-1.2.5.zip
    Complete output from command python setup.py egg_info:
    sh: mysql_config: command not found
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-kWowP9/MySQL-python/setup.py", line 17, in <module>
        metadata, options = get_config()
      File "setup_posix.py", line 43, in get_config
        libs = mysql_config("libs_r")
      File "setup_posix.py", line 25, in mysql_config
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    EnvironmentError: mysql_config not found

    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-kWowP9/MySQL-python/
```
首先安装
```
sudo yum install python-devel mysql-community-devel -y
```

## 下面安装依赖
```
sudo pip install -r requirements.txt
```
## 修改数据库配置
编辑工程中的``config.py``文件
```
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://root:root@localhost/sqladvisor'
```
把第二个``root``修改成你安装Mysql时设置的密码。

## 恢复数据库
```
python manager.py db init
python manager.py db migrate
python manage.py db upgrade
```
经过上三条命令，``sqladvisor``数据库中的表已经被创建了。

## 启动系统

```
python manage.py runserver --host 0.0.0.0
```
## 部署sqladvisor-web
使用上面的命令是在开发环境启动Python Web应用，如果想要供多人使用还是使用```gunicorn```部署比较好。
* 安装```gunicorn```
```
pip install gunicorn
```
* 启动服务
```
gunicorn manage:app -p manage.pid -b 0.0.0.0:8000 -D
```
上面的命令启动一个监听0.0.0.0:8000 IP和端口的服务，-D是启动一个守护进程

## 3、截图
![analysis](screenshot/WX20170330-145627.png)
![setting](screenshot/WX20170330-150957.png)
![his](screenshot/his.png)
