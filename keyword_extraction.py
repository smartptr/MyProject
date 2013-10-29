/*思路：
1.分词，词性标注，去除停用词，保留名词和动词
2.title， 摘要， 正文：区域分数制定
3.词的元组(词频， pos(所在区域))
alpha*词频因子(f/(1+f))+beta*pos因子(迭代)
4.权重值排序
*/

# -*- coding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import codecs
import numpy as np
import math

alpha = 2 #weight factor
maxIterator = 500 #max iterator times

#the score of the different pos in the text
TITLE = 10
ABSTRACT = 6
CONTENT = 1

posTag = ['ns', 'v', 'a', 'n', 'vn', 'l', 'nr']
stopwords = []
# get all the stop words
def stopWords(filename = ''):
    global stopwords
    stop = set()
    f = open(filename, 'r')
    line = f.readline().rstrip()
    while line:
        stop.add(line)
        line = f.readline().rstrip()
    f.close()
    stopwords = list(stop)

def getContent(filename = ''):
    content = ''
    f = open(filename, 'r')
    line = f.readline().rstrip()
    title = line
    print line
    while line:
        content = content + line
        line = f.readline().rstrip()
    return title, content

# word segment
def splitword(content):
    global stopwords
    global posTag
    mywords = {}
    words = pseg.cut(content)
    #print type(stopwords[0])
    for w in words:
        key = w.word.encode('utf-8')
        if (key not in stopwords) and (w.flag in posTag) and (len(w.word) > 1):
            #rint key, w.flag, len(key)
            mywords.setdefault(key, 0)
            mywords[key] += 1
    return mywords

# the factor of the frequence
def getF(f):
    return float(f)/float(f+1)

# the process iterator
#1. x0 = transpose(x0(1),x0(2)...x0(n)), m0 = max{x0(i)|1<=i<=n}, y0 = x0/m0
#2. x(k+1) = A*yk, m(k+1) = max{x(k+1)(i)|1<=i<=n}, y(k+1) = x(k+1)/m(k+1)
#3. if |m(k+1)-m(k)|<theta, goto setp 4, else k = k + 1, goto step 1
#4. w = y(k+1)/sum{y(k+1)(i), 1<=i<=n}, 特征值是m(k+1)
def process(numFeatures, word2matrix):
    global maxIterator
    init_Vector = np.random.rand(1, numFeatures)#np.ones((1, numFeatures))
    #print init_Vector
    mylist = list(init_Vector[0])
    m0 = max(mylist)
    y_vector = init_Vector / m0
    theat = 1e-10
    times = 0
    #print maxIterator
    while times <= maxIterator:
        #print times, '!!!'
        times += 1
        vector_k = np.transpose(np.dot(word2matrix, np.transpose(y_vector)))
        mylist = list(vector_k[0])
        mk = max(mylist)
        y_vector = vector_k / mk
        #if math.fabs(mk-m0) < theat:
        #   break
        m0 = mk
    mylist = list(y_vector[0])
    total_sum = sum(mylist)
    y_vector = y_vector / total_sum
    return mk, list(y_vector[0])

# get the domin of each word
def getScore(title, abstract, mydict):
    mydict1 = {} #mydict1:{word, pos(title, abstract, content)}
    for key in mydict.keys():
        mydict1.setdefault(key, 1)
        if title.find(key) != -1:
            mydict1[key] = TITLE
        elif abstract.find(key) != -1:
            mydict1[key] = ABSTRACT
    return mydict1

# get the related score between words
def get_word2matrix(mydict1, mydict):
    word2word = []
    mysum = sum(mydict1.values())
    for key in mydict1.keys():
        word = []
        score = mydict1[key]
        times = mydict[key]
        for key1 in mydict1.keys():
            bili = float(score)/float(mydict1[key1])
            times_bili = float(times)/float(mysum) #float(mydict2[key1])
            word.append(bili*(-1*math.log(times_bili)))
        word2word.append(word)
    word2matrix = np.array(word2word)
    return word2matrix

# the final score accouting for frequence and positon
def getFinalScore(mydict, y_list):
    index = 0
    for key in mydict.keys():
        score = getF(mydict[key]) * alpha + y_list[index] # a*f/(1+f) + loc
        index += 1
        mydict[key] = score
    return mydict

def solve_problem(filename = ''):
    stopWords('mystropwords.txt')
    jieba.load_userdict('dict.txt')
    #print len(stopwords)
    title, mycon = getContent(filename)
    mydict = splitword(mycon) #mydict:{word, times}
    #print len(mydict)
    s = '摘要'
    e = '关键'
    s = s.decode('utf-8').encode('gbk')
    e = e.decode('utf-8').encode('gbk')
    #print s, e
    #print mycon, type(mycon)
    startindex = mycon.find(s)
    endindex = mycon.find(e)
    abstract = ''
    if startindex != -1 and endindex != -1:
        abstract = mycon[startindex:endindex];
    #print title
    #print abstract
    mydict1= getScore(title, abstract, mydict)
    #print '&&&&&&&&&&777'
    #for key in mydict1.keys():
    #    print key.decode('utf-8'), mydict1[key]
    word2matrix = get_word2matrix(mydict1, mydict)
    dim = len(mydict1)
    #print 'dim: ', dim
    mk, y_list = process(dim, word2matrix)
    #print mk, '11'
    #print y_list, '11'
    mydict = getFinalScore(mydict, y_list)
    mykey = mydict.keys()
    for i in range(len(mykey)):
        for j in range(len(mykey)):
            if i == j:
                continue
            else:
                if mykey[i].find(mykey[j]) != -1:
                    if mykey[j] in mydict.keys():
                        mydict.pop(mykey[j])   
    for key in [a[0] for a in sorted(mydict.items(), key = lambda x:x[1], reverse = True)][:6]:
        print key.decode('utf-8').encode('gbk')
    
def main():
    solve_problem('con1.txt')
    print '\n\n'
    solve_problem('con2.txt')
    print '\n\n'
    solve_problem('con3.txt')
    print '\n\n'

if __name__ == '__main__':
    main()
        
