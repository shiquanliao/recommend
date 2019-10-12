```shell script
# 在208测试服务器上 python环境搭建为：py3.6_gunicorn虚拟环境
# 需要先进入到虚拟环境中
source py3.6_gunicorn/bin/activate
gunicorn --worker-class=gevent --worker-connections=500 --workers=3 -b 0.0.0.0:16735 runserver:app
```