# sqladvisor-web
美团SQLAdvisor SQL优化建议工具的Web版，告别命令行。
* 项目中使用的美团SQL分析工具是在CentOS上编译的，所以建议部署到CentOS上。
* 该项目是使用Python的Flask框架开发的。
* 使用CentOS自带的Python版本,版本号是2.7.5。
* 再部署前建议先看一下[美团的分析工具文档](https://github.com/Meituan-Dianping/SQLAdvisor)

## 安装依赖
```
pip install -r requirements.txt
```

## 恢复数据库
```
python manage.py db upgrade
```

## 启动系统
进入sqladvisor-web
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

## 截图
![analysis](screenshot/WX20170330-145627.png)
![setting](screenshot/WX20170330-150957.png)
![his](screenshot/his.png)
