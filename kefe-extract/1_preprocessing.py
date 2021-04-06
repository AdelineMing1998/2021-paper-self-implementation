'''
时间：2021年03月30日
日志：复现KEFE方法中对于数据与处理的部分
步骤：去除噪声值，包括
    · 非英文数据
    · emoji
    · 特殊符号
    · 特殊数字
'''
import re
import json

app_dictionary = {
    "yahoo-mail": 100001, "gmail": 100002,
    "instagram": 100003, "snapchat": 100004,
    "com.chase.sig.android": 100005, "com.bpi.ng.mobilebanking": 100006,
}

def remove_serial_number(text):
    text = re.sub(r'[^a-zA-Z0-9,.\!?]+', ' ', text)
    text = re.sub(r'[●,=√#￥%&,[]【】◆ ★◎☆⊙]', ' ', text)
    return text

def remove_exce_punc(text):
    duels = [x + x for x in list('。，,=！!-—#')]
    # print(duels)
    for d in duels:
      while d in text:
        text = text.replace(d, d[0])
    return text

def pre_process(file_path):
    print("[INFO] Start to manage: " + file_path)
    lines = open(file_path, encoding="utf-8").readlines()
    print("[FILE] The file has " + str(len(lines)) + " lines.")
    # write_file = open("train/preprocess_result/" + file_path.strip().split("/")[8]+ "_clean_" + file_path.strip().split("/")[9], "w", encoding="utf-8")
    write_file = open("test/preprocess_result/" + file_path.strip().split("/")[8]+ "_clean_" + file_path.strip().split("/")[9], "w", encoding="utf-8")
    id_list = []
    for line in lines:
        line = json.loads(line)
        id = line["id"]
        id_list.append(id)
        text = line["text"].strip()
        # 除去文本之中的噪声项
        text = remove_serial_number(str(text))
        text_remove_noisy = remove_exce_punc(text)
        write_file.write(str(id) + "******" + text_remove_noisy + "\n")
    write_file.close()
    print("[END] Finish writing file " + "preprocess_result/" + file_path.strip().split("/")[8]+ "_clean_data.json")


def read_file(trainData_or_testData):
    file_path_list = []
    for i in range(0, 10): file_path_list.append("data/fold_"+ str(i) + "/" + str(trainData_or_testData) + ".json")
    return file_path_list

if __name__ == "__main__":
    # trainData_or_testData = "train" # 预处理训练集数据中的「特征候选短语」
    trainData_or_testData = "dev" # 预处理测试集数据中的「特征候选短语」
    file_path_list = read_file(trainData_or_testData)
    for one_file_path in file_path_list: pre_process(one_file_path)