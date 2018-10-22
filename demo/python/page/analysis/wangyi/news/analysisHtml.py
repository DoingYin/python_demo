#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  urllib.request
import re
import os
import urllib.error as error
import parser

#设置需要解析的url
url='https://news.163.com/'

#请求
request = urllib.request.Request(url)

#结果
response = urllib.request.urlopen(request)
data = response.read()
data = data.decode('gbk')
# print(type(data))

print(data)

parser