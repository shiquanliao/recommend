#! /usr/bin/env python
# coding=utf-8
import logging, os
from cloghandler import ConcurrentRotatingFileHandler
from logging import handlers
import time


class Logger:
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG, when='M', backCount=5,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s | %(message)s', '%Y-%m-%d %H:%M:%S')
        # fmt = logging.Formatter('%(asctime)s | %(message)s')
        # Use an absolute path to prevent file rotation trouble.
        logfile = os.path.abspath(path)
        # Rotate log after reaching 512K, keep 5 old copies.
        rh = ConcurrentRotatingFileHandler(logfile, "a", 5120 * 1024, backCount)
        # th = handlers.TimedRotatingFileHandler(filename=logfile, when=when, backupCount=backCount, encoding='utf-8')
        rh.setFormatter(fmt)

        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path, encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        # self.logger.addHandler(fh)
        # self.logger.addHandler(th)
        self.logger.addHandler(rh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def collection(self, imei, unique_id, tag_algorithm, recommend_algorithm, hot_word_index, user_tag, similarity,
                   recommend_type):
        srt = imei + " | " + unique_id + " | " + tag_algorithm + " | " + recommend_algorithm + \
              " | " + hot_word_index + " | " + user_tag + " | " + similarity + " | " + recommend_type
        self.logger.info(srt)

# if __name__ == '__main__':
# logyyx = Logger('./log/all.log', logging.ERROR, logging.DEBUG)
# index = 1.0
# while True:
#     index = index + 1
#     imei = "----" + str(index) + "-----"
#     # 时间 | imei | 唯一id | 标签算法 | 推荐算法 | 热词列表索引 | 用户标签 | 相似度
#     data_str = imei + " | " + "---唯一id---" + " | " + "----标签算法----" + " | " + "---推荐算法----" + \
#                " | " + "----热词列表索引 ------" + " | " + "-----用户标签-----" + " | " + "-----相似度----"
#     logyyx.collection(imei, "--唯一id--", "--标签算法--", "--推荐算法--", "--热词列表索引--", "--用户标签--", "--相似度--")
#     time.sleep(0.005)
