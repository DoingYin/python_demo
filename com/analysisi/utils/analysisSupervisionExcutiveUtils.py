#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import re
import uuid

from com.database.ConnectDataBase import ConnectionDatabase
from com.analysisi.utils import Utils

'''
    数据库连接
'''
def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn

def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa9History")
    return __conn

'''
    解析常务会议文件
'''
def analysisSupervisionExcutiveCsv(fileName):
    # print(fileName)
    #节点反馈数据
    if fileName.name.find("fb") != -1:
        print('节点反馈数据')
        analysisTaskNodeFb(fileName)
        pass
    elif fileName.name.find("node") != -1:
        print("节点数据")
        analysisTaskNode(fileName)
        pass
    else:
        print("基本信息")
        analysisExcutiveCsv(fileName)
        pass


#############################################常务会议督察工作信息##########################################

'''
    解析常务会议督查基本信息
'''
def analysisExcutiveCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 12:
            continue
        task = {}
        task['pviguid'] = row[0]
        task['rowguid'] = row[1]
        task['registername'] = row[2]
        task['registerguid'] = row[3]
        registertimeStr = row[4]
        if registertimeStr and len(registertimeStr) > 0:
            registertime = Utils.formatStrToTime(registertimeStr)
            registertimeStr = Utils.fromatTimeToStr(registertime, '%Y-%m-%d')
        else:
            registertimeStr = None
        task['registertime'] = registertimeStr
        task['supervisionnum'] = row[5]
        task['taskname'] = row[6]
        executivetimeStr = row[7]
        if executivetimeStr and len(executivetimeStr) > 0:
            executivetime = Utils.formatStrToTime(executivetimeStr)
            executivetimeStr = Utils.fromatTimeToStr(executivetime, '%Y-%m-%d')
        else:
            executivetimeStr = None
        task['executivetime'] = executivetimeStr

        feedbacktimeStr = row[8]
        if feedbacktimeStr and len(feedbacktimeStr) > 0:
            feedbacktime = Utils.formatStrToTime(feedbacktimeStr)
            feedbacktimeStr = Utils.fromatTimeToStr(feedbacktime, '%Y-%m-%d')
        else:
            feedbacktimeStr = None
        task['feedbacktime'] = feedbacktimeStr
        meetingcontentStr = row[9]
        meetingcontentStr1 = re.sub('<[^>]*>', '', meetingcontentStr)
        task['meetingcontent'] = meetingcontentStr1
        matcherObjs = Utils.getStrByReg(meetingcontentStr, '[0-9a-zA-Z]{32}')
        # print(matcherObjs)
        if matcherObjs:
            wd24PviGuid = matcherObjs[1]
        task['BelongXiaQuCode'] = wd24PviGuid
        task['yearFlag'] = row[10]
        isacrossyear = 0
        if '是' == row[11]:
            isacrossyear = 1
        task['isacrossyear'] = isacrossyear
        task['imported'] = "1"
        task['taskType'] = "1"
        task['pvistatus'] = "9"
        # print(task)
        if insertTask(__conn, task):
            counter += 1
            print("插入常务会议数据：%d 条。"%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入常务会议督查任务数据
'''
def insertTask(__conn, task):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_REGISTER(pviguid, rowguid, registername, registerguid, registertime,
        supervisionnum, taskname, executivetime, feedbacktime, meetingcontent, BelongXiaQuCode, yearFlag, isacrossyear, 
        imported, taskType, pvistatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (task['pviguid'], task['rowguid'], task['registername'], task['registerguid'], task['registertime'],
                task['supervisionnum'], task['taskname'], task['executivetime'], task['feedbacktime'],
                task['meetingcontent'], task['BelongXiaQuCode'],task['yearFlag'], task['isacrossyear'],
                task['imported'], task['taskType'], task['pvistatus'])
    return __conn.mssql_exe_sql(__sql, __params)

'''
    解析节点数据
'''
def analysisTaskNode(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 8:
            continue
        taskNode = {}
        taskNode['rowguid'] = row[0]
        taskNode['taskregisterguid'] = row[1]
        taskNode['YearFlag'] = row[2]
        taskNode['ordernum'] = row[3]
        taskNode['nodename'] = row[4]
        taskNode['issuecontent'] = row[5]
        taskNode['Responseouname'] = row[6]
        taskNode['finisheddetail'] = row[7]
        taskNode['BelongXiaQuCode'] = "1"
        # print(taskNode)
        if insertTaskNode(__conn, taskNode):
            counter += 1
            print("插入常务会议要点数据：%d 条。"%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入常务会议督查任务节点数据
'''
def insertTaskNode(__conn, taskNode):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_Node(RowGuid, taskregisterguid, YearFlag, ordernum, nodename, issuecontent,
        Responseouname, finisheddetail, BelongXiaQuCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (taskNode['rowguid'], taskNode['taskregisterguid'], taskNode['YearFlag'], taskNode['ordernum'],
                taskNode['nodename'], taskNode['issuecontent'], taskNode['Responseouname'], taskNode['finisheddetail'],
                taskNode['BelongXiaQuCode'])
    return __conn.mssql_exe_sql(__sql, __params)


'''
    解析节点反馈数据
'''
def analysisTaskNodeFb(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 7:
            continue
        taskNodeFb = {}
        taskNodeFb['RowGuid'] = row[0]
        taskNodeFb['tasknodeguid'] = row[1]
        taskNodeFb['Ordernum'] = row[2]
        taskNodeFb['feedbacker'] = row[3]
        taskNodeFb['feedbackerguid'] = row[4]
        operateDateStr = row[5]
        if operateDateStr and len(operateDateStr) > 0:
            operateDate = Utils.formatStrToTime(operateDateStr)
            operateDateStr = Utils.fromatTimeToStr(operateDate, '%Y-%m-%d')
        else:
            operateDateStr = None
        taskNodeFb['OperateDate'] = operateDateStr
        taskNodeFb['Others'] = row[6]
        taskNodeFb['BelongXiaQuCode'] = "1"
        # print(taskNodeFb)
        if insertTaskNodeFb(__conn, taskNodeFb):
            counter += 1
            print("插入常务会议反馈数据：%d 条。"%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入节点反馈数据
'''
def insertTaskNodeFb(__conn, taskNodeFb):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_Node_feedback(RowGuid, tasknodeguid, Ordernum, feedbacker, feedbackerguid,
        OperateDate, Others, BelongXiaQuCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (taskNodeFb['RowGuid'], taskNodeFb['tasknodeguid'], taskNodeFb['Ordernum'], taskNodeFb['feedbacker'],
                taskNodeFb['feedbackerguid'], taskNodeFb['OperateDate'], taskNodeFb['Others'],
                taskNodeFb['BelongXiaQuCode'])
    return __conn.mssql_exe_sql(__sql, __params)