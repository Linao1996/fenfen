import codecs
import sys
import re
import pickle
from math import log

MIN = -3.14e100


def character_tagging(input_file, output_file):  # 格式2：remin
    with open(output_file, 'w') as output:
        with open(input_file, 'r') as f:
            for line in f.readlines():
                for word in line.strip().split():
                    if word.find("199801") != -1:  # for renmin
                        continue
                    word = word.split('/')[0]
                    if len(word) == 0:
                        continue
                    elif len(word) == 1:
                        output.write('/S' + word)
                    elif len(word) == 2:
                        output.write('/B' + word[0])
                        output.write('/E' + word[1])
                    elif len(word) == 3:
                        output.write('/B' + word[0])
                        output.write('/1' + word[1])
                        output.write('/E' + word[2])
                    elif len(word) == 4:
                        output.write('/B' + word[0])
                        output.write('/1' + word[1])
                        output.write('/2' + word[2])
                        output.write('/E' + word[3])
                    else:
                        output.write('/B' + word[0])
                        output.write('/1' + word[1])
                        output.write('/2' + word[2])
                        for w in word[3:len(word) - 1]:
                            output.write('/M' + w)
                        output.write('/E' + word[-1])
                output.write("\n")





def get_start(input_file):
    start_p = {}
    start_p['E'] = MIN
    start_p['M'] = MIN
    start_p['1'] = MIN
    start_p['2'] = MIN
    lineNum = 0
    BNum = 0
    SNum = 0
    with open(input_file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0: continue
            lineNum += 1
            if line[1] == 'S':
                SNum += 1
            elif line[1] == 'B':
                BNum += 1
    start_p['S'] = log(SNum / lineNum)
    start_p['B'] = log(BNum / lineNum)
    return start_p


def get_trans(input_file):
    trans_p = {}
    freq = {}
    with open(input_file, "r") as f:
        pre = 0
        for line in f.readlines():
            for word in line.strip().split('/'):
                if len(word) != 0 and word[0] in 'B12MES':
                    state = word[0]
                    word = word[1]
                    if state in freq:
                        freq[state] += 1
                    else:
                        freq[state] = 1
                    if pre != 0 and pre in trans_p:
                        if state in trans_p[pre]:
                            trans_p[pre][state] += 1
                        else:
                            trans_p[pre][state] = 1
                    elif pre != 0:
                        trans_p[pre] = {}
                        trans_p[pre][state] = 1
                    pre = state
                    # print(pre)
        for pre in trans_p:
            for now in trans_p[pre]:
                trans_p[pre][now] = log(trans_p[pre][now] / freq[pre])
    return trans_p  # input_files = ["/home/lucas/Desktop/icwb2-data/training/pku_training_tagging.utf8",


def get_emit(input_file):
    freq = {}
    emit_p = {}
    for char in '12BMES':
        freq[char] = 0
        emit_p[char] = {}
    with open(input_file, 'r') as f:
        for line in f.readlines():
            for word in line.split('/'):
                if len(word) == 2:
                    freq[word[0]] += 1
                    if word[1] in emit_p[word[0]]:
                        emit_p[word[0]][word[1]] += 1
                    else:
                        emit_p[word[0]][word[1]] = 1

    for state in emit_p:
        for word in emit_p[state]:
            emit_p[state][word] = log(emit_p[state][word] / freq[state])
    return emit_p


input_file = "icwb2-data/renmin.txt"
tagging_file = "icwb2-data/renmin_tagging.txt"
character_tagging(input_file,tagging_file)

start_p = get_start(tagging_file)
trans_p = get_trans(tagging_file)
emit_p = get_emit(tagging_file)

# start.p:jieba
# start2.p:all.txt
# start3.p:renmin.txt
# start4.p:bakefoff
#

print(trans_p)
with open('HMM_PARA/prob_start_6tag.p', 'wb') as f:
    pickle.dump(start_p, f)
with open('HMM_PARA/prob_trans_6tag.p', 'wb') as f:
    pickle.dump(trans_p, f)
with open('HMM_PARA/prob_emit_6tag.p', 'wb') as f:
    pickle.dump(emit_p, f)
    #
