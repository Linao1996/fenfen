# !/usr/bin/python
# -*-coding:utf-8-*-

import pickle
import re

prob_start = open("./HMM_PARA/prob_start_6tag.p", "rb")
start_p = pickle.load(prob_start)

prob_emit = open("./HMM_PARA/prob_emit_6tag.p", "rb")
emit_p = pickle.load(prob_emit)

prob_trans = open("./HMM_PARA/prob_trans_6tag.p", "rb")
trans_p = pickle.load(prob_trans)

re_han = re.compile('([\u4E00-\u9FA5，。？：；（《 ‘’!"“”—……、]+)')  # 加了括号之后可以匹配本身

MIN_FLOAT = -3.14e100

pre_state = {
    'B': 'ES',
    'M': 'M2',
    'S': 'SE',
    'E': 'B12M',
    '1': 'B',
    '2': '1'
}


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = {}  # 二維数组 V[i,j] 代表時間t狀態爲j的最大概率
    pre = {}  # 二維數組pre[t,j] 代表時間t狀態爲j時的（前狀態）
    path = []
    for y in states:
        V[(0, y)] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
    for t in range(1, len(obs)):
        for y in states:
            em_p = emit_p[y].get(obs[t], MIN_FLOAT)
            (V[(t, y)], pre[(t, y)]) = max((V[(t - 1, y0)] + em_p + trans_p[y0][y], y0) for y0 in pre_state[y])

    (prob, state) = max([(V[len(obs) - 1, y], y) for y in 'ES'])
    path += state
    for t in range(len(obs) - 1, 0, -1):
        path += pre[t, path[-1]]
    # print(path[::-1])
    return (prob, path[::-1])


def cut_han(sentense):
    prob, pos_list = viterbi(sentense, 'B12MES', start_p, trans_p, emit_p)
    begin = 0
    for i, letter in enumerate(sentense, 0):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'S':
            yield letter
        elif pos == 'M' or pos == '1' or pos == '2':
            continue
        else:
            yield sentense[begin:i + 1]


def cut_HMM(sentence):
    blocks = re_han.split(sentence)
    for block in blocks:
        if not block:
            continue
        if re_han.match(block):
            for word in cut_han(block):
                yield word
        else:
            yield block

if __name__ == '__main__':
    text = "邓颖超生前使用过的物品" #验证人名学习能力
    for word in cut_HMM(text):
        print(word)

    with open("/home/lucas/Desktop/icwb2-data/testing/pku_test.utf8", "r") as f:#测试数据地址
        with open("/home/lucas/Desktop/result.txt", "w") as f2: #结果输出地址
            for line in f:
                for word in cut_HMM(line):
                    f2.write(word + "  ")



