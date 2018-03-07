# !/usr/bin/python
# -*-coding:utf-8-*-
import os
import codecs
import trainCRF as trainCRF


def character_to_word(input_file, output_file):  # 把标注结果改为分词结果
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        if line == "\n":
            output_data.write("\n")
        else:
            char_tag_pair = line.strip().split('\t')
            char = char_tag_pair[0]
            tag = char_tag_pair[2]
            if tag == 'B':
                output_data.write(' ' + char)
            elif tag == 'M':
                output_data.write(char)
            elif tag == 'E':
                output_data.write(char + ' ')
            else:
                output_data.write(' ' + char + ' ')
    input_data.close()
    output_data.close()

def character_split(input_file, output_file):  # 处理测试语料,单字成行 后面加B作为占位符
    with open(input_file,'r') as input_data:
        with open(output_file,'w') as output_data:
            for line in input_data.readlines():
                for word in line.strip():
                    word = word.strip()
                    if word:
                        output_data.write(word + "\tB\n")
                output_data.write("\n")


def cut_CRF(sentense, model='CRF_FILE/crf_model'):
    tmp_file = 'CRF_FILE/tmp'
    tmp_tagging_file =  'CRF_FILE/tmp_tagging_file'
    tmp_tagging_result_file = 'CRF_FILE/tmp_tagging_result_file'
    tmp_word_cut_result_file = 'CRF_FILE/tmp_word_cut.txt'
    model =  model
    with open(tmp_file, 'w') as f:
        f.write(sentense)
    character_split(tmp_file, tmp_tagging_file)
    cmd ="crf_test -m %s %s > %s" % (model, tmp_tagging_file, tmp_tagging_result_file)
    os.system(cmd)
    character_to_word(tmp_tagging_result_file, tmp_word_cut_result_file)
    with open(tmp_word_cut_result_file, 'r') as f:
        for line in f.readlines():
            for word in line.strip().split(" "):
                yield word

if __name__ == '__main__':
    for word in cut_CRF(u"张林昊在北京准备复试"):
        print(word)
