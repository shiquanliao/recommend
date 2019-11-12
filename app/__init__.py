# -*- coding: utf-8 -*-
from flask import Flask
from app.setting import *
from flask_apscheduler import APScheduler
import os as os
from app.dbs import BufferData
from app.task import TimeTasks
from app.utils import Logging
import logging

import atexit
import fcntl
from flask_apscheduler import APScheduler

# create project object
app = Flask(__name__)
bufferData = BufferData.MySQLBufferData()
logger = Logging.Logger('./log/all.log', logging.ERROR, logging.DEBUG)
# app.config.from_object(ASConfig)  # 为实例化的flask引入配置

# def init(apps):
#     f = open("scheduler.lock", "wb")
#     try:
#         fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
#         print("scheduler is start...")
#         scheduler = APScheduler()
#         scheduler.init_app(apps)
#         scheduler.start()
#     except:
#         pass
#
#     def unlock():
#         fcntl.flock(f, fcntl.LOCK_UN)
#         f.close()
#
#     atexit.register(unlock)

# init(app)

# if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
#     print("scheduler is start...")
#     scheduler = APScheduler()
#     scheduler.api_enabled = True
#     scheduler.init_app(app)
#     scheduler.start()

TimeTasks.load_hot_key_tag_task(bufferData)

print("scheduler is start...")
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
# scheduler.add_job(func=TimeTasks.load_hot_key_tag_task, args=(bufferData,), trigger='interval', second=10, id="start")
scheduler.add_job(func=TimeTasks.load_hot_key_tag_task, args=(bufferData,), trigger='interval', minutes=5, id="start")
scheduler.start()

# 不能换位置
from app.views import main_views

"""
    这里添加我们的接口
"""

# app.run(debug=True)
