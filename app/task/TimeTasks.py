from app.dbs import main_dbs
from app.utils import DateUtil
from app.setting import redis_perfix


def method_test1(a, b):
    print(a + b)


def method_test2(a, b):
    print(a + b)


def load_hot_key_tag_task(bufferData):
    """
    拿到全部热词 bangdan_*
    :return:
    """
    # print("load_hot_key_tag_task ----- time is {}".format(DateUtil.now_datetime()))
    # hot_buffer = main_dbs.get_hot_key_tag_from_redis(redis_perfix['hot_key_perfix'], "*")
    # print(type(hot_buffer))
    # print(hot_buffer)
    # bufferData.set_hot_key_tag_buffer(hot_buffer)

    # 切换到mysql数据库
    hot_buffer1 = main_dbs.get_hot_key_tag_from_mysql()
    if hot_buffer1 is not None:
        print("update hot_buffer")
        print(hot_buffer1)
        bufferData.set_hot_key_tag_buffer(hot_buffer1)


def load_user_key_tag_task(bufferData):
    """
    拿到全部用户标签
    :param bufferData:
    :return:
    """
    bufferData.set_user_key_tag_buffer(main_dbs.get_user_keywords_tags_from_redis("al_*"))
