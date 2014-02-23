# -*- coding: utf-8 -*-

import math

def readfile(filename = ''):
	f = open(filename, 'r')
	topic_words = []
	line = f.readline().rstrip()
	while line:
		line = map(float, line.split(' '))
		topic_words.append(line)
		line = f.readline().rstrip()
	f.close()
	return topic_words

def addvalue(x, y):
	if y != 0:
		return x * math.log(x / y)
	else:
		return 0

def add(x, y):
	return x + y

def calKL(p,q):
	mylist = map(addvalue, p, q)
	return reduce(add, mylist)

def calallKL(index, topic_words):
	p = topic_words[index]
	res = []
	for i in range(len(topic_words)):
		q = topic_words[i]
		res.append((i, calKL(p, q)))
	return sorted(res, key = lambda x:x[1])

topic_words = readfile('model-final.phi')
res = calallKL(5, topic_words)
for i in range(min(len(res),10)):
	print "%d: %.4f" % (res[i][0], res[i][1])


