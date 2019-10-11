import pandas as pd


def Ngram_distance(str1, str2, n=2):
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
    # num_dist = len1 + len2 - 2 * lenx
    num_dist = len1 + len2 - lenx
    num_sim = 1 - num_dist / (len1 + len2)
    return {'dist': num_dist, 'sim': num_sim}


def find_user_similarity_keywords(user_key_tags_buffer,
                                  hot_key_tags_buffer,
                                  imei,
                                  news_type,
                                  news_source,
                                  similarity_keywords_num,
                                  similarity_keywords_min):
    """
    :param user_key_tags_buffer:
    :param hot_key_tags_buffer:
    :param imei:
    :param news_type:
    :param news_source:
    :param similarity_keywords_num:
    :param similarity_keywords_min:
    :return:
    """

    hot_keywords = list(hot_key_tags_buffer.keys())
    # print("hot_keywords is {}".format(hot_keywords))
    # print(type(hot_keywords))

    hot_keywords_tags = list(hot_key_tags_buffer.values())
    # print("hot_keywords_and_tags is {}".format(hot_keywords_tags))
    # hot_keywords.index = range(200)  # 200
    # hot_keywords_tags.index = range(200)  # 200
    # hot_keywords_tags.to_csv(r'/data/test_2.csv')

    # print(user_key_tags_buffer)

    # xiaoshuaiwujieguo
    if (user_key_tags_buffer is None) | (len(hot_keywords_tags) == 0):
        return -1
    user_keywords = {}
    distance = []
    order_number = []
    result = []

    # print(hot_keywords_tags.shape())
    # hot_keyword_tags = hot_keyword_tags.reset_index(drop=True)
    for j in range(len(hot_keywords)):
        # print(hot_keywords_tags[j])
        if (hot_keywords_tags[j] is not None) & (user_key_tags_buffer.values() is not None):
            # print(hot_keywords_tags[j])
            # print(user_key_tags_buffer)
            ngram_distance = Ngram_distance(hot_keywords_tags[j], str(user_key_tags_buffer.values()), 2)
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
    keywords = {"imei": imei,
                "hotwords": keyword2
                }

    # elapsed = (time.clock() - start)
    # print("Time used:", elapsed)

    return keywords
