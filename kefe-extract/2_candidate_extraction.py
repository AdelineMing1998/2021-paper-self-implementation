'''
时间：2021年03月30日
日志：复现KEFE中的候选词抽取步骤
步骤：利用NLTK工具进行
    1. 词切分
    2. POS
    3. 基于模式匹配的关键词抽取（模式并没有继续采用KEFE方法中的模式，而是沿用了SAFE中定义针对英文文本的模式）
'''

import nltk
from nltk.corpus import stopwords
from nltk.corpus import brown
import numpy as np
import json

pattern_list = [
    "NN,NN",
    "VB,NN",
    "JJ,NN",
    "NN,CC,NN",
    "JJ,NN,NN",
    "NN,NN,NN",
    "VB,PRP,NN",
    "VB,NN,NN",
    "VB,JJ,NN",
    "VB,VB,NN",
    "NN,IN,NN",
    "VB,DT,NN",
    "VB,NN,IN,NN",
    "JJ,NN,NN,NN",
    "JJ,CC,JJ",
    "VB,IN,JJ,NN",
    "VB,PRP,JJ,NN",
    "NN,CC,NN,NN",
]

def safe_method(text):
    # 分词
    # text = "Sentiment analysis is a challenging subject in machine learning.\
    # People express their emotions in language that is often obscured by sarcasm,\
    # ambiguity, and plays on words, all of which could be very misleading for \
    # both humans and computers."
    text = text.lower()
    text_list = nltk.word_tokenize(text)
    # 去掉标点符号
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '>', '<']
    text_list = [word for word in text_list if word not in english_punctuations]
    # 去掉停用词
    # stops = set(stopwords.words("english"))
    # text_list = [word for word in text_list if word not in stops]
    # 词性标注
    pos_list = nltk.pos_tag(text_list)
    # print(pos_list)
    # 标签提取
    tagging_list = []
    for tag in pos_list:
        tagging_list.append(tag[1])
    # print(tagging_list)
    # 词性还原
    pos_list_origin = []
    for pos in tagging_list:
        if str(pos).startswith("NN"):
            pos_list_origin.append("NN")
        elif str(pos).startswith("VB"):
            pos_list_origin.append("VB")
        elif str(pos).startswith("JJ"):
            pos_list_origin.append("JJ")
        elif str(pos).startswith("PRP"):
            pos_list_origin.append("PRP")
        elif str(pos).startswith("R"):
            pos_list_origin.append("R")
        else:
            pos_list_origin.append(str(pos))
    # print(pos_list_origin)
    # 将分词合并成一个字符串
    tagging_str = ",".join(pos_list_origin)
    # print(tagging_str)
    # 模式匹配
    fit_pattern_list = []
    for pattern in pattern_list:
        start = tagging_str.find(pattern)
        if start<0:
            pass
        else:
            fit_pattern_list.append(str(pattern))
            # print(pattern)
            # print(start)
    # print(fit_pattern_list)
    # 回溯索引
    index_list = []
    for fit_pattern in fit_pattern_list:
        # print(fit_pattern)
        # print(tagging_str.split(fit_pattern,2)[0])
        start_index = len((tagging_str.split(fit_pattern,2)[0]).split(",")) - 1
        end_index = start_index + len(fit_pattern.split(","))
        index = [start_index, end_index]
        index_list.append(index)
        # print(start_index, end_index)
    # 得到结果
    phrase_list = []
    for index in index_list:
        results = pos_list[index[0]: index[1]]
        phrase = ""
        for result in results:
            phrase = phrase + " " + str(result[0])
            # print(result[0])
        # print(phrase.strip())

        phrase_list.append({"phrase":phrase.strip(), "index": index})
    return phrase_list

def read_file(trainData_or_testData):
    file_path_list = []
    # for i in range(0, 10): file_path_list.append("train/preprocess_result/fold_" + str(i) + "_clean_train.json")
    for i in range(0, 10): file_path_list.append("test/preprocess_result/fold_" + str(i) + "_clean_dev.json")
    return file_path_list

def extraction_feature(file_path):
    print("[INFO] Start to extract file " + file_path)
    lines = open(file_path, encoding="utf-8").readlines()
    print("[FILE] The file has " + str(len(lines)) + " lines.")
    # write = open("train/candidate_feature/" + file_path.split("/")[2].split("_")[0] + "_" + file_path.split("/")[2].split("_")[1] + "_candidate_" + file_path.split("/")[2].split("_")[3], "w", encoding="utf-8")
    write = open("test/candidate_feature/" + file_path.split("/")[2].split("_")[0] + "_" + file_path.split("/")[2].split("_")[1] + "_candidate_" + file_path.split("/")[2].split("_")[3], "w", encoding="utf-8")
    for line in lines:
        line_array = line.strip().split("******", 2)
        if len(line_array) != 2: 
            print("[ERROR] Split error ")
        else:
            feature_list = []
            review = line_array[1].strip()
            extraction_dic_list = safe_method(review)
            for extraction_phrase_dic in extraction_dic_list: feature_list.append(extraction_phrase_dic["phrase"])
            write.write(json.dumps(feature_list) + "\n")
    write.close()
    print("[END] Finish write file " + file_path.split("/")[2].split("_")[0] + "_" + file_path.split("/")[2].split("_")[1] + "_candidate_" + file_path.split("/")[2].split("_")[3])


if __name__ == "__main__":
    # trainData_or_testData = "train" # 抽取训练集数据中的「特征候选短语」
    trainData_or_testData = "dev" # 抽取测试集数据中的「特征候选短语」
    file_path_list = read_file(trainData_or_testData)
    for file_path in file_path_list: extraction_feature(file_path)