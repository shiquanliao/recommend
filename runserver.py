# -*- coding: utf-8 -*-
import pymysql
import redis
import hashlib
import time
import pandas as pd
import traceback, json
from app import app
from app.dbs import main_dbs

# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()
# gevent end


if __name__ == '__main__':
    # app.run(host="192.168.115.70", port=44757)
    # app.run(host="0.0.0.0",port=16735,debug=False,threaded=True)
    print("main function !!!")
    http_server = WSGIServer(("0.0.0.0", 8890), app)
    http_server.serve_forever()
