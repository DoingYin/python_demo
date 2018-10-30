#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    time模块
    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.
'''
import time

# 接收时间戳并返回格当地时间下的时间元组t。
loctime = time.localtime()
print(loctime)

# 推迟调用线程的运行，secs指秒数。
# time.sleep(2)

# 接收时间元组并返回时间戳。
# loctime1 = time.mktime(loctime)
# print(loctime1)

# 接收时间元组，并返回指定格式可读字符串标识当地时间，格式由fmt决定。
loctime2 = time.strftime('%Y-%m-%d %H:%M:%S  %p', loctime)
print(loctime2)

#接收时间元组，并返回指定格式可读字符串标识当地时间，格式由fmt决定。
loctime3 = time.strptime(str(loctime2), '%Y-%m-%d %H:%M:%S %p')
print(loctime3)

#将时间字符串转换为时间元组
timestr = '2018-08-08'
loctime = time.strptime(timestr, '%Y-%m-%d')
print("*"* 50)
print(loctime)

#返回当前时间的时间戳。
# loctime4 = time.time()
# print(loctime4)

#返回时间,将时间戳转换为时间
# loctime5 = time.ctime(time.time())
# print(loctime5)

