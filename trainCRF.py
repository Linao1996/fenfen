import codecs
import sys
import os


def character_tagging(input_file, output_file):  # 得到CRF++要求的训练语料
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            if len(word) == 1:
                output_data.write(word + "\tS\n")
            else:
                output_data.write(word[0] + "\tB\n")
                for w in word[1:len(word) - 1]:
                    output_data.write(w + "\tM\n")
                output_data.write(word[len(word) - 1] + "\tE\n")
        output_data.write("\n")
    input_data.close()
    output_data.close()



if __name__ == '__main__':
    train_file = "icwb2-data/training/msr_training.utf8"
    train_tagging_file = "icwb2-data/training/msr_crf_training_tagging.utf8"
    template_path = "/home/lucas/Downloads/CRF++-0.58/example/seg/template"
    crf_model_file = 'CRF_FILE/crf_model'
    character_tagging(train_file, train_tagging_file)
    #训练很麻烦，执行下面的结果会覆盖原来结果，慎重！
    '''
    # os.system("crf_learn -f 3 -c 4.0 %s %s %s" % (template_path, train_tagging_file, crf_model_file))
    '''



    '''
    3.4 纯CRF msr测试数据
    === TOTAL TRUE WORDS RECALL:	0.833
    === TOTAL TEST WORDS PRECISION:	0.820
    === F MEASURE:	0.827
    
    '''
