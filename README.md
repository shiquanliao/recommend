```shell script
# 在208测试服务器上 python环境搭建为：py3.6_gunicorn虚拟环境
# 需要先进入到虚拟环境中
source py3.6_gunicorn/bin/activate
gunicorn --worker-class=gevent --worker-connections=500 --workers=8 -b 0.0.0.0:16736 runserver:app &
```

[如何优雅的退出/关闭/重启gunicorn进程](https://cloud.tencent.com/developer/article/1366142)
```shell script
# 当报错这样的时候
File "/usr/lib/python2.7/dist-packages/gunicorn/util.py", line 143, in load_class
RuntimeError: You need gevent installed to use this worker.

# 解决办法
which gunicorn
cat /usr/local/bin/gunicorn
# 第一行可能是python2.7 需要修改为python3

pstree -ap|grep gunicorn
kill -9 主进程
```