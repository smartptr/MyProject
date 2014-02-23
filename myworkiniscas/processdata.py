# -*- coding:utf-8 -*-
import re

def get1(id1, id2, id3):
    if id2 == -1 and id3 == -1:
        return id1
    elif id2 != -1:
        if id1 < id2:
            return id1
        else:
            return id2
    elif id3 != -1:
        if id1 < id3:
            return id3
        else:
            return id1

def getindex(id1, id2, id3):
    if id1 == -1 and id2 == -1 and id3 == -1:
        return -1
    elif id1 != -1:
        return get1(id1, id2, id3)
    elif id2 != -1:
        return get1(id2, id1, id3)
    elif id3 != -1:
        return get1(id3, id1, id2)
          
def processdata(filename = ''):
    data = []
    f = open(filename, 'r')
    line = f.readline().rstrip()
    line = f.readline().rstrip()
    while line:
        #mylist = line.split('\3')
        mydata = line.strip()
        #mytime = mylist[-1]
        line = f.readline().rstrip()
        mydata = mydata
        index = mydata.find('http')
        if index != -1:
            mydata = mydata[0:index]
        index = mydata.find('\/\/')
        if index != -1:
            mydata = mydata[0:index]
        index = mydata.rfind('@')
        if index != -1:
            mydata = mydata[index:len(mydata)]
        index = mydata.find(' ')
        index1 = mydata.find(':')
        index2 = mydata.find('，')
        id1 = getindex(index, index1, index2)
        if id1 != -1:
            if id1 == index:
                id1 = id1 + len(' ')
            if id1 == index1:
                id1 = id1 + len(':')
            if id1 == index2:
                id1 = id1 + len('，')
            mydata = mydata[id1:len(mydata)]
        mydata = mydata.strip()
        if len(mydata) < 60:
            #or re.match(r'^@', mydata):
            continue
        #if re.match(r'^\/\/', mydata):
            #print mydata
            #continue
        #if re.match(r'回复', mydata):

            #print mydata
            #continue
        #if re.match(r'^说：', mydata):
        #    mydata = mydata[len('说：')+1:]
        mydata.rstrip()
        while re.match(r'^，', mydata):
            mydata = mydata[len('，'):len(mydata)]
        if re.match(r'^）', mydata):
            mydata = mydata[len('）'):]
        if re.match(r'^！', mydata):
            mydata = mydata[len('！'):]
        if re.match(r'^： ', mydata):
            mydata = mydata[len('： '):]
        if re.match(r'^；', mydata):
            mydata = mydata[len('；'):]
        if re.match(r'^：', mydata):
            mydata = mydata[len('：'):]
        index = mydata.find('//')
        if index != -1:
            mydata = mydata[0:index]
        mydata = mydata.rstrip()
        data.append(mydata)
    f.close()
    return data
'''
filepath1 = u'C:\\Users\\Topman3758\\Desktop\\ntt\\ntt_data\\ntt_data\\ntt\\奔驰 E\\微博.txt'
data = processdata(filepath1)
data.sort()
'''
mydata = []
'''
mydata.append(data[0])
o = data[0][0]
for i in range(1, len(data)):
    if data[i][0] == o:
        continue
    else:
        o = data[i][0]
        mydata.append(data[i])
print len(mydata)
'''
filepath1 = 'train_new_data.txt'#u'C:\\Users\\Topman3758\\Desktop\\ntt\\ntt_data\\ntt_data\\ntt\\奔驰 E\\微博.txt'
data = processdata(filepath1)
data.sort()
mydata.append(data[0])
o = data[0]
for i in range(1, len(data)):
    if data[i] == o:
        continue
    else:
        o = data[i]
        mydata.append(data[i])
print len(mydata)

'''
filepath1 = u'C:\\Users\\Topman3758\\Desktop\\ntt\\ntt_data\\ntt_data\\ntt\\丰田 RAV4\\微博.txt'
data = processdata(filepath1)
data.sort()
mydata.append(data[0])
o = data[0][0]
for i in range(1, len(data)):
    if data[i][0] == o:
        continue
    else:
        o = data[i][0]
        mydata.append(data[i])
print len(mydata)

for i in range(2):
    print data[i][0]
'''
'''
Months = {}
def init(filename = ''):
    global Months
    f = open(filename, 'r')
    line = f.readline().rstrip()
    index = 1
    while line:
        Months.setdefault(line, 0)
        Months[line] = index
        index += 1
        line = f.readline().rstrip()
    f.close()
init('Month.txt')
def gettime(mytime):
    global Months
    mylist = mytime.split(' ')
    mystr = mylist[-1]+'-'+str(Months[mylist[1]])+'-'+mylist[2]
    return mystr
'''    
f = open("train_input_data.txt", 'w')
for o in mydata:
    f.write(o+'\n')
f.close()


        
