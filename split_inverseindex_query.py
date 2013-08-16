# -*- coding:utf-8 -*-

from xml.dom import minidom
import os
import sys
import codecs
import jieba
import chardet
import math
#jieba.enable_parallel(4)

mydict = set() #词典几集合
idfdict = {} #idf对应的词典
alpha = 0.4 #增强因子 tf' = alpha + (1-alpha)*tf
inverindex = {} #倒排表
fileindex = {} #文件索引
allSegdict = {} #所有分词结果列表
totalFileNum = 0
myfile = [] #所有文件

PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*', '。', '、', '，',\
               '‘', '“', '”', '；', '：', '！', '？', '@', '#', '$', '%', '^', '&', '（', '）',\
               '【', '】','{', '}'] #去除标点符号

def readFile(filename = ''):
    try:
        f = open(filename)
        line = f.readline()
        con = ""
        while line:
            con = con + line
            line = f.readline()
        f.close()
        return con
    except Exception,e:
        print str(e)
        return ''
    
#对其中一个文件切词
def process(filename = ''):
    con = readFile(filename)
    if con == '':
        return
    global mydict
    global idfdict
    global alpha
    mydict1 = {}
    seg_list = list(jieba.cut(con, cut_all = False))
    print '/ '.join(jieba.cut(con, cut_all = False))
    print seg_list
    f = open('out.txt', 'w')
    #print len(seg_list)
    for o in seg_list:
        s = o.encode('utf-8')
        o = o.encode('gbk')
        if s not in PUNCTUATION:
            mydict.add(o) #加到词典
            mydict1.setdefault(o, 0)#该文档对应的词频集合
            mydict1[o] += 1
        f.write(o+'\n')
    f.close()
    mmax = 0
    for o in mydict1.keys():
        idfdict.setdefault(o, 0)
        inverindex.setdefault(o, set())
        idfdict[o] += 1 #逆文档频率
        inverindex[o].add(fileindex[filename])
        if mydict1[o] > mmax:
            mmax = mydict1[o]
    for o in mydict1.keys(): #归一化处理,增强准确率
        mydict1[o] = alpha + (1-alpha) * mydict1[o] / mmax
    return mydict1

#获取目录下所有文件
def getAllFile(dir = ''):
    global totalFileNum
    allFile = os.listdir(dir)
    totalFileNum = len(allFile)
    return allFile

def calidf(num):
    global totalFileNum
    return math.log(float(totalFileNum)/float(num))

def processFile(dir1 = ''):
    global fileindex
    global allSegdict
    global mydict
    global idfdict
    global myfile
    allFile = getAllFile(dir1)
    allFile = sorted(allFile)
    print allFile
    i = 0
    for fe in allFile:
        fe = dir1+'/'+fe
        fileindex[fe] = i
        myfile.append(fe)
        mydict1 = process(fe)
        allSegdict[i] = mydict1
        i += 1
    for key in allSegdict.keys():
        mydict1 = allSegdict[key]
        dict1 = {}
        for o in mydict:
            if o in mydict1.keys():
                #print o, '########## ', idfdict[o], '   ', mydict1[o], '  ',calidf(idfdict[o])
                dict1[o] = mydict1[o] * calidf(idfdict[o])
            else:
                dict1[o] = 0
        allSegdict[key] = dict1

def search(query): #query， 根据倒排索引进行
    global fileindex
    global myfile
    res = set()
    i = 0
    for o in query:
        o = o.encode('gbk')
        #print inverindex[o]
        if i == 0:
            res = inverindex[o]
        else:
            res = res & inverindex[o]
        i = i + 1
    mylist = []
    for o in res:
        mylist.append(myfile[o])
    return mylist
#con = process('user.xml')
#con = process('test.txt')
#print len(mydict)
#print len(con)
#print con
processFile('C:/Users/Topman3758/Desktop/mydir')
print totalFileNum
def printAll(mydict1):
    s = ""
    #print '!!!!!!!  ', len(mydict1)
    #print sum(mydict1.values)
    for key in mydict1.keys():
        va = mydict1[key]
        #key = key.encode('gbk')
        s = s + key + ': ' + str(va) + ' '
    print s
for i in range(totalFileNum):
    printAll(allSegdict[i])
    print len(allSegdict[i])
s = search([u'中华人民共和国', u'我们', u'名字'])
print s

