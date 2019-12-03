# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
import logging
import pandas as pd
import numpy as np
from collections import defaultdict


# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class TFSimilarities(object):
    def __init__(self):
        self.tfidf = None
        self.index = None
        self.dictionary = None
        self.keyword = None
        self.hot_keyword_tags = None

    def get_hot_keywords_corpus(self, hot_keyword_tags):
        # 创建字典（单词与编号之间的映射）
        keyword_tags_list = []
        for i in range(len(hot_keyword_tags)):
            temp = list(
                str(hot_keyword_tags[i]).replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(','))
            keyword_tags_list.append(temp)
        # todo 需要把dictionary变成全局的
        dictionary = corpora.Dictionary(keyword_tags_list)
        # 打印字典，key为单词，value为单词的编号
        # print(dictionary.token2id)

        # 建立语料库
        # 将每一篇文档转换为向量
        corpus = [dictionary.doc2bow(text) for text in keyword_tags_list]
        # print(corpus)
        # [[[(0, 1), (1, 1), (2, 1)], [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)], [(1, 1), (4, 1), (5, 1), (8, 1)], [(0, 1), (5, 2), (8, 1)], [(4, 1), (6, 1), (7, 1)], [(9, 1)], [(9, 1), (10, 1)], [(9, 1), (10, 1), (11, 1)], [(3, 1), (10, 1), (11, 1)]]

        # 初始化模型
        # 初始化一个tfidf模型,可以用它来转换向量（词袋整数计数）表示方法为新的表示方法（Tfidf 实数权重）
        tfidf = models.TfidfModel(corpus)
        # 测试
        test_doc_bow = [(0, 1), (1, 1)]
        print(tfidf[test_doc_bow])
        # [(0, 0.7071067811865476), (1, 0.7071067811865476)]

        # 将整个语料库转为tfidf表示方法
        corpus_tfidf = tfidf[corpus]
        # for doc in corpus_tfidf:
        # 	print(doc)

        # 创建索引
        index = similarities.MatrixSimilarity(corpus_tfidf)

        self.tfidf = tfidf
        self.index = index
        self.dictionary = dictionary

    def calculation_similarity(self, user_keyword, keyword, keyword_tags, recommend_number=12, threshold=0.1):
        # print(type(user_keyword))
        self.keyword = keyword
        self.hot_keyword_tags = keyword_tags

        if self.tfidf is None or self.index is None or self.dictionary is None:
            self.get_hot_keywords_corpus(keyword_tags)

        # 将要比较的文档转换为向量（词袋表示方法）
        # 要比较的文档
        # new_doc = "['苹果', '时间', '透露', '人士', '做好', '零售店', '知情', '便是', '上市', '发布', '发布会', '店员', '距离']"
        user_keyword = str(user_keyword).replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
        # print(user_keyword)

        # 将文档分词并使用doc2bow方法对每个不同单词的词频进行了统计，并将单词转换为其编号，然后以稀疏向量的形式返回结果
        new_vec = self.dictionary.doc2bow(user_keyword)
        # print(new_vec)
        # [[(0, 1), (2, 1)]

        # 8.相似度计算
        new_vec_tfidf = self.tfidf[new_vec]  # 将要比较文档转换为tfidf表示方法
        # print(new_vec_tfidf)
        # [(0, 0.7071067811865476), (2, 0.7071067811865476)]

        # 计算要比较的文档与语料库中每篇文档的相似度
        sims = self.index[new_vec_tfidf]
        # print(sims)
        # print(type(sims))
        # print(len(sims))
        # print('--------------------------')
        argsort_sims = sims.argsort()
        sims = np.sort(sims)
        # print(sims)
        # print('--------------------------')
        # print(argsort_sims)
        recommend_keywords = []
        total_size = len(sims)

        for i in range(recommend_number):
            if sims[total_size - i - 1] > threshold:
                recommend_keywords.append(self.keyword[argsort_sims[total_size - i - 1]])

        return recommend_keywords
        # [ 0.81649655  0.31412902  0.          0.34777319  0.          0.          0.
        #  0.          0.        ]
