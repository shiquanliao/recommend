import csv
import redis
import os

redis_config = {
    'RD_PSW': '993kf4wK9d',
    'RD_HOST': 'r-bp1xaotsrn21sdk8n6.redis.rds.aliyuncs.com',
    'RD_PORT': 6379,
    'RD_CHARSET': 'UTF8',
    'TEST_DB': 0,
    'TEMP_DB': 15,  # 缓存db
}


class RedisMysqlCache(object):
    '''
    a redis cache for mysql
    '''

    def __init__(self, timeout=60 * 60,  # one hour
                 host=redis_config['RD_HOST'],
                 port=redis_config['RD_PORT'],
                 password=redis_config['RD_PSW'],
                 db=redis_config['TEMP_DB'],
                 charset=redis_config['RD_CHARSET']):
        # self.__db = redis.Redis(host=host, port=port, password=password, db=db, charset=charset,
        # decode_responses=True)
        self.__rdb = redis.ConnectionPool(host=host, port=port, password=password, db=db,
                                          decode_responses=True)
        self.__db = redis.StrictRedis(connection_pool=self.__rdb)
        print("-------------")
        self.timeout = timeout

    def select_user_key_tag_no_mysql(self, select_key, max_number=20):
        """
        获取redis数据库数据
        :param max_number: 最大标签数
        :param select_key: example: "al_imei"
        :return: list
        """
        # print('key is {}'.format(select_key))
        value = self.__db.hgetall(select_key)
        # value = self.__db.get(select_key)
        # print("redis select_user_key_tag_no_mysql is {}".format(value))
        return value


# 先把函数拿过来 ---- 在这里调试，避免改那边的diam
def Ngram_distance(str1, str2, n):
    tmp = ' ' * (n - 1)
    str1 = tmp + str1 + tmp
    str2 = tmp + str2 + tmp
    # set1 = set([str1[i:i + n] for i in range(len(str1) - (n - 1))])
    # set2 = set([str2[i:i + n] for i in range(len(str2) - (n - 1))])
    set1 = set(str1)
    set2 = set(str2)
    setx = set1 & set2
    len1 = len(set1)
    len2 = len(set2)
    lenx = len(setx)
    num_dist = len1 + len2 - 2 * lenx
    # num_dist = len1 + len2 - lenx
    num_sim = 1 - num_dist / (len1 + len2)
    return {'dist': num_dist, 'sim': num_sim}


if __name__ == "__main__":
    # 读取csv至字典
    file_abspath = os.path.abspath("imei_click.txt")
    print("file_abspath is: {}".format(file_abspath))

    csvFile = open(file_abspath, "r")
    reader = csv.reader(csvFile)
    redisBuffer = RedisMysqlCache()

    # 建立列表
    for item in reader:
        hot_word_tag = [x.strip('[').strip(']').strip("\"").strip(" ").strip("'") for x in item[2:]]
        user_key_tags = redisBuffer.select_user_key_tag_no_mysql("click_" + item[0])
        # user_key_tags = ['中源', '公告', '立案', '来源', '披露', '因涉嫌', '信息', '董事长', '违规', '接到', '违法', '调查', '财经', '股评', '标题']
        ret = Ngram_distance(str(hot_word_tag), str(user_key_tags), 1)
        all_info = {'hot_word_tag': hot_word_tag, 'user_key_tags': user_key_tags, 'Ngram_distance result': ret}
        print(all_info)
        # print("itme[3] keyword_tags is: {}".format(item[3]))

    csvFile.close()
