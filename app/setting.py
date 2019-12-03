# encodig=utf-8

class ASConfig(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        # {  # 第一个任务
        #     'id': 'job1',
        #     'func': 'app.task.TimeTasks:method_test1',
        #     'args': (1, 2),
        #     'trigger': 'cron',  # cron表示定时任务
        #     'hour': 19,
        #     'minute': 27
        # },
        {  # 第一个任务
            'id': 'job1',
            'func': 'app.task.TimeTasks:method_test1',
            'args': (1, 2),  # 入参
            'trigger': 'interval',  # cron表示定时任务
            'seconds': 3,
        },
        {  # 第二个任务，每隔5S执行一次
            'id': 'job2',
            'func': 'app.task.TimeTasks:method_test2',  # 方法名
            'args': (3, 2),  # 入参
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 3,
        }
    ]


# redis前缀
redis_perfix = {
    'hot_key_perfix': 'bangdan',
    'user_key_perfix': 'al'
}

db_config_local = {
    'DB_USER': 'dev_write',
    'DB_PSW': 'dev_write',
    'DB_NAME': 'global_search',
    'DB_HOST': '192.168.115.223',
    'DB_PORT': 3306,
    'DB_CHARSET': 'utf8'
}

db_config_release = {
    'DB_USER': 'testgsearchdbjlw',
    'DB_PSW':  '$jxuxju9f@',
    'DB_NAME': 'testgsearchdbjl',
    'DB_HOST': 'testidpaydb01.mysql.rds.aliyuncs.com',
    'DB_PORT': 3306,
    'DB_CHARSET': 'utf8'
}

redis_config_local = {
    'RD_PSW': None,
    'RD_HOST': '0.0.0.0',
    'RD_PORT': 6379,
    'RD_CHARSET': 'UTF8',
    'TEST_DB': 0,
    'TEMP_DB': 15,  # 缓存db
    'RECORD_DB': 2  # 用户访问db
}

redis_config_release = {
    'RD_PSW': 'w2Wzp^vm',
    'RD_HOST': '10.117.106.97',
    'RD_PORT': 7379,
    'RD_CHARSET': 'UTF8',
    'TEST_DB': 0,
    'TEMP_DB': 15,  # 缓存db
}

redis_config_test = {
    'RD_PSW': '993kf4wK9d',
    'RD_HOST': 'r-bp1xaotsrn21sdk8n6.redis.rds.aliyuncs.com',
    'RD_PORT': 6379,
    'RD_CHARSET': 'UTF8',
    'TEST_DB': 0,
    'TEMP_DB': 15,  # 缓存db
}

redis_config = redis_config_test
db_config = db_config_release
