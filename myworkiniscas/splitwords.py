# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import re
import math

PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*', '。', '、', '，',\
				'‘', '“', '”', '；', '：', '！', '？', '@', '#', '$', '%', '^', '&', '（', '）',\
				'【', '】','{', '}', '...', '…', '—', '←', '·', '•', '％', '～', '＂', '▲'] #去除标点符号

def getstopwords(filename = ''):
	stopwords = {}
	f = open(filename, 'r')
	line = f.readline().rstrip()
	while line:
		stopwords.setdefault(line, 0)
		stopwords[line] = 1
		line = f.readline().rstrip()
	f.close()
	return stopwords


def readfile(filename = ''):
	f = open(filename, 'r')
	line = f.readline().rstrip()
	content = []
	while line:
		line = line.split('\3')[3]
		content.append(line)
		line = f.readline().rstrip()
	f.close()
	return content

def getfeature(content, stopwords):
	doc_word = []
	for con in content:
		words = pseg.cut(con)
		con1 = []
		for w in words:
			key = w.word.encode('utf-8').strip()
			if (not re.match(r'^[0-9]+', key)) and len(key) > 1 and \
				(key not in PUNCTUATION) and (stopwords.get(key) == None) \
				and (not re.match(r'\.', key)) and key != 'quot' and key != 'hao123' \
				and (not re.match(r'#', key)):
				con1.append(key)
		doc_word.append(con1)
	return doc_word

stopwords = getstopwords('stopwords.txt')
content = readfile('test_not_qiche.txt')
jieba.load_userdict('dict')
doc_word = getfeature(content, stopwords)
print len(doc_word)
fw = open('testdoc_other_words.txt', 'w')
for o in doc_word:
	mystr = ''
	for w in o:
		if mystr == '':
			mystr = w
		else:
			mystr += ' ' + w
	fw.write(mystr+'\n')
fw.close()

