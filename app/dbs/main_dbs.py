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
mysqlBuffer = Mysql()
mysql_update_time = None


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


# def get_hot_key_tag_from_mysql():
#     # step1: 先获取表的更新时间
#     global mysqlBuffer
#     global mysql_update_time
#     print("mysql execute ...")
#     select_update_time = "select max(update_time) from search_hot_word_with_sch_url_recommend"
#     current_time = mysqlBuffer.exec_select(select_update_time, None)
#     if (mysql_update_time is not None) or (current_time == mysql_update_time):
#         print("get_hot_key_tag_from_mysql --- don`t update")
#         mysql_update_time = current_time
#         return None
#
#     # step2: 获取所有的source， category
#     source_category_sql = "select DISTINCT source,category from search_hot_word_with_sch_url_recommend"
#     temp = mysqlBuffer.exec_select(source_category_sql, None)
#     print("mysql: {}".format(temp))
#     print("type is :{}".format(type(temp)))
#
#     # step3: 循环更新所有的数据
#     for i, val in enumerate(temp):
#         source = val['source']
#         category = val['category']
#         print('source is: {}, category is: {}'.format(source, category))
#
#         data_sql = "select a.source,a.category,a.keyword,b.keyword_tags from search_hot_word_with_sch_url_recommend a join search_hot_word_with_sch_url b on a.source=b.source and a.category=b.category and a.keyword=b.keyword where a.source= %(source)s and a.category= %(category)s"
#         params = {"source": source, "category": category}
#         data = mysqlBuffer.exec_select(data_sql, params)
#         print(type(data))
#         print(len(data))

def get_hot_key_tag_from_mysql():
    # step1: 先获取表的更新时间
    global mysqlBuffer
    global mysql_update_time
    print("mysql execute ...")

    # 查询最大创建时间
    select_update_time = "select max(create_time) from search_hot_word_with_sch_url"
    current_time = mysqlBuffer.exec_select(select_update_time, None)[0]['max(create_time)']
    # print("current_time is: {}, mysql_update_time is: {}".format(current_time, mysql_update_time))
    if (mysql_update_time is not None) or (current_time == mysql_update_time):
        # print("get_hot_key_tag_from_mysql --- don`t update")
        return None

    # 查询存储时间
    mysql_update_time = current_time
    default_time_sql = "SELECT key_value,parameter from search_server_config " \
                       "where key_value= 'hotword_recommend_pool_time_hours'"
    result_select_config_time = mysqlBuffer.exec_select(default_time_sql, None)
    default_time = result_select_config_time[0]['parameter']
    # print(default_time)

    # 查询所有的分类，不需要重新分类了
    source_category_sql = "select DISTINCT source,category from search_hot_word_with_sch_url"
    source_category = mysqlBuffer.exec_select(source_category_sql, None)
    # print(source_category)
    result_dic = {}
    for i, val in enumerate(source_category):
        source = val['source']
        category = val['category']
        # 重新拉取一遍数据
        load_all_data_sql = "SELECT keyword,keyword_tags,tag,rise,search_num " \
                            "from search_hot_word_with_sch_url " \
                            "where create_time>=date_sub(NOW(), interval %s hour) " \
                            "and (keyword_tags is not null and keyword_tags!='' and keyword_tags != '[]') " \
                            "ORDER BY create_time desc"
        load_data = mysqlBuffer.exec_select(load_all_data_sql, default_time)
        key = source + "_" + category
        # dict_value = {}
        # for temp1 in enumerate(load_data):
        #     dict_value[temp1[1]['keyword']] = temp1[1]['keyword_tags']
        # result_dic[key] = dict_value

        result_dic[key] = load_data

    # print(result_dic)
    return result_dic


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
