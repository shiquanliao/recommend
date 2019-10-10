# coding=utf-8
'''
Created on 2015年6月16日

@author: hzwangzhiwei
'''
from app import app
from app.dbs import test_dbs
from app.dbs import main_dbs
from app.others import tasks
from app.utils import OtherUtil
import traceback
import json
from flask import jsonify, request
from app.algorithm import NGRAMSimilarities
import time


@app.route('/', methods=['GET'])
def index_page():
    # async task
    tasks.count_to_10000()
    # 此处应该渲染首页模版
    try:
        rst = test_dbs.get_test_by_id('1')
    except:
        rst = {}
    return OtherUtil.object_2_dict(rst)


# 定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return '404'


@app.errorhandler(502)
def server_502_error(error):
    return '502'


@app.route("/gsearch/hotWord/personalizedRecommendation", methods=("POST", "GET"))
def index():
    try:
        param = request.get_data()
        # print(type(param))
        input_param = json.loads(param.decode("utf-8"))
        if input_param is None:
            raise Exception("请输入参数")

        # start_time = time.time()
        imei = input_param['imei']
        news_source = input_param['listNames'][0]['source']
        news_type = input_param['listNames'][0]['category']
        similarity_keywords_num = input_param['similarityKeywordsNum']
        similarity_keywords_min = input_param['similarityKeywordsThreshold']

        hot_key_tags_buffer = main_dbs.get_hot_key_tag_from_redis(news_source, news_type)
        user_key_tags_buffer = main_dbs.get_user_keywords_tags_from_redis(imei, similarity_keywords_num,
                                                                          similarity_keywords_min)
        # print("hot_key_tags_buffer is {}".format(hot_key_tags_buffer))
        # print("user_key_tags_buffer is {}".format(user_key_tags_buffer))
        # print(type(hot_key_tags_buffer))
        # print(type(user_key_tags_buffer))
        start_time = time.time()
        result = NGRAMSimilarities.find_user_similarity_keywords(user_key_tags_buffer, hot_key_tags_buffer, imei,
                                                                 news_source, news_type, similarity_keywords_num,
                                                                 similarity_keywords_min)
        print("elapsed_time is {}".format(time.time() - start_time))
        return jsonify(result)

    except Exception as e:
        error = traceback.format_exc()
        print(e)
        return error
