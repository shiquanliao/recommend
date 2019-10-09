# -*- coding: utf-8 -*-
from flask import Flask
from app.setting import *
from flask_apscheduler import APScheduler
import os as os

import atexit
import fcntl
from flask_apscheduler import APScheduler


def init(apps):
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print("scheduler is start...")
        scheduler = APScheduler()
        scheduler.init_app(apps)
        scheduler.start()
    except:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)


# create project object
app = Flask(__name__)
app.config.from_object(ASConfig())  # 为实例化的flask引入配置
# if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
#     print("scheduler is start...")
#     scheduler = APScheduler()
#     scheduler.api_enabled = True
#     scheduler.init_app(app)
#     scheduler.start()


init(app)

# 不能换位置
from app.views import main_views
# app.run(debug=True)
