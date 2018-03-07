import re

input_files_1 = ["icwb2-data/training/msr_training.utf8",
                 "icwb2-data/training/pku_training.utf8"]

input_files_2 = ["icwb2-data/renmin.txt","/home/lucas/Desktop/all.txt"]
input_files_3 = ["icwb2-data/baidu.txt"]

output_file = "dict2.txt"


def get_dict_1(input_files):  # 格式1 bakeoff
    res = {}
    for input_file in input_files:
        with open(input_file, "r") as f:
            for line in f.readlines():
                for word in line.strip().split():
                    if word in res:
                        res[word] += 1
                    else:
                        res[word] = 1

    return res


def get_dict_2(input_files):  # 格式2 renmin
    res = {}
    for input_file in input_files:
        with open(input_file, "r") as f:
            for line in f.readlines():
                for word in line.strip().split():
                    word = word.split('/')[0]
                    if word.find('199801') != -1:
                        continue
                    if word in res:
                        res[word] += 1
                    else:
                        res[word] = 1
    return res


def to_file(output_file):
    res1 = get_dict_1(input_files_1)
    res2 = get_dict_2(input_files_2)
    res = res1
    res.update(res2)
    res = sorted(res.items(),key = lambda x:x[1],reverse=True) #list
    with open(output_file,'w') as f:
        for key,value in res:
            f.write(key + " " + str(value) + "\n")


to_file(output_file)







# 如何按前缀排序词典
# 如何按前缀排序词典
