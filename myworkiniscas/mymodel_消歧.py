#-*- coding:utf-8 -*-

import re
import string
import math

def readfile(filename = ''):
	f = open(filename, 'r')
	line = f.readline()
	topic_doc = {}
	docid = 0
	while line:
		line = line.strip().split(' ')
		mylist = []
		for i in range(len(line)):
			mylist.append((float(line[i]), i))
		for item in sorted(mylist, key = lambda x:x[0], reverse = True)[:1]:
			key = int(item[1])
			topic_doc.setdefault(key, [])
			topic_doc[key].append((docid, item[0]))
		docid += 1
		line = f.readline().rstrip()
	f.close()
	print docid
	return topic_doc

def readdocfile(filename = ''):
	f = open(filename, 'r')
	line = f.readline().rstrip()
	line = f.readline().rstrip()
	doc_word = []
	docid = 0
	while line:
		line = line.split(' ')
		worddict = {}
		for o in line:
			worddict.setdefault(o, 0)
			worddict[o] = 1
		doc_word.append(worddict)
		line = f.readline().rstrip()
	f.close()
	return doc_word

def readfeature(filename = ''):
	feature = {}
	f = open(filename, 'r')
	line = f.readline().rstrip()
	while line:
		feature.setdefault(line, 0)
		feature[line] = 1
		line = f.readline().rstrip()
	f.close()
	return feature


def readtopicword(filename = ''):
	f = open(filename, 'r')
	topic_word = {}
	line = f.readline().rstrip()
	index = -1
	while line:
		if re.match(r'^Topic', line):
			index += 1
			topic_word.setdefault(index, [])
			line = f.readline().rstrip()
			continue
		topic_word[index].append(line)
		line = f.readline().rstrip()
	f.close()
	return topic_word

# set label, topic:1：相关，-1：不相关
# label:(doc_label, +1 or -1)
def callabel(topic_doc, doc_word, feature):
	topic_label = []
	for key in topic_doc.keys():
		mydocset = topic_doc[key]
		doc_label = []
		docset = []
		for doc in mydocset:
			docid, pro = doc[0], doc[1]
			words = doc_word[docid].keys()
			num = 0
			for w in words:
				if feature.has_key(w):
					num += 1
			docset.append(num * pro)
		print docset
		maxele = max(docset)*1.0
		positive_num = 0
		neg_num = 0
		for obj in docset:
			if maxele == 0:
				neg_num += 1
				doc_label.append(-1)
				continue
			if maxele > 0.0:
				positive_num += 1
				doc_label.append(1)
			else:
				neg_num += 1
				doc_label.append(-1)
		if positive_num >= neg_num:
			topic_label.append((doc_label, 1))
		else:
			topic_label.append((doc_label, -1))
	return topic_label

def callabel_bootstrap(topic_doc, doc_word, topic_word, feature, simmatrix):
	topic_label = []
	wordset = topic_word.get(0)
	num = 0
	for word in wordset:
		flag = False
		for key in feature.keys():
			if string.find(key, word) != -1 or string.find(word, key) != -1:
				flag = True
				break
		if flag == True:
			num += 1
	if num >= 3:
		topic_label.append(1)
	else:
		topic_label.append(-1)
	topic_num = 100
	for i in range(1, topic_num):
		mydoc = [x[0] for x in topic_doc.get(i)]
		mylabel = 0
		for doc in mydoc:
			for topic_id in range(len(topic_label)):
				cur_doc = [x[0] for x in topic_doc.get(topic_id)]
				cur_label = topic_label[topic_id]
				mysum = 0.0
				for c_d in cur_doc:
					mysum += float(simmatrix[doc][c_d])/(len(doc_word[doc])*1.0*len(doc_word[c_d]))
				if mysum >= 0.15:
					mylabel += cur_label * 1
				else:
					mylabel += cur_label * -1
		if mylabel > 0:
			topic_label.append(1)
		else:
			topic_label.append(-1)
	return topic_label

def callabel_1(topic_word, feature):
	topic_label = []
	total = 0
	index = 0
	for key in topic_word.keys():
		wordset = topic_word[key]
		num = 0
		myset = set()
		for word in wordset:
			flag = False
			for key in feature.keys():
				if string.find(key, word) != -1 or string.find(word, key) != -1:
					flag = True
					break
			if flag == True:
				myset.add(word)
		num = len(myset)
		if num >= 2:
			topic_label.append(1)
			total += 1
		else:
			topic_label.append(-1)
		index += 1
	print total, ' 1111111111111111111111111'
	#fw = open('relate_file', 'w')
	return topic_label


def readnewdata(filename = ''):
	newdata = []
	f = open(filename,'r')
	line = f.readline().rstrip()
	while line:
		line = line.split(' ')
		newdata.append(line)
		line = f.readline().rstrip()
	f.close()
	return newdata

def calsim(doc1, doc2):
	num = 0
	for w in doc1:
		flag = False
		for w1 in doc2:
			if string.find(w, w1) != -1 or string.find(w1, w) != -1:
				flag = True;
				break
		if flag == True:
			num += 1
	return num

def calsim_1(doc1, doc2):
	mydict = {}
	for o in doc2:
		mydict.setdefault(o, 0)
		mydict[o] = 1
	num = 0
	for o in doc1:
		if mydict.has_key(o):
			num += 1
	return num

def readsim(filename = ''):
	f = open(filename)
	mysimmatrix = []
	line = f.readline().rstrip()
	while line:
		line = line.split('\t')[1]
		line = line.split(' ')
		cur = []
		for o in line:
			cur.append(float(o))
		mysimmatrix.append(cur)
		line = f.readline().rstrip()
	f.close()
	return mysimmatrix

def calsimmatrix(newdata, doc_word):
	sim = []
	for data in newdata:
		subsim = []
		for doc in doc_word:
			subsim.append(calsim(data, doc))
		sim.append(subsim)
	return sim

def sign(f):
	if f >= 0.5:
		return 1
	else:
		return 0
def prediction(newcont, topic_label, topic_doc, doc_word, sim_matrix):
	predict_result = []
	data_id = 0
	theta = 0.03
	for data in newcont:
		index = 0
		curlabel = 0
		for key in topic_doc.keys():
			label = topic_label[index]
			#print label
			if label is  -1:
				index += 1
				continue
			#print '###########'
			index += 1
			docset = topic_doc[key]
			sim = 0.0
			doc_id = 0
			t_num = 0
			len1 = len(newcont[data_id])
			#print len(docset)
			for doc in docset:
				docid, pro = int(doc[0]), float(doc[1])
				#print docid
				#print pro
				#sim += sim_matrix[data_id][doc_id]/math.log(len1*1.0*len(doc_word[doc_id]))#calsim(data, doc_word[docid]) * pro
				if(pro >= 0.01):
					sim += float(sim_matrix[docid][data_id]) * pro
					t_num += 1
				doc_id += 1
			sim = sim / (t_num*1.0)
			#print sim
			if sim >= theta:
				curlabel += 1 * int(label)
			else:
				curlabel += -1 * int(label)
		#if index == 2:
		#	break
		if curlabel >= 0:
			predict_result.append(1)
		else:
			predict_result.append(-1)
		data_id += 1
	return predict_result


def readdocsim(filename = ''):
	f = open(filename, 'r')
	simmatrix = []
	mylist = []
	line = f.readline().rstrip()
	while line:
		docid, doc = line.split('\t')
		docid = int(docid)
		doc = doc.split(' ')
		mylist.append((docid, doc))
		line = f.readline().rstrip()
	f.close()
	simmatrix = [x[1] for x in sorted(mylist, key = lambda y: y[0])]
	return simmatrix

#docsim = readdocsim('simmatrix')

#print docsim[0]
feature = readfeature('apple_feature')
topic_doc = readfile('model-final.theta')
doc_word = readdocfile('mydata_chinese')
topic_word = readtopicword('topicwords.txt')
topic_label = callabel_1(topic_word, feature)
newdata = readnewdata('testdoc_qiche_words.txt')
#sim_matrix = calsimmatrix(newdata, doc_word)
sim_matrix = readdocsim('newdata_qiche_matrix')


'''
topic_label_boostrap = callabel_bootstrap(topic_doc, doc_word, topic_word, feature, docsim)

num = 0
numid = 0
for i in topic_label_boostrap:
	if i == 1:
		num += 1
	else:
		print 'numid = ', numid
	numid += 1
print 'bootstrap = ', num
'''
print '######################'
num = 0
numid = 0
for i in topic_label:
	if i == 1:
		num += 1
	else:
		print 'numid = ', numid
	numid += 1
print 'comman = ', num

def getreleatefile(topic_doc, doc_word, topic_label):
	f = open('releate_file', 'w')
	doc_set = set()
	for tid, to in enumerate(topic_label):
		if int(to) is 1:
			mydoc = topic_doc[tid]
			for d in mydoc:
				doc_set.add(d[0])
	print len(doc_set), '@@@@@@@@@@@@@@@@222'
	for d in doc_set:
		mydict = doc_word[d]
		mystr = ''
		for key in mydict.keys():
			if mystr == '':
				mystr = key
			else:
				mystr += ' ' + key
		f.write(mystr +'\n')
	f.close()
print '----------------'
getreleatefile(topic_doc, doc_word, topic_label)
num = 0
mysum = 0
for i in range(100):
	if topic_doc.get(i) != None:
		num += 1
		print len(topic_doc[i])
		mysum += len(topic_doc[i])
print mysum
print num
print '---------------'
predict_result = prediction(newdata, topic_label, topic_doc, doc_word, sim_matrix)
num = 0
fw = open('result_qiche', 'w')
for o in predict_result:
	if o == 1:
		num += 1
	fw.write(str(o)+'\n')
fw.close()
print num
print len(predict_result)
print 'qiche', num*1.0/(len(predict_result)*1.0)
sum1 = num
sum2 = len(predict_result)

newdata = readnewdata('testdoc_other_words.txt')
sim_matrix = readdocsim('newdata_other_matrix')
predict_result = prediction(newdata, topic_label, topic_doc, doc_word, sim_matrix)
num = 0
fw = open('result_other', 'w')
for o in predict_result:
	if o == -1:
		num += 1
	fw.write(str(o)+'\n')
fw.close()
print num
print len(predict_result)
print 'other ', num*1.0/(len(predict_result)*1.0)
sum1 += num
sum2 += len(predict_result)

print 'total accuray = ', sum1*1.0/(sum2*1.0)

'''
topic_label = callabel(topic_doc, doc_word, feature)
num = 0
for obj in topic_label:
	if obj[1] == -1:
		num += 1
	print obj[1]
print num
'''
#callabel_1(topic_word, feature)
