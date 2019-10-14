# coding=utf-8
'''
Created on 2019-10-09
main模块涉及的数据库操作
可以是mysql，也可以是mongodb
使用什么数据库，什么orm均不限制
@author: ShiQuan
'''
from app.dbs.inc.Redis import RedisMysqlCache
from app.dbs.inc.Mysql import Mysql

redisBuffer = RedisMysqlCache()


def get_user_by_id(u_id):
    '''
    get the user information
    '''
    # 执行sql，获得数据，返回给views层使用
    return {'name': 'hzwangzhiwei', 'sex': 1, 'uid': u_id}


# 获取tid的测试信息
def get_test_by_id(test_id, use_redis_cache=True):
    sql = "select keyword, keyword_tags, category, source from search_hot_word_with_sch_url_recommend"
    params = (test_id,)

    # 该方法你用redis缓存
    if use_redis_cache:
        return redisBuffer.select_one(sql, params)
    else:
        return Mysql().exec_select_one(sql, params)


# hot_key
def get_hot_key_tag_from_redis(source, category):
    key = source + "_" + category
    # print("hot_key_tag key is {}".format(key))
    global redisBuffer
    return redisBuffer.select_hot_key_tag_no_mysql(key)


def get_user_keywords_tags_from_redis(key):
    # key = 'al_' + input_imei
    global redisBuffer
    return redisBuffer.select_user_key_tag_no_mysql(key)
