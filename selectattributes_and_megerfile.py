# -*- coding:utf-8 -*-

import os
import sys
import codecs
import xlrd
import types

dir_attr = []

#get all dir and file from mydir
def getFile(mydir = ''):
    try:
        return os.listdir(mydir)
    except Exception,e:
        print str(e)
    
#get the dir of all types
def getFileByType(mydir = ''):
    alldir = getFile(mydir)
    allTypeFile = []
    for o in alldir:
        if os.path.isdir(mydir+'\\'+o) == True:
            allTypeFile.append(mydir+'\\'+o)
    return allTypeFile

#pre process
def preprocess():
    global dir_attr
    name = ['评论', '微博', '用户']
    for o in name:
        dir_attr.append(o.decode('utf-8').encode('gbk'))

#return comment, weiobo, users
def getAllFile(mydir = ''):
    global dir_attr
    files = []
    dict1 = {}
    dir1 = getFile(mydir) # two level dir
    for d in dir1:
        fn = mydir + '\\' + d
        if os.path.isdir(fn) == False: #is file, not dir
            continue
        files = getFile(fn) # get all files in the dir
        tmpfile = []
        for o in files:
            if os.path.isfile(fn+'\\'+o) == True: # is file
                tmpfile.append(fn+'\\'+o)
        #print len(files)
        if d not in dict1.keys():
            dict1[d] = tmpfile
        else:
            dict1[d].extend(tmpfile)
    for key in dict1.keys():
        i = 0
        for o in dir_attr:
            if o == key:
                files[i] = dict1[key]
                break
            i = i + 1
    #comment_files = files[0]
    #weibo_files = files[1]
    #user_files = files[2]
    #print len(comment_files), dir_attr[0]
    #print len(weibo_files), dir_attr[1]
    #print len(user_files), dir_attr[2]
    return files[0], files[1], files[2] # comment, weiobo, users

# oepn excel(.xls)     
def open_excel(filename = ''):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception,e:
        print str(e)

#user_info
user_info = ['id', 'name', 'province', 'city', 'location', 'description', 'gender', 'followers_count', 'friends_count',\
             'statuses_count', 'favourites_count', 'created_at', 'verified', 'verified_type', 'verified_reason', 'follow_me',\
             'bi_followers_count']
#weibo_info
weibo_info = ['wei_id', 'text', 'favorited', 'reposts_count', 'comments_count', 'created_at']
#comment_info
comment_info = ['created_at', 'id', 'text', 'user', 'mid', 'status']

#get user data from excel based index
def excel_table_byindex(filename = '', data_info = [], colnameindex = 1, byindex = 0):
    global user_info
    try:
        data = open_excel(filename)
        table = data.sheets()[byindex]
        nrows = table.nrows
        ncols = table.ncols
        colnames = table.row_values(colnameindex)
        index = []
        for num in range(ncols):
            #print colnames[num], '#####', data_info[num]
            if colnames[num] in data_info:
                index.append(num)
            else:
                index.append(-1)
        content = []
        for rownum in range(2, nrows):
            result = []
            row = table.row_values(rownum)
            for num in range(ncols):
                if index[num] != -1:
                    #print row[num], '!!!'
                    s = ''
                    j = 0
                    for ln in row[num].splitlines():
                        if j == 0:
                            s = s + ln
                        else:
                            s = s + ' ' + ln
                        j = j + 1
                    result.append(s)
            content.append(result)
        return content
    except Exception,e:
        print str(e)

#return str from the list
def getstr(data):
    mystr = ''
    for i in range(len(data)):
        if i == 0:
            mystr = data[i]
        else:
            mystr = mystr + '\3' + data[i]
    return mystr

def merger_users(mydir = ''):
    global user_info
    global weibo_info
    global comment_info
    alldir = getFileByType(mydir)
    for dir1 in alldir:
        #print dir1,'@@@'
        comment_files, weibo_files, user_files = getAllFile(dir1)
        all_users_info = []
        
        #user_info
        user_file = open(dir1 + '\\' + dir_attr[2] + '.txt', 'w')
        mystr = getstr(user_info)
        user_file.write(mystr+'\n')
        for f in user_files:
            content = excel_table_byindex(f, user_info)
            #print type(content)
            all_users_info.extend(content)
            for list1 in content:
                #print list1, '!@#%^&*('
                mystr = getstr(list1)
                user_file.write(mystr.encode('utf-8')+'\n')
        user_file.close()
        print dir1, len(all_users_info)
        
        #weibo_info
        all_weibo_info = []
        weibo_file = open(dir1 + '\\' + dir_attr[1] + '.txt', 'w')
        mystr = getstr(weibo_info)
        weibo_file.write(mystr+'\n')
        for f in weibo_files:
            content = excel_table_byindex(f, weibo_info)
            all_weibo_info.extend(content)
            for list1 in content:
                mystr = getstr(list1)
                weibo_file.write(mystr.encode('utf-8')+'\n')
        weibo_file.close()
        print dir1, len(all_weibo_info)
        #comment_info
        all_comment_info = []
        comment_file = open(dir1 + '\\' + dir_attr[0] + '.txt', 'w')
        mystr = getstr(comment_info)
        comment_file.write(mystr+'\n')
        for f in comment_files:
            content = excel_table_byindex(f, comment_info)
            all_comment_info.extend(content)
            for list1 in content:
                mystr = getstr(list1)
                comment_file.write(mystr.encode('utf-8')+'\n')
        comment_file.close()
        print dir1, len(all_comment_info)
        
rootdir = 'C:\\Users\\Topman3758\\Desktop\\ntt_data\\ntt_data\\ntt'
preprocess() #pre process
merger_users(rootdir)
f = getFileByType(rootdir)

'''
print len(f)
for o in f:
    t = open(o+'\\user.txt', 'w')
    t.close()

for o in f:
    print len(o)
'''
        

    
