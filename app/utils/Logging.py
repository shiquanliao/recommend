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
        fmt = logging.Formatter('%(asctime)s, %(message)s', '%Y-%m-%d %H:%M:%S')
        # Use an absolute path to prevent file rotation trouble.
        logfile = os.path.abspath(path)
        # Rotate log after reaching 512K, keep 5 old copies.
        rh = ConcurrentRotatingFileHandler(logfile, "a", 5120 * 1024, backCount)
        # th = handlers.TimedRotatingFileHandler(filename=logfile, when=when, backupCount=backCount, encoding='utf-8')

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


if __name__ == '__main__':
    logyyx = Logger('./log/all.log', logging.ERROR, logging.DEBUG)
    index = 1.0
    while True:
        index = index + 1
        logyyx.debug('一个debug信息' + str(index))
        logyyx.info('一个info信息' + str(index))
        logyyx.war('一个warning信息' + str(index))
        logyyx.error('一个error信息' + str(index))
        logyyx.cri('一个致命critical信息' + str(index))
        time.sleep(0.005)
