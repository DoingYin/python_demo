#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  urllib.request
import re
import os
import urllib.error as error

#url地址
#url='https://blog.csdn.net/xc_zhou/article/details/80907101'
url='https://music.163.com/#/playlist?id=2405723358'

#请求
request = urllib.request.Request(url)

#结果
response = urllib.request.urlopen(request)
data = response.read()

data = data.decode("utf-8")

print(data)

###################图片抓取###########################

imgre = re.compile('<img src=\"(.+?)\"')
imglist = imgre.findall(data)  # re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
# 把筛选的图片地址通过for循环遍历并保存到本地
# 核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
x = 0
dirpath = 'E:/test/'
for imgurl in imglist:
    pattern = re.compile(r'^http://.*.jpg$')
    if pattern.match(imgurl):
        try:
            image_data = urllib.request.urlopen(imgurl).read()
            image_path = dirpath + str(x) + '.png'
            x += 1
            print(image_path)
            with open(image_path, 'wb') as image_file:
                image_file.write(image_data)
            image_file.close()
        except error.URLError as e:
            print('Download failed')


###################歌曲信息抓取###########################


