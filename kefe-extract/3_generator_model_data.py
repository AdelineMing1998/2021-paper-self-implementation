'''
时间：2021-03-31
说明：将抽取出来的候选词与label标签进行对比，生成训练数据集以及测试数据集
'''
import json 
import difflib

def generate_dataset(candidate_file_path, label_file_path):
    candidate_file_lines = open(candidate_file_path, encoding="utf-8").readlines()
    label_file_lines = open(label_file_path, encoding="utf-8").readlines()
    print("[INFO] Start to manage file " + candidate_file_path.strip().split("/")[1])
    # write_file = open("train/bert_model_dataset/fold_" + candidate_file_path.strip().split("/")[2].split("_")[1] + "_tag.txt", "w", encoding="utf-8")
    # write_file = open("test/bert_model_dataset/fold_" + candidate_file_path.strip().split("/")[2].split("_")[1] + "_tag.txt", "w", encoding="utf-8")

    # write_file = open("train/candidate_tag_list/fold_" + candidate_file_path.strip().split("/")[2].split("_")[1] + "_tag.txt", "w", encoding="utf-8")
    # write_file = open("test/candidate_tag_list/fold_" + candidate_file_path.strip().split("/")[2].split("_")[1] + "_tag.txt", "w", encoding="utf-8")
    
    if len(candidate_file_lines) != len(label_file_lines): 
        print("[ERROR] File not match")
    else:
        index = len(candidate_file_lines)
        for i in range(0, index): 
            candidate_list = json.loads(candidate_file_lines[i])
            label_list = get_label_list_method(label_file_lines[i])
            tag_list = compare_candidate_feature(candidate_list, label_list)
            # 按行写入匹配文件，方便后续的复原
            write_file.write(str(candidate_list) + "\t" + str(tag_list) + "\n")
            # for j in range(0, len(tag_list)):
                # 写入所有文本
                # write_file.write(str(tag_list[j]) + "\t" + str(candidate_list[j]) + "\n")
                # write_file.write(str(candidate_list[j]) + "\t" + str(tag_list[j]) + "\n")
                # 只写入正文本
                # if tag_list[j] == 1:
                #     # write_file.write(str(tag_list[j]) + "\t" + str(candidate_list[j]) + "\n")
                #     write_file.write(str(candidate_list[j]) + "\t" + str(tag_list[j]) + "\n")
                # else:
                #     pass
    write_file.close()
    print("[END] Finish writing file " + str(write_file))


def get_label_list_method(one_line):
    line = json.loads(one_line)
    label = line["label"]
    label_list = []
    if len(label) != 0: 
        label_list = list(label["name"].keys())
    return label_list


def compare_candidate_feature(candidate_list, label_list):
    if len(candidate_list) == 0:
        return []
    elif len(label_list) == 0:
        return [0 * len(candidate_list)]
    else:
        tag_list = [0] * len(candidate_list)
        for i in range(0, len(candidate_list)):
            if if_match(candidate_list[i], label_list):
                tag_list[i] = 1
            else:
                tag_list[i] = 0
        return tag_list


def if_match(entity, manual_phrase):
    if len(manual_phrase) == 0 or len(entity) == 0:
        return False
    entity_word_list = entity.strip().split(" ")
    first_word_of_entity = entity_word_list[0]
    last_word_of_entity = entity_word_list[len(entity_word_list)-1]

    for label in manual_phrase:
        manual_word_list = label.strip().split(" ")
        first_word_of_manual = manual_word_list[0]
        last_word_of_manual = manual_word_list[len(manual_word_list)-1]
        if first_word_of_entity == first_word_of_manual or last_word_of_entity == last_word_of_manual:
            similar = difflib.SequenceMatcher(None, entity, label).quick_ratio()
            if similar >= 0.5:
                # print(entity + "++" + label)
                return True
    return False
   

def file_path_generator():
    candidate_dataset_file_list = []
    label_dataset_file_list = []
    for i in range(0, 10):
        # candidate_dataset_file_list.append("train/candidate_feature/fold_" + str(i) + "_candidate_train.json")
        # label_dataset_file_list.append("data/fold_" + str(i) + "/train.json")

        candidate_dataset_file_list.append("test/candidate_feature/fold_" + str(i) + "_candidate_dev.json")
        label_dataset_file_list.append("data/fold_" + str(i) + "/dev.json")
    return candidate_dataset_file_list, label_dataset_file_list

if __name__ == "__main__":
    candidate_dataset_file_list, label_dataset_file_list = file_path_generator()
    for i in range(0, 10): generate_dataset(candidate_dataset_file_list[i], label_dataset_file_list[i])