# -*- coding:utf-8 -*-

import jieba
import re
import jieba.posseg as pseg
import codecs

PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*', '。', '、', '，',\
               '‘', '“', '”', '；', '：', '！', '？', '@', '#', '$', '%', '^', '&', '（', '）',\
               '【', '】','{', '}', '...', '…', '—', '←', '·', '•', '％', '～', '＂', '▲'] #去除标点符号
stopwords = {}

def stroword(filename = ''):
    global stopwords
    f = open(filename, 'r')
    line = f.readline().rstrip()
    while line:
        stopwords.setdefault(line, 0)
        stopwords[line] = 1
        line = f.readline().rstrip()
    f.close()


def process(filename = ''):
    global stopwords
    f = open(filename, 'r')
    line = f.readline().rstrip()
    #mywords = {}
    #mywordindex = {}
    index = 0
    content = []

    while line:
        words = pseg.cut(line)
        con1 = []
        for w in words:
            key = w.word.encode('utf-8')
            if (not re.match(r'^[0-9]+', key)) and len(key) > 1 and \
				(key not in PUNCTUATION) and (stopwords.get(key) == None) \
				and (not re.match(r'\.', key)) and key != 'quot' \
				and key != 'hao123' and (not re.match(r'#', key)):
					con1.append(key)
					#mywords.setdefault(key, 0)
					#mywords[key] += 1
        content.append(con1)
        line = f.readline().rstrip()
    f.close()
    #indextoword = []
    '''
	for key in mywords.keys():
        mywordindex.setdefault(key, -1)
        mywordindex[key] = index
        indextoword.append(key)
        index += 1
	'''
    return mywords, mywordindex, content, indextoword


stroword('stopwords.txt')
jieba.load_userdict('dict')
words, myindex, content, indextoword = process('train_input_data.txt')
print len(words)
print len(myindex)
print len(content)

'''
f = open('word.txt', 'w')
for o in content:
    f.write(o)
f.write('\n')
f.close()
'''

#f = open('inputdata.txt', 'w')
f = open('index_word_apple.txt', 'w')
for o in indextoword:
    f.write(o+'\n')
f.close()

f = open('mydata_apple.txt', 'w')
num = 0
for o in content:
	if len(o) != 0:
		num = num + 1
f.write(str(num)+'\n')
for o in content:
    mystr = ''
    if len(o) == 0:
        continue
    for i in range(len(o)):
        if i == 0:
            mystr = str(myindex[o[i]])
        else:
            mystr = mystr + ' ' + str(myindex[o[i]])
    mystr = mystr + '\n'
    f.write(mystr)
f.close()
print 'end'




