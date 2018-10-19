#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import os
import re

#按行读取文件中所有的内容
sourceLines = open('analysisTest.txt', 'r', encoding='utf-8').readlines()
#print(lines)

resultFile = open('resultFile.txt', 'a', encoding='utf-8')

linepattern = re.compile('.*.<br />$')
name = ''
link = ''
for line in sourceLines:
    if linepattern.match(line):
        #print(line)
        params = line.split('----')
        if (len(params) > 1) :
            #print(params)
            # print(params[0], params[1])
            #print(params[1].index("<"))
           # if (params[1].index("<") > 0):
            print(params[0] + "——>" + params[1][: -7])
            resultFile.write(params[0] + "——>" + params[1][: -7] + "\n")