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
import traceback, json


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


@app.route('/not_allow', methods=['GET'])
def deny(error):
    return 'You IP address is not in white list...'


@app.route("/gsearch/hotWord/personalizedRecommendation", methods=("POST", "GET"))
def index():
    try:
        # 获取参数
        # p = request.json or request.args
        # print(p)
        # global redis_buffer
        # global mysql_buffer
        # if redis_buffer is None:
        #     print('reload buffer --- redise')
        #     redis_buffer = redis_memory()
        # if mysql_buffer is None:
        #     print('reload buffer --- mysql')
        #     mysql_buffer = mysql_memory()
        #
        # param = request.get_data()
        # p = json.loads(param.decode("utf-8"))
        # print(type(param))
        # print(type(p))
        # print("redis_buffer: {}".format(redis_buffer))
        # print("mysql_buffer: {}".format(mysql_buffer))

        # if p is None:
        #     raise Exception("请输入参数")
        # result = find_user_similarity_keywords(redis_buffer, mysql_buffer, p)
        # return jsonify(result)
        return main_dbs.get_user_by_id(199)

    except Exception as e:
        error = traceback.format_exc()
        return error
