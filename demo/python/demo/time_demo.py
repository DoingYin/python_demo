#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import time

#将时间字符串转换为时间元组
timeStr = '2018-08-07 21:56:39'
time1 = time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
print(time1)

#将时间元组转换为时间戳
print(time.mktime(time1))
