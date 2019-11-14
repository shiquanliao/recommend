import csv

if __name__ == "__main__":
    # 读取csv至字典
    csvFile = open("iemi_hotword_tag.csv", "r")
    reader = csv.reader(csvFile)

    # 建立空字典
    result = {}
    for item in reader:
        print(type(item))

    csvFile.close()
