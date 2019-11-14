import csv

if __name__ == "__main__":
    # 读取csv至字典
    csvFile = open("iemi_hotword_tag.csv", "r")
    reader = csv.reader(csvFile)

    # 建立列表
    for item in reader:
        print(str(item))

        # print("itme[3] keyword_tags is: {}".format(item[3]))

    csvFile.close()
