#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import time
from python.common.ConnectDataBase import ConnectionMyslq


# 解析栏目数据
def getHtmlData(url):
    # 请求
    request = urllib.request.Request(url)

    # 结果
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('gbk')
    return data


# 结项详细信息
def soupDetial(data):
    soup = BeautifulSoup(data)
    content = soup.select('.post_text > *')
    contentStr = ''
    for tag in content:
        # print(tag)
        contentStr += str(tag)
    # print(contentStr)
    return contentStr


# 通过children将字符串转为标签
def soupData(data):
    soup = BeautifulSoup(data)
    infostag = soup.select(".today_news")
    for child in infostag:
        # print(child.children)
        for child1 in child.children:
            print(type(child1))
            print(len(child1))
            if len(child1) > 0:
                print("*" * 50)
                print(child1)
    infos = list()
    index = 0;
    # for atag in infostag:
    #     if re.match('[a-zA-z]+://[^\s]*', atag.get('href')):
    #         info = {}
    #         info['index'] = index
    #         info['text'] = atag.get('')
    #         info['href'] = atag.get('href')
    #         detailData = getHtmlData(atag.get('href'))
    #         content = soupDetial(detailData)
    #         info['content'] = content
    #         infos.append(info)
    #         index += 1
    # print(soup.prettify())
    print(infos)


# 通过children将字符串转为标签
def soupData1(data):
    soup = BeautifulSoup(data)
    infostag = soup.select(".today_news")
    for child in infostag:
        # print(child.children)
        for child1 in child.children:
            print(type(child1))
            print(len(child1))
            if len(child1) > 0:
                print("*" * 50)
                print(child1)


# 通过select样式选择器，选择需要的内容
def soupData2(data):
    soup = BeautifulSoup(data)
    # 获取今日推荐内容
    infostag = soup.select('.today_news > ul > li > a')
    infos = list()
    for child in infostag:
        info = {}
        info['title'] = child.get_text()
        info['href'] = child.get('href')
        info['time'] = time.strftime('%Y-%m-%d', time.localtime())
        # detailData = getHtmlData(child.get('href'))
        # content = soupDetial(detailData)
        # info['content'] = content
        #调用数据库方法，将数据入库
        insertInfo(info)
        # infos.append(info)
    # print(infos)


# 数据入库
def insertInfo(info):
    conn = ConnectionMyslq("localhost", "root",
                           "Gepoint", "pythondb", 3306)
    sql = 'insert into news_info(title, link, time) values("%s", "%s", "%s")' % (
        info['title'], info['href'], info['time'])
    conn.exe_sql(sql)

# 数据查询
def findAll():
    conn = ConnectionMyslq("localhost", "root",
                           "Gepoint", "pythondb", 3306)
    sql = 'select * from news_info'
    result = conn.findList(sql)
    print(result)


if __name__ == "__main__":

    # 中间列数据接口 http://temp.163.com/special/00804KVA/cm_guonei_02.js?callback=data01_callback
    # 网易的今日推荐新闻
    data = getHtmlData(url='http://news.163.com/domestic/')
    # soupData2(data)
    findAll()
    info = {'title': 'skssksks'}
    # insertInfo(info)
    # soupDetial(getHtmlData('http://news.163.com/18/1023/12/DUQ7NIL5000189FH.html'))
