#!/usr/bin/python
# -*- coding: UTF-8 -*-

import uuid
import time
import re
import json
from com.database.ConnectDataBase import ConnectionDatabase
from tkinter import filedialog

'''
    数据库连接
'''
def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn

def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn


#############################################常务会议督察工作信息##########################################

'''
    获取督察工作信息
'''
def getSupervisionTasks(__conn):
    __sql = '''
        SELECT UNID, registername, registerguid, Registertime, Responseouname, Taskname, 
            feedbacktimes, YearFlag, Supervisionnum, Executivetime, Isacrossyear
        FROM supervision_task_excutive
    '''
    results = __conn.mssql_findList(__sql)
    return results

def insertSupervisionTasks(__conn, supervisionTask):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_REGISTER(rowguid, pviguid, registername, Registertime, 
            Responseouname, Taskname, Feedbacktime, YearFlag, Supervisionnum, Executivetime, 
            Isacrossyear, meetingcontent, tasktype, imported, pvistatus, registerguid) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (supervisionTask['rowguid'], supervisionTask['pviguid'], supervisionTask['registername'],
              supervisionTask['Registertime'], supervisionTask['Responseouname'],
              supervisionTask['Taskname'], supervisionTask['Feedbacktime'],
              supervisionTask['YearFlag'], supervisionTask['Supervisionnum'],
              supervisionTask['Executivetime'], supervisionTask['Isacrossyear'],
              supervisionTask['meetingcontent'], supervisionTask['taskType'],
              supervisionTask['imported'], supervisionTask['pvistatus'],
              supervisionTask['registerguid'])
    # print(__sql % params)
    return __conn.mssql_exe_sql(__sql, params)

'''
    处理年度督察数据
'''
def handleSupervisionTask():
    __conn1 = getConnect_old()
    # __conn2 = getConnect_new()
    records = getSupervisionTasks(__conn1)
    # __conn1.closeConn()

    counter = 0
    for record in records:
        supervisionTask = {}

        UNID = record[0]
        if UNID:
            UNID = re.sub('[^a-zA-Z0-9]', '', str(UNID))
        supervisionTask['rowguid'] = UNID
        supervisionTask['pviguid'] = UNID

        registername = record[1]
        supervisionTask['registername'] = registername

        registerguid = record[2]
        if registerguid:
            registerguid = re.findall(r"U[0-9]{5}", registerguid)[0]
        supervisionTask['registerguid'] = registerguid

        Registertime = record[3]
        if Registertime:
            Registertime = re.sub('[^0-9\/]', '', str(Registertime))
        supervisionTask['Registertime'] = Registertime

        Responseouname = record[4]
        supervisionTask['Responseouname'] = Responseouname

        Taskname = record[5]
        supervisionTask['Taskname'] = Taskname

        Feedbacktime = record[6]
        if Feedbacktime:
            Feedbacktime = re.sub('[^0-9\/]', '', str(Feedbacktime))
        supervisionTask['Feedbacktime'] = Feedbacktime

        YearFlag = record[7]
        supervisionTask['YearFlag'] = YearFlag

        Supervisionnum = record[8]
        supervisionTask['Supervisionnum'] = Supervisionnum

        Executivetime = record[9]
        if Feedbacktime:
            Feedbacktime = re.sub('[^0-9\/]', '', str(Feedbacktime))
        supervisionTask['Executivetime'] = Executivetime

        Isacrossyear = record[10]
        if Isacrossyear == '是':
            Isacrossyear = 1
        else:
            Isacrossyear = 0
        supervisionTask['Isacrossyear'] = Isacrossyear

        meetingcontentGroup = re.findall('[0-9]{1,3}', Taskname)
        meetingcontentNum = 0
        if meetingcontentGroup:
            meetingcontentNum = meetingcontentGroup[0]
        supervisionTask['meetingcontent'] = '区政府第%d次常务会议纪要'%int(meetingcontentNum)

        supervisionTask['taskType'] = 1
        supervisionTask['imported'] = 1
        supervisionTask['pvistatus'] = 9

        if insertSupervisionTasks(__conn1, supervisionTask) > 0:
            counter += 1
            print("已经插入：%d条数据。"%counter)
        if counter % 1000 == 0:
            __conn1.commitData()
    __conn1.commitData()
    __conn1.closeConn()


#############################################################常务会议督查任务节点处理###################################################

def getTaskNode(__conn):
    __sql = '''
        SELECT rowguid, taskguid, nodename, ordernum, issuecontent, Responseouname, others
        FROM supervision_executive_tasknode
    '''
    return __conn.mssql_findList(__sql)


def insertTaskNode(__conn, tasknode):
    __sql = '''
        INSERT INTO [oa_old].[dbo].[SJ_SUPERVISION_TASK_NODE] (
            [rowguid], [taskregisterguid], [nodename], [ordernum], [issuecontent], [Responseouname], [others]
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (tasknode['rowguid'], tasknode['taskguid'], tasknode['nodename'],
                tasknode['ordernum'], tasknode['issuecontent'], tasknode['Responseouname'],
                tasknode['others'])
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

def handleTasknode():
    __conn = getConnect_old()
    records = getTaskNode(__conn)
    counter = 0
    for record in records:
        tasknode = {}
        # print(record)
        tasknode['rowguid'] = record[0]
        tasknode['taskguid'] = record[1]
        tasknode['nodename'] = record[2]
        tasknode['ordernum'] = record[3]
        tasknode['issuecontent'] = record[4]
        tasknode['Responseouname'] = record[5]
        tasknode['others'] = record[6]

        if insertTaskNode(__conn, tasknode):
            counter += 1
            print('已插入： %d 条数据.'%counter)

    __conn.commitData()
    __conn.closeConn()

################################################常务会议督察工作流处理########################################
def getExcutiveWorkflow(__conn):
    __sql = '''
        SELECT UNID, subject, U_UnitIndex, U_UnitName, U_UnitUserTitle, U_UnitEndTime, 
            U_UnitAction, U_UnitToTitle FROM supervision_executive_workflow
    '''
    return __conn.mssql_findList(__sql)


def insertExcutiveWorkflow(__conn, workflow):
    __sql = '''
        INSERT INTO [oa_old].[dbo].[supervision_executive_workflow_copy] ([﻿﻿UNID], [subject], [U_UnitIndex], 
            [U_UnitName], [U_UnitUserTitle], [U_UnitEndTime], [U_UnitAction], [U_UnitToTitle])
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (workflow['UNID'], workflow['subject'], workflow['U_UnitIndex'],
                workflow['U_UnitName'], workflow['U_UnitUserTitle'], workflow['U_UnitEndTime'],
                workflow['U_UnitAction'], workflow['U_UnitToTitle'])
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)


def handleworkflow():
    __conn = getConnect_old()
    records = getExcutiveWorkflow(__conn)
    counter = 0
    for record in records:
        UNID = record[0]
        subject = record[1]
        U_UnitIndexStr = record[2]
        U_UnitNameStr = record[3]
        U_UnitUserTitleStr = record[4]
        U_UnitEndTimeStr = record[5]
        U_UnitActionStr = record[6]
        U_UnitToTitleStr = record[7]
        if U_UnitIndexStr:
            workflow = {}
            workflow['UNID'] = UNID
            workflow['subject'] = subject
            U_UnitIndexs = str(U_UnitIndexStr).split(',')
            for i in range(len(U_UnitIndexs)):
                workflow['U_UnitIndex'] = U_UnitIndexs[i]

                U_UnitNames = str(U_UnitNameStr).split(',')
                workflow['U_UnitName'] = U_UnitNames[i]

                U_UnitUserTitles = str(U_UnitUserTitleStr).split(',')
                workflow['U_UnitUserTitle'] = U_UnitUserTitles[i]

                U_UnitEndTimes = str(U_UnitEndTimeStr).split(',')
                workflow['U_UnitEndTime'] = U_UnitEndTimes[i]

                U_UnitActions = str(U_UnitActionStr).split(',')
                workflow['U_UnitAction'] = U_UnitActions[i]

                U_UnitToTitles = str(U_UnitToTitleStr).split(',')
                workflow['U_UnitToTitle'] = U_UnitToTitles[i]

                if insertExcutiveWorkflow(__conn, workflow):
                    counter += 1
                    print('已经插入: %d 条数据。'%counter)
    __conn.commitData()
    __conn.closeConn()

#######################################################流程意见信息处理######################################################

'''
    数据迁移,封装流程步骤对应的数据
'''
def workitemdata(workflow):
    objworkitem = {}
    objworkitem['workItemGuid'] = workflow['rowguid']
    objworkitem['activityName'] = workflow['U_UnitName']
    objworkitem['workItemName'] = ''
    objworkitem['workItemType'] = ''
    objworkitem['handleUrl'] = ''
    objworkitem['status'] = ''
    objworkitem['readDate'] = workflow['U_UnitEndTime']
    objworkitem['operationDate'] = workflow['U_UnitEndTime']
    objworkitem['createDate'] = workflow['U_UnitEndTime']
    objworkitem['endDate'] = workflow['U_UnitEndTime']
    objworkitem['opinion'] = workflow['opinionbody']
    objworkitem['terminateDate'] = ''
    objworkitem['processVersionInstanceGuid'] = workflow['UUID']
    objworkitem['operationType'] = ''
    objworkitem['transactorName'] = workflow['U_UnitToTitle']
    objworkitem['operatorName'] = workflow['U_UnitAction']
    objworkitem['operationname'] = workflow['U_UnitAction']
    objworkitem['operatorForDisplayName'] = workflow['U_UnitToTitle']
    objworkitem['senderName'] = workflow['U_UnitUserTitle']
    objworkitem['note'] = ''
    return objworkitem

'''
    审批流程对应的步骤数据列表
'''
def workitemList(pviguid, conn):
    #通过流程guid获取相关的审批步骤数据
    sql = \
        '''
            select UNID,subject,U_UnitName,U_UnitEndTime,U_UnitUserTitle, U_UnitIndex, U_UnitAction, U_UnitToTitle from 
                supervision_executive_workflow_copy where UNID='%s' order by U_UnitEndTime ASC
        ''' % pviguid
    # conn = getConnect()
    records = conn.mssql_findList(sql)
    workitemMap = {}
    workitemlist = []
    counter = 0
    for coursor in records:
        # print(coursor)
        workflow = {}
        workflow['rowguid'] = coursor[0]
        workflow['UUID'] = coursor[0]
        workflow['subject'] = coursor[1]
        workflow['U_UnitName'] = coursor[2]
        U_UnitEndTime = coursor[3]
        if U_UnitEndTime:
            U_UnitEndTime = re.sub('[^0-9 | - | :]', '', U_UnitEndTime)
        else:
            U_UnitEndTime = ''
        workflow['U_UnitEndTime'] = U_UnitEndTime
        workflow['U_UnitUserTitle'] = coursor[4]
        workflow['U_UnitAction'] = coursor[6]
        U_UnitToTitleStr = coursor[7]
        if U_UnitToTitleStr:
            U_UnitToTitleStr = str(U_UnitToTitleStr).replace('等','')
        workflow['U_UnitToTitle'] = U_UnitToTitleStr
        if coursor[0] and coursor[3] and coursor[4]:
            workflow['opinionbody'] = workflow_opinion(coursor[3], coursor[0], coursor[5], coursor[4], conn)
        else:
            workflow['opinionbody'] = ''
        if workflow['opinionbody'] != '':
            counter += 1
            print("找到：%d 条意见信息。"%counter)
        workitem = workitemdata(workflow)
        workitemlist.append(workitem)
    workitemMap['workitemlist'] = workitemlist
    return workitemMap

'''
    获取对应的意见信息
'''
def workflow_opinion(unitEndTimeStr, parentUnid, unitIndex, opinionUserTitle, conn):
    if unitEndTimeStr:
        unitEndTimeStr = re.sub('[^0-9 | - | :]', '', unitEndTimeStr)
        # unitEndTime = time.strptime(unitEndTimeStr, '%Y/%m/%d %H:%M:%S')
        # unitEndTimeStr = time.strftime('%Y-%m-%d %H:%M', unitEndTime)
    sql = '''
            SELECT time,OPINIONBODY,parentUnid FROM supervision_task_opinion WHERE ParentUnid = '%s' 
                AND UnitIndex = %d AND OPINIONUSERTITLE = '%s' ORDER BY time ASC
        ''' % (parentUnid, int(unitIndex), opinionUserTitle)
    records = conn.mssql_findList(sql)
    opinionBody = ''
    if records and len(records) > 0:
        for record in records:
            opinionTimeStr = record[0]
            if opinionTimeStr:
                opinionTimeStr = re.sub('[^0-9 | \/ | :]', '', opinionTimeStr)
                opinionTime = time.strptime(opinionTimeStr, '%Y/%m/%d %H:%M:%S')
                opinionTimeStr = time.strftime('%Y-%m-%d %H:%M', opinionTime)
                print(opinionTimeStr)
                if unitEndTimeStr == opinionTimeStr:
                    opinionBody = record[1]
                    break
    return opinionBody


'''
    workflow对应的一条数据模型
'''
def workflowdata(pviguid, title, workitemListJson):
    workflow = {}
    workflow['rowguid'] = str(uuid.uuid1())
    workflow['processVersionInstanceGuid'] = pviguid
    workflow['processVersionInstanceName'] = title
    workflow['processVersionGuid'] = None
    workflow['initiatorname'] = None
    workflow['startDate'] = None
    workflow['endTime'] = None
    workflow['terminateDate'] = None
    workflow['status'] = 0
    workflow['tag'] = '2'
    workflow['note'] = None
    workflow['workitemjson'] = workitemListJson
    workflow['instancejson'] = None
    workflow['defXml'] = None
    workflow['operatedate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return  workflow

'''
    插入工作流数据
'''
def insertWorkflowData(workflowData, __conn):
    sql = \
        '''
            insert into workflow_pvi_sd_supervision_1(rowguid,processVersionInstanceGuid,processVersionInstanceName,processVersionGuid,			
                initiatorname,startDate,endTime,terminateDate,status,tag,note,workitemjson,instancejson,defXml) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%d,%s,%s,%s,%s,%s)
        '''
    params = (workflowData['rowguid'],workflowData['processVersionInstanceGuid'],workflowData['processVersionInstanceName'], \
              workflowData['processVersionGuid'],workflowData['initiatorname'], workflowData['startDate'],workflowData['endTime'], \
              workflowData['terminateDate'],workflowData['status'],workflowData['tag'],workflowData['note'], \
              workflowData['workitemjson'],workflowData['instancejson'],workflowData['defXml'])
    # print(sql % params)
    return  __conn.mssql_exe_sql(sql, params)

'''
    workflow数据集，构建迁移数据模型，插入数据
'''
def handleWorkflowData():
    sql = 'SELECT w1.UNID, w1.subject FROM supervision_executive_workflow w1'
    __conn1 = getConnect_old()
    cursors = __conn1.mssql_findList(sql)
    counter = 0
    start = time.time()
    for cursor in cursors:
        # print(cursor)
        workitemlist = workitemList(cursor[0], __conn1)
        workitemListJson = json.dumps(workitemlist)
        begin = time.time()
        workflowData = workflowdata(cursor[0], cursor[1], workitemListJson)
        # print(workflowData)
        if(insertWorkflowData(workflowData, __conn1)):
            counter += 1
            pass
        else:
            break
        end = time.time()
        if counter % 1000 == 0:
            __conn1.commitData()
        print('工作流数据已插入：%d, 用时为：%f'%(counter, end-begin))
    over=time.time()
    __conn1.commitData()
    print('总共插入：%d, 总用时：%f'%(counter, over-start))
    __conn1.closeConn()

if __name__ == '__main__':
    # str = '区政府第22次常务会议决定事项落实情况 '
    # print(re.findall('[0-9]{1,3}', str)[0])
    # handleSupervisionTask()
    # handleworkflow()
    handleWorkflowData()
    # handleTasknode()