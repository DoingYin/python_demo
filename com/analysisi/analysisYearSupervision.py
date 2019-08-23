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


#############################################年度督察工作信息##########################################

'''
    获取督察工作信息
'''
def getSupervisionTasks(__conn):
    __sql = '''
        SELECT UNID, registername, Registertime, Responseouname, Peiheouname, Typename,
            typeguid, typelevel, Taskname, Fenguanname, fenguanguid, Ordernum, Feedbacktime,
            Feedbackcyvle, isfinished, Responseoutel, Peiheoutel, YearFlag, registerguid
            FROM supervision_task_2018
    '''
    results = __conn.mssql_findList(__sql)
    return results

def insertSupervisionTasks(__conn, supervisionTask):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_REGISTER(rowguid, pviguid, registername, Registertime, 
            Responseouname, Peiheouname, Typename, typeguid, typelevel, Taskname, Fenguanname, 
            fenguanguid, Ordernum, Feedbacktime, Feedbackcyvle, isfinished, Responseoutel, 
            Peiheoutel, YearFlag, taskType, imported, pvistatus, registerguid) VALUES(%s, %s, %s, %s
            , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (supervisionTask['rowguid'], supervisionTask['pviguid'], supervisionTask['registername'],
              supervisionTask['Registertime'], supervisionTask['Responseouname'], supervisionTask['Peiheouname'],
              supervisionTask['Typename'], supervisionTask['typeguid'], supervisionTask['typelevel'],
              supervisionTask['Taskname'], supervisionTask['Fenguanname'], supervisionTask['fenguanguid'],
              supervisionTask['Ordernum'], supervisionTask['Feedbacktime'], supervisionTask['Feedbackcyvle'],
              supervisionTask['isfinished'], supervisionTask['Responseoutel'], supervisionTask['Peiheoutel'],
              supervisionTask['YearFlag'], supervisionTask['taskType'], supervisionTask['imported'],
              supervisionTask['pvistatus'], supervisionTask['registerguid'])
    # print(__sql % params)
    try:
        results = __conn.mssql_exe_sql(__sql, params)
    except Exception as e:
        print(__sql%params)
        print(e)
    return results

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

        Registertime = record[2]
        if Registertime:
            Registertime = re.sub('[^0-9\/]', '', str(Registertime))
        supervisionTask['Registertime'] = Registertime

        Responseouname = record[3]
        supervisionTask['Responseouname'] = Responseouname

        Peiheouname = record[4]
        supervisionTask['Peiheouname'] = Peiheouname

        Typename = record[5]
        supervisionTask['Typename'] = Typename

        typeguid = record[6]
        # if typeguid == '0000_1':
        #     typeguid = '54774d35-b901-40cb-8c2a-df8749d1473d'
        # elif typeguid == '0000_2':
        #     typeguid = '1f7a7fb9-9a4f-4cc6-9e64-28a0f3fe4b6f'
        # elif typeguid == '0000_3':
        #     typeguid = '812cdf9b-9e29-44d4-a482-9c9ca20b9bf9'
        # elif typeguid == '0000_4':
        #     typeguid = 'c40c0d94-7887-4a91-8cb6-f4ff223f3714'
        # elif typeguid == '0000_5':
        #     typeguid = '65a6789c-e461-4812-83ab-d55d63c02cac'
        # elif typeguid == '0000_6':
        #     typeguid = '9697c7d4-102a-4b69-a2de-ec9c4f7a1656'
        supervisionTask['typeguid'] = typeguid

        typelevel = record[7]
        supervisionTask['typelevel'] = str(typelevel).replace('_', '/')

        Taskname = record[8]
        supervisionTask['Taskname'] = Taskname

        Fenguanname = record[9]
        supervisionTask['Fenguanname'] = Fenguanname

        fenguanguid = record[10]
        supervisionTask['fenguanguid'] = fenguanguid

        Ordernum = record[11]
        supervisionTask['Ordernum'] = Ordernum

        Feedbacktime = record[12]
        if Feedbacktime:
            Feedbacktime = re.sub('[^0-9\/]', '', str(Feedbacktime))
        supervisionTask['Feedbacktime'] = Feedbacktime

        Feedbackcyvle = record[13]
        supervisionTask['Feedbackcyvle'] = Feedbackcyvle

        isfinished = record[14]
        supervisionTask['isfinished'] = isfinished

        Responseoutel = record[15]
        supervisionTask['Responseoutel'] = Responseoutel

        Peiheoutel = record[16]
        supervisionTask['Peiheoutel'] = Peiheoutel

        YearFlag = record[17]
        supervisionTask['YearFlag'] = YearFlag

        registerguid = record[18]
        if registerguid:
            registerguid = re.findall(r"U[0-9]{5}", registerguid)[0]
        supervisionTask['registerguid'] = registerguid

        supervisionTask['taskType'] = 0
        supervisionTask['imported'] = 1
        supervisionTask['pvistatus'] = 9

        if insertSupervisionTasks(__conn1, supervisionTask) > 0:
            counter += 1
        if counter % 1000 == 0:
            __conn1.commitData()
        print("已经插入：%d条数据。"%counter)
    __conn1.commitData()
    __conn1.closeConn()



#############################################################任务节点处理###################################################

def getTaskNode(__conn):
    __sql = '''
        SELECT rowguid, YearFlag, nodename, ordernum, finishedtime, feedbacktype, finisheddetail, 
            finishedprogress, status, others, Responseouname, taskguid
        FROM supervision_tasknode_2018
    '''
    return __conn.mssql_findList(__sql)


def insertTaskNode(__conn, tasknode):
    __sql = '''
        INSERT INTO [oa_old].[dbo].[SJ_SUPERVISION_TASK_NODE] (
            [rowguid], [YearFlag], [nodename], [ordernum], [finishedtime], [feedbacktype], 
            [finisheddetail], [finishedprogress], [status], [others], [Responseouname], 
            [taskregisterguid]) 
            VALUES (%s, %s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (tasknode['rowguid'], tasknode['YearFlag'], tasknode['nodename'],
                tasknode['ordernum'], tasknode['finishedtime'], tasknode['feedbacktype'],
                tasknode['finisheddetail'], tasknode['finishedprogress'], tasknode['status'],
                tasknode['others'], tasknode['Responseouname'], tasknode['taskguid'])
    print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

def handleTasknode():
    __conn = getConnect_old()
    records = getTaskNode(__conn)
    counter = 0
    for record in records:
        tasknode = {}
        print(record[0])
        tasknode['rowguid'] = record[0]
        tasknode['YearFlag'] = record[1]
        tasknode['nodename'] = record[2]
        ordernum = record[3]
        if ordernum:
            tasknode['ordernum'] = int(ordernum)
        else:
            tasknode['ordernum'] = 1
        finishedtime = record[4]
        if finishedtime:
            finishedtime = re.sub('[^0-9 | \/ | :|-]', '', finishedtime)
        tasknode['finishedtime'] = finishedtime
        tasknode['feedbacktype'] = record[5]
        tasknode['finisheddetail'] = record[6]
        tasknode['finishedprogress'] = record[7]
        tasknode['status'] = record[8]
        tasknode['others'] = record[9]
        tasknode['Responseouname'] = record[10]
        tasknode['taskguid'] = record[11]

        if insertTaskNode(__conn, tasknode):
            counter += 1
            print('已插入： %d 条数据.'%counter)

    __conn.commitData()
    __conn.closeConn()


#############################################################摘要反馈处理############################################
def getTaskSummary(__conn):
    __sql = '''
        SELECT unid, PARENTUNID, Subject, DraftDate, Draftertitle, DeptTitle, 
            Drafter, MainDeptTitle, YYear, MMonth, abstract FROM supervision_summary_2018
    '''
    results = __conn.mssql_findList(__sql)
    return results

def insertSummary(__conn, summary):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_SUMMARY(rowguid, summaryyear, summarymonth, taskname, 
            taskguid, responseouname, feedbacker, feedbackerguid, feedbacktime, txtcontent) 
            VALUES(%s, %d, %d, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (summary['rowguid'], summary['summaryyear'], summary['summarymonth'],
              summary['taskname'], summary['taskguid'], summary['responseouname'],
              summary['feedbacker'], summary['feedbackerguid'], summary['feedbacktime'],
              summary['txtcontent'])
    print(__sql%params)
    try:
        results = __conn.mssql_exe_sql(__sql, params)
    except Exception as e:
        print(__sql%params)
    return results

def handleSummary():
    __conn = getConnect_old()
    records = getTaskSummary(__conn)
    counter = 0
    for record in records:
        summary = {}
        unid = record[0]
        if unid:
            unid = re.sub('[^a-zA-Z0-9]', '', str(unid))
        summary['rowguid'] = unid

        parentguid = record[1]
        if parentguid:
            parentguid = re.sub('[^a-zA-Z0-9]', '', str(parentguid))
        summary['taskguid'] = parentguid

        subject = record[2]
        summary['taskname'] = subject

        DraftDate = record[3]
        if DraftDate:
            DraftDate = re.sub('[^0-9\/ | :|-]', '', str(DraftDate))
        summary['feedbacktime'] = DraftDate

        Draftertitle = record[4]
        summary['feedbacker'] = Draftertitle

        DeptTitle = record[5]
        summary['responseouname'] = DeptTitle

        Drafter = record[6]
        summary['feedbackerguid'] = Drafter

        MainDeptTitle = record[7]
        summary['responseouname'] = MainDeptTitle

        YYear = record[8]
        if not YYear:
            YYear = DraftDate.split('-')[0]
        summary['summaryyear'] = int(YYear)

        MMonth = record[9]
        if not MMonth:
            MMonth = DraftDate.split('-')[1]
        print(unid)
        summary['summarymonth'] = int(MMonth)
        abstract = record[10]
        summary['txtcontent'] = abstract

        if insertSummary(__conn, summary) > 0:
            counter += 1
            print('已经插入：%d 条数据。'%counter)
    __conn.commitData()
    __conn.closeConn()


#######################################流程信息处理#########################################

def getTaskWorkflow(__conn):
    sql = '''
        SELECT UNID, subject, U_UnitIndex, U_UnitName, U_UnitUserTitle, U_UnitEndTime, 
            U_UnitAction, U_UnitToTitle FROM supervision_task_workflow_2016
    '''
    results = __conn.mssql_findList(sql)
    return results

def insertWorkflow(__conn, workflow):
    __sql = '''
        INSERT INTO [oa_old].[dbo].[supervision_task_workflows] ([﻿﻿UNID], [subject], [U_UnitIndex], 
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

    records = getTaskWorkflow(__conn)
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

                if insertWorkflow(__conn, workflow):
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
    objworkitem['workItemGuid'] = str(uuid.uuid1())
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
    objworkitem['processVersionInstanceGuid'] = workflow['UNID']
    objworkitem['operationType'] = ''
    objworkitem['transactorName'] = workflow['U_UnitUserTitle']
    objworkitem['operatorName'] = workflow['U_UnitAction']
    objworkitem['operationname'] = workflow['U_UnitAction']
    objworkitem['operatorForDisplayName'] = workflow['U_UnitUserTitle']
    objworkitem['senderName'] = workflow['U_UnitToTitle']
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
                supervision_task_workflows where UNID='%s' order by U_UnitEndTime ASC
        ''' % pviguid
    # conn = getConnect()
    records = conn.mssql_findList(sql)
    workitemMap = {}
    workitemlist = []
    counter = 0
    if records and len(records)>0:
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
            unitUserTitle = coursor[4]
            if unitUserTitle == ':':
                continue
            workflow['U_UnitUserTitle'] = unitUserTitle
            unitAction = coursor[6]
            if unitAction == ':':
                continue
            workflow['U_UnitAction'] = unitAction
            U_UnitToTitleStr = coursor[7]
            if U_UnitToTitleStr:
                U_UnitToTitleStr = str(U_UnitToTitleStr).replace('等','')
            if U_UnitToTitleStr == ':':
                continue
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
            insert into workflow_pvi_sd_supervision_0(rowguid,processVersionInstanceGuid,processVersionInstanceName,processVersionGuid,			
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
    sql = 'SELECT w1.UNID, w1.subject FROM supervision_task_workflow_2018 w1'
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

####################################################节点反馈信息########################################################
'''
    获取节点反馈意见信息
'''
def getNodeFeedback(__conn):
    __sql = '''
        select [﻿﻿Ordernum], [tasknodeguid], [feedbacker], [feedbackerguid], [OperateDate], [feedbacktype], 
            [finisheddetail], [finishedprogress], [Others], [rowguid] from supervision_tasknode_feedback_2018
    '''
    return __conn.mssql_findList(__sql)

def insertNodeFeedback(__conn, nodefeedback):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TASK_NODE_FEEDBACK ([﻿﻿Ordernum], [tasknodeguid], [feedbacker],
            [feedbackerguid], [OperateDate], [feedbacktype], [finisheddetail], [finishedprogress],
            [Others], [rowguid]) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    __params = (nodefeedback['﻿﻿Ordernum'], nodefeedback['tasknodeguid'], nodefeedback['feedbacker'],
                nodefeedback['feedbackerguid'], nodefeedback['OperateDate'], nodefeedback['feedbacktype'],
                nodefeedback['finisheddetail'], nodefeedback['finishedprogress'], nodefeedback['Others'],
                nodefeedback['rowguid']
                )
    print(__sql%__params)
    return __conn.mssql_exe_sql(__sql, __params)

'''
    节点反馈信息处理
'''
def handleNodeFeedback():
    __conn = getConnect_old()
    records = getNodeFeedback(__conn)
    counter = 0
    for record in records:
        nodefeedback = {}
        nodefeedback['﻿﻿Ordernum'] = record[0]
        nodefeedback['tasknodeguid'] = record[1]
        nodefeedback['feedbacker'] = record[2]
        nodefeedback['feedbackerguid'] = record[3]
        OperateDate = record[4]
        if OperateDate:
            OperateDate = re.sub('[^0-9 | :|-|/]', '', OperateDate)
        nodefeedback['OperateDate'] = OperateDate
        nodefeedback['feedbacktype'] = record[5]
        nodefeedback['finisheddetail'] = record[6]
        nodefeedback['finishedprogress'] = record[7]
        nodefeedback['Others'] = record[8]
        nodefeedback['rowguid'] = record[9]
        if insertNodeFeedback(__conn, nodefeedback):
            counter += 1
            print('已经插入：%d 条数据。'%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

##################################################类别配置信息处理#####################################################
def getTypeSetting(__conn):
    __sql = '''
        SELECT unid,code,name,categorynum,ordernum,yearflag FROM supervision_tasktypesetting2018
    '''
    return __conn.mssql_findList(__sql)

def insertTypeSetting(__conn, typesetting):
    __sql = '''
        INSERT INTO SJ_SUPERVISION_TYPE_SETTING ([RowGuid], [code], [name], [categorynum], 
            [ordernum], [YearFlag]) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    __params = (typesetting['RowGuid'], typesetting['code'], typesetting['name'], typesetting['categorynum'],
                typesetting['ordernum'], typesetting['YearFlag'])
    return __conn.mssql_exe_sql(__sql, __params)

def handleTypeSetting():
    __conn = getConnect_old()
    records = getTypeSetting(__conn)
    counter = 0
    for record in records:
        typesetting = {}
        typesetting['RowGuid'] = record[0]
        typesetting['code'] = record[1]
        typesetting['name'] = record[2]
        typesetting['categorynum'] = record[3]
        typesetting['ordernum'] = record[4]
        typesetting['YearFlag'] = record[5]
        if insertTypeSetting(__conn, typesetting):
            counter += 1
            print('已经插入：%d 条数据。'%counter)
    __conn.commitData()
    __conn.closeConn()

if __name__ == '__main__':
    # a = 'CN=U05514aO=SJGOV'
    # matchObj =  re.findall(r"U[0-9]{5}", a)
    # print(matchObj[0])
    # handleSupervisionTask()
    # handleSummary()
    # handleworkflow()
    handleWorkflowData()
    # handleTasknode()
    # handleNodeFeedback()
    # handleTypeSetting()