#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
from xml.dom.minidom import parse
import xml.dom.minidom
from com.database.ConnectDataBase import ConnectionDatabase
import pymysql
import pymssql

def analysisSupervision():
    file = open('F:\松江OA\OA数据解析\supervision', 'r', encoding='utf-8')
    for line in file.readlines():
        lineArr = line.split(',')
        if (len(lineArr) > 1):
            guid = lineArr[0]
            name = lineArr[1]
            print(guid, name, sep='->')

# 获取的列表信息
def getXMLData(url):
    # 请求
    request = urllib.request.Request(url)
    request.add_header(
        'Cookie', '_eGov_workurger.nsf_=4.0; LastLoginUser=zhanglei; LtpaToken=AAECAzVCRDEyMTUxNUJEMTU5OTFDTj1VMDYzNzMvTz1TSkdPVs4kv2dcFxGhLi9x061UX9baHTAX')

    # 结果
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('utf-8')
    # print(data)
    with open('supervision.xml', 'w', encoding='utf-8') as file:
        content = file.write(data)
        # print(content)  #返回的是成功写入的字符串长度
    # 解析数据
    data = praseXML('supervision.xml')
    return data

# 获取详细信息
def getHtmlData(url):
    # 请求
    request = urllib.request.Request(url)
    request.add_header(
        'Cookie', '_eGov_workurger.nsf_=4.0; LastLoginUser=zhanglei; LtpaToken=AAECAzVCRDEyMTUxNUJEMTU5OTFDTj1VMDYzNzMvTz1TSkdPVs4kv2dcFxGhLi9x061UX9baHTAX')

    # 结果
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('GBK')
    # print(data)
    # with open('supervision.xml', 'w', encoding='utf-8') as file:
    #     content = file.write(data)
    #     # print(content)  #返回的是成功写入的字符串长度
    # 解析数据
    # data = praseXML('supervision.xml')
    return data

#解析XML文件
def praseXML(filename):
    DOMTree = xml.dom.minidom.parse(filename)
    viewentries = DOMTree.documentElement
    # print(collection)
    # if viewentries.hasAttribute("timestamp"):
    #     print("Root element : %s"%viewentries.getAttribute("timestamp"))
    viewentrys = viewentries.getElementsByTagName("viewentry")
    supervisions = list()
    for viewentry in viewentrys:
        # print(viewentry.getAttribute("unid"))
        supervision_task = {}
        if viewentry.hasAttribute("unid"):
            supervision_task["taskguid"] = viewentry.getAttribute("unid")
        colums = viewentry.getElementsByTagName('entrydata')
        for colum in colums:
            # print(colum.getAttribute("name") == "$Subject")
            if colum.hasAttribute("name") and colum.getAttribute("name") == "$Subject":
                supervision_task["taskname"] = colum.getElementsByTagName("text")[0].childNodes[0].data
                # print(colum.getElementsByTagName("text")[0].childNodes[0].data)
            if colum.hasAttribute("name") and colum.getAttribute("name") == "$taskflag":
                supervision_task["feedbackflag"] = colum.getElementsByTagName("text")[0].childNodes[0].data
            if colum.hasAttribute("name") and colum.getAttribute("name") == "$MainDeptTitle":
                supervision_task["responseouname"] = colum.getElementsByTagName("text")[0].childNodes[0].data
            if colum.hasAttribute("name") and colum.getAttribute("name") == "$HelpDeptTitle":
                peiheouname = ''
                if len(colum.getElementsByTagName("text")[0].childNodes) > 0:
                    peiheouname = colum.getElementsByTagName("text")[0].childNodes[0].data
                supervision_task["peiheouname"] = peiheouname
            if colum.hasAttribute("name") and colum.getAttribute("name") == "$onworkflag":
                if len(colum.getElementsByTagName("text")[0].childNodes) > 0:
                    supervision_task["hastasknode"] = colum.getElementsByTagName("text")[0].childNodes[0].data
            supervisions.append(supervision_task)
    # print("the length:%d"%len(supervisions))
    return supervisions

def insertData(supervision):
    conn = ConnectionDatabase("localhost", "sa", "11111", "oa_supervision")
    sql = 'SELECT * FROM SJ_SUPERVISION_TASK_REGISTER'
    results = conn.mssql_findList(sql)
    print("-"*50, "sqlserver","-"*50)
    for result in results:
        print(result)


    # conn1 = ConnectionDatabase("localhost", "root", "Gepoint", "pythondb")
    # sql = 'SELECT * FROM user'
    # results = conn1.mysql_findList(sql)
    # print("-"*50, "mysql","-"*50)
    # for result in results:
    #     print(result)
if __name__ == '__main__':
    # analysisSupervision()
    listUrl = 'http://webnew.songjiang.gov.cn/eGov/workurger.nsf/AllInfoByTree?ReadViewEntries&Count=100&Start=1&RestrictToCategory=1'
    taskdetailUrl = 'http://webnew.songjiang.gov.cn/eGov/workurger.nsf/AllInfoByTree/F3ED8A333C2D3E6D4825822D002D1F01'
    # tasks = list()
    # 解析的任务列表数据
    # for i in range(1, 7):
    #     listUrl = 'http://webnew.songjiang.gov.cn/eGov/workurger.nsf/AllInfoByTree?ReadViewEntries&Count=100&Start=1&RestrictToCategory=%d'%i
    #     data = getHtmlData(listUrl)
    #     tasks.extend(data)

    # print(len(tasks))

    # print(getHtmlData(taskdetailUrl))
    supervision = {}
    insertData(supervision)