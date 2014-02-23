# -*- coding:utf-8 -*-

import re
indextoword = []
def getindex_word(filename = ''):
    f = open(filename, 'r')
    line = f.readline().rstrip()
    while line:
        indextoword.append(line)
        line = f.readline().rstrip()
    f.close()

def getindex(filename = '', length=0):
    global indextoword
    f = open(filename, 'r')
    wf = open('topic_result_apple.txt', 'w')
    line = f.readline().rstrip()
    while line:
        wf.write(line+'\n')
        for i in range(length):
            line = f.readline().strip()
            mylist = line.split(' ')
			
            my = []
            for o in mylist:
                if o != '':
                    my.append(o)
            wordid, fre = int(my[0]), my[1]
            word = indextoword[wordid]
            wf.write('\t'+word+'\t'+fre+'\n')
        line = f.readline().strip()
    f.close()
    wf.close()
    
def getindex_lda(filename = '', length=0):
    global indextoword
    f = open(filename, 'r')
    wf = open('lda_outputdata', 'w')
    line = f.readline()
    while line:
        #print line
        if line.strip() == 'Background' or re.match(r'^Topic', line.strip()):
            wf.write(line.rstrip()+'\n')
            line = f.readline()
            continue
        elif line == '\n':
            line = f.readline()
        else:
            line = line.strip()
            wf.write(indextoword[int(line)]+'\n')
            line = f.readline()
    f.close()
    wf.close()

def getindex_ccda(filename = '', length=0):
    global indextoword
    f = open(filename, 'r')
    wf = open('ccda_outputdata', 'w')
    line = f.readline().rstrip()
    while line:
        #print line
        if re.match(r'^-', line) or re.match(r'^Topic', line):
            wf.write(line+'\n')
            line = f.readline().rstrip()
            continue
        elif line == '':
            line = f.readline().rstrip()
        else:
            wf.write(indextoword[int(line)]+'\n')
            line = f.readline().rstrip()
    f.close()
    wf.close()

def getindex_tam(filename = '', length=0):
    global indextoword
    f = open(filename, 'r')
    wf = open('tam_outputdata', 'w')
    line = f.readline()
    while line:
        #print line
        if re.match(r'Background', line) or re.match(r'^Aspect', line.strip()) \
           or re.match(r'^Topic', line):
            wf.write(line.strip() + '\n')
            line = f.readline()
            continue
        elif line == '\n':
            line = f.readline()
        else:
            line = line.strip()
            wf.write(indextoword[int(line)]+'\n')
            line = f.readline()
    f.close()
    wf.close()
getindex_word('index_word_apple.txt')
#getindex_ccda('cclda_output_topwords')
#getindex_tam('tam_output_topwords')
#getindex_lda('lda_output_topwords', 20)
getindex('model-final.twords', 30)
