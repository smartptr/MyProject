# -*- coding:utf-8 -*-

from xml.dom import minidom
import os
import sys
import codecs

# [[DOI, Label], [DOI, Label],...]
paperList = []

wordDict = set()

def splitWord(content = ''):
    global wordDict
    seg_list = jieba.cut(content, cut_all=False)
    seg_list = ' '.join(seg_list)
    for word in seg_list:
        wordDict.add(word)
    return seg_list
    
def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index=0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else ''

#get all file in dir
def getAllFile(dir = ''):
    myfilelist = os.listdir(dir)
    return myfilelist

def parseXML(filename = ''):
    global paperList
    doc = minidom.parse(filename)
    root = doc.documentElement
    #print root
    paper_nodes = get_xmlnode(root, 'PaprElem')
    for node in paper_nodes:
        paprBsc_node = get_xmlnode(node, 'PaprBscElem')
        #print paprBsc_node
        DOI_node = get_xmlnode(paprBsc_node[0], 'DOI')
        doi = get_nodevalue(DOI_node[0])
        #print DOI_node
        type_node = get_xmlnode(paprBsc_node[0], 'PTypCat')
        label = get_nodevalue(type_node[0])
        #print doi, label
        paperList.append([doi, label])

def process():
    global paperList
    dir = ''
    allFile = getAllFile(dir)
    for f in allFile:
        f = dir + '/' + f
        parseXML(f)

def getCon(filename = ''):
    f = None
    try:
        f = open(filename, 'r')
        con = f.readline().rstrip()
        while f:
            str1 = f.readline()
            con = con + str
        return con
    except Exception,e:
        print str(e)

#read all file
def readFile():
    global paperList
    dataSet = []
    dir1 = '../txt'
    allFile = getAllFile(dir)
    for pao in paperList:
        f = dir1 + '/' + pao[0] + '.txt'
        con = getCon(f)
        dataSet.append([pao[0], con, pao[1]])
    return dataSet


def main():
    global paperList
    #process()
    s = '11-1692-F_2012011_X_0000.xml'
    parseXML('11-1692-F_2012011_X_0000.xml')
    s = s[0:s.find('.')]
    s = s + '.txt'
    dataSet = []
    dir1 = '../txt'
    for pao in paperList:
        f = dir1 + '/' + pao[0] + '.txt'
        con = getCon(f.encode('utf-8'))
        dataSet.append([pao[0], con, pao[1]])
    print dataSet
    #print len(paperList)
    #print paperList
    
main()

    
