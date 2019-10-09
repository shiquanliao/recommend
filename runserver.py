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

from flask import Flask, jsonify, request

redis_buffer = None
mysql_buffer = None

def init_buffer():
    global redis_buffer
    global mysql_buffer
    if redis_buffer is None:
        print('init buffer --- redise')
        redis_buffer = redis_memory()
    if mysql_buffer is None:
        print('init buffer --- mysql')
        mysql_buffer = mysql_memory()


def Ngram_distance(str1, str2, n=2):
    tmp = ' ' * (n - 1)
    str1 = tmp + str1 + tmp
    str2 = tmp + str2 + tmp
    set1 = set([str1[i:i + n] for i in range(len(str1) - (n - 1))])
    set2 = set([str2[i:i + n] for i in range(len(str2) - (n - 1))])
    setx = set1 & set2
    len1 = len(set1)
    len2 = len(set2)
    lenx = len(setx)
    num_dist = len1 + len2 - 2 * lenx
    num_sim = 1 - num_dist / (len1 + len2)
    return {'dist': num_dist, 'sim': num_sim}


def redis_memory():
    redisurl = '10.117.106.97'
    redisport = 7379
    redispassword = 'w2Wzp^vm'
    redis_result = redis.Redis(host=redisurl, port=7379, password=redispassword, db=15, decode_responses=True)
    return redis_result


def find_user_keywords_tags(r, input_imei):
    # redisurl = 'r-bp1xaotsrn21sdk8n6.redis.rds.aliyuncs.com'
    # redisport = 6379
    # redispassword = '993kf4wK9d'
    # r = redis.Redis(host=redisurl, port=6379, password=redispassword, db=0, decode_responses=True)
    # # 自己改参数，key规则为 al_+md5(imei) ,里面是map结构
    # key = 'al_' + hashlib.md5(input_imei).hexdigest()
    # print(key)

    # return r.hgetall(key).key()[:-1]

    # redisurl = '192.168.115.223'
    # redisport = 7379
    # redispassword = 'w2Wzp^vm'
    # r = redis.Redis(host=redisurl, port=7379, password=redispassword, db=15, decode_responses=True)

    # 自己改参数，key规则为 al_+md5(imei) ,里面是map结构
    # key = 'al_' + hashlib.md5(input_imei.encode("utf8")).hexdigest()
    key = 'al_' + input_imei
    # print(r.hgetall(key).keys())
    return list(r.hgetall(key).keys())[:20]


def mysql_memory():
    conn = pymysql.connect(host='perftestdb01.mysql.rds.aliyuncs.com', user='testsearchdbw', passwd='testsearch@123',
                           db='testsearchdb',
                           charset='utf8')
    sql1 = "select keyword, keyword_tags, category, source from search_hot_word_with_sch_url_recommend"
    mysql_result = pd.read_sql_query(sql1, conn)
    # conn.close()
    return mysql_result


def find_hot_keywords_and_tags(mysql_mem, sources, types):
    # conn = MySQLdb.connect(host='192.168.115.223', user='dev_write', passwd='dev_write', db='global_search',
    #                        charset='utf8')

    # conn = pymysql.connect(host='192.168.115.223', user='dev_write', passwd='dev_write', db='global_search',
    #                      charset='utf8')

    mysql_result = mysql_mem.loc[(mysql_mem['category'] == types) & (mysql_mem['source'] == sources)]
    # mysql_result.reset_index(drop=True)
    mysql_result1 = mysql_result[:200]  # 200
    return mysql_result1


# def find_user_similarity_keywords(user_keyword_tags, hot_keywords, hot_keywords_tags, similarity_keywords_num,similarity_keywords_min):
def find_user_similarity_keywords(r, mysql_data, input_imei):
    # time.sleep(100)

    imei = input_imei['imei']
    news_source = input_imei['listNames'][0]['source']
    news_type = input_imei['listNames'][0]['category']
    similarity_keywords_num = input_imei['similarityKeywordsNum']
    similarity_keywords_min = input_imei['similarityKeywordsThreshold']

    # print(mysql_data.shape())
    hot_keywords_and_tags = find_hot_keywords_and_tags(mysql_data, news_source, news_type)
    hot_keywords = hot_keywords_and_tags['keyword']
    hot_keywords_tags = hot_keywords_and_tags['keyword_tags']
    hot_keywords.index = range(200)  # 200
    hot_keywords_tags.index = range(200)  # 200
    user_keyword_tags = find_user_keywords_tags(r, imei)
    # hot_keywords_tags.to_csv(r'/data/test_2.csv')

    # xiaoshuaiwujieguo
    if (user_keyword_tags == None) | (len(hot_keywords_and_tags) == 0):
        return -1
    user_keywords = {}
    distance = []
    order_number = []
    result = []

    # print(hot_keywords_tags.shape())
    # hot_keyword_tags = hot_keyword_tags.reset_index(drop=True)
    for j in range(len(hot_keywords)):
        # print(hot_keywords_tags[j])
        if (hot_keywords_tags[j] != None) & (user_keyword_tags != None):
            ngram_distance = Ngram_distance(hot_keywords_tags[j], str(user_keyword_tags), 2)
            distance.append(ngram_distance['sim'])
            order_number.append(j)

    # 取相似度前3，且相似度系数大于0.5

    d = {'col1': distance, 'col2': order_number}
    panadas_results = pd.DataFrame(data=d)
    panadas_results_sorted = panadas_results.sort_values(by='col1', ascending=False)
    # print(type(similarity_keywords_num))
    # print("panadas_results_sorted['col2']= ", panadas_results_sorted['col2'][:12])
    keywords_results = panadas_results_sorted['col2'][:int(similarity_keywords_num)].loc[
        panadas_results_sorted['col1'] > float(similarity_keywords_min)]  # 0.6较准确，但匹配的热词很少, 0.1

    for k1 in keywords_results:
        result.append(hot_keywords[k1])

    # keywords ={}
    # keywords = {"imei": imei,
    #             "similarity_keyword": result,
    #             "listNames": [
    #                 {
    #                     "source": news_source,
    #                     "category": news_type,
    #                 }],
    #             }

    keyword2 = []
    for i in range(len(result)):
        keyword1 = {
            "rank": i + 1,
            "keyword": result[i],
            "category": news_type,
            "source": news_source
        }
        keyword2.append(keyword1)
    keywords = {}
    keywords = {"imei": imei,
                "hotwords": keyword2
                }

    # elapsed = (time.clock() - start)
    # print("Time used:", elapsed)

    return keywords
    # keywords=[]
    # return keywords

# @app.route("/gsearch/hotWord/personalizedRecommendation", methods=("POST", "GET"))
# def index():
#     try:
#         # 获取参数
#         # p = request.json or request.args
#         # print(p)
#         # global redis_buffer
#         # global mysql_buffer
#         # if redis_buffer is None:
#         #     print('reload buffer --- redise')
#         #     redis_buffer = redis_memory()
#         # if mysql_buffer is None:
#         #     print('reload buffer --- mysql')
#         #     mysql_buffer = mysql_memory()
#         #
#         # param = request.get_data()
#         # p = json.loads(param.decode("utf-8"))
#         # print(type(param))
#         # print(type(p))
#         # print("redis_buffer: {}".format(redis_buffer))
#         # print("mysql_buffer: {}".format(mysql_buffer))
#
#         # if p is None:
#         #     raise Exception("请输入参数")
#         # result = find_user_similarity_keywords(redis_buffer, mysql_buffer, p)
#         # return jsonify(result)
#         return main_dbs.get_user_by_id(199)
#
#     except Exception as e:
#         error = traceback.format_exc()
#         return error

if __name__ == '__main__':
    # app.run(host="192.168.115.70", port=44757)
    # app.run(host="192.168.115.227", port=16735)
    # app.run(host="127.0.0.1", port=4375)
    # app.run(host="0.0.0.0",port =16735)
    # app.run(host="0.0.0.0",port=16735,debug=False,threaded=True)
    print("main function !!!")
    http_server = WSGIServer(("0.0.0.0", 8890), app)
    http_server.serve_forever()
