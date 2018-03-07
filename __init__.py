# !/usr/bin/python
# -*-coding:utf-8-*-

import re
from math import log
from trie import Trie
import HMM
import sys
import CRF

freq = {}
trie = Trie()
freq_total = 0
re_han = re.compile('([\u4E00-\u9FA5，。？：；（《 ‘’!"“”—……、]+)')  # 加了括号之后可以匹配本身

'''
based on dictionary,calculating the max probability of all possible combinations of word cut
'''


def get_trie(dict_path):
    global freq_total
    with open(dict_path, 'r') as f:  # 打开文件 dict.txt
        for line in f:  # 行号,行 指定从1开始
            word = line.split(" ")[0]
            freq = line.split(" ")[1]
            freq = int(freq)
            trie.add(word, freq)  # 词典的排序方式是无所谓的，即使北京大学出现在北京之前，将北京词频置为0后，再次扫描到北京会将其词频重新改为正确的数值
            freq_total += freq


def get_prob(sentence, DAG, prob_route):  # 动态规划,获取最大概率路径
    global freq_total
    lenth = len(sentence)
    prob_route[lenth] = (0, 0)
    log_freq_total = log(freq_total)
    for idx in range(lenth - 1, -1, -1):
        prob_route[idx] = (
            log(trie.get_freq(sentence[idx:idx + 1]) or 1) - log_freq_total + prob_route[idx + 1][0], idx)
        for x in DAG[idx]:
            prob_route[idx] = max((prob_route[idx][0], prob_route[idx][1]),
                                  (log(trie.get_freq(sentence[idx:x + 1]) or 1) - log_freq_total +
                                   prob_route[x + 1][0], x))


def get_DAG(sentence):
    global trie
    DAG = {}
    N = len(sentence)
    for i in range(N):
        tmplist = []
        j = i
        subword = sentence[j]
        while j < N:
            if trie.get_freq(subword) != 0:
                tmplist.append(j)
            j += 1
            subword = sentence[i:j + 1]
        if len(tmplist) == 0:
            tmplist.append(i)
        DAG[i] = tmplist
    return DAG


def cut_DAG(sentence):
    DAG = get_DAG(sentence)
    prob_route = {}
    get_prob(sentence, DAG, prob_route)  # route 是以idx:(概率对数最大值，词语末字位置)键值对形式保存的字典。
    x = 0
    N = len(sentence)
    while x < N:  # 从头开始
        y = prob_route[x][1] + 1  # route[x][1]对应的位置i能够使得x...i出现的概率最大化
        l_word = sentence[x:y]
        yield l_word
        x = y


def cut_sentense(sentence):
    blocks = re_han.split(sentence)
    for block in blocks:
        if not block:
            continue
        if re_han.match(block):
            for word in cut_DAG(block):
                yield word


def get_score(test_file, output_file, mode='quick'):
    with open(test_file, "r") as f:
        with open(output_file, "w") as f2:
            for line in f:
                if mode == 'quick':
                    for word in cut_sentense(line):
                        f2.write(word + "  ")
                if mode == 'HMM':
                    for word in HMM.cut_HMM(line):
                        f2.write(word + " ")
                if mode == 'CRF':
                    for word in CRF.cut_CRF(line):
                        f2.write(word + " ")


if __name__ == '__main__':
    get_trie("dict.txt")
    # for word in cut_sentense("张林昊在北京吃火锅"):
    #     print(word)
    # if len(sys.argv) != 3:
    #     print("usage: .py -mode text")
    # elif sys.argv[1] == '-name':
    #     HMM.cut_HMM(sys.argv[2])
    # elif sys.argv[1] == '-fast':
    #     cut_sentense(sys.argv[2])
    # else:
    #     print("unknown mode")

    test_file = "/home/lucas/Desktop/icwb2-data/testing/pku_test.utf8"
    output_file = "/home/lucas/Desktop/result.txt"
    get_score(test_file, output_file,'CRF')
