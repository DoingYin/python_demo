#!/usr/bin/python
# -*- coding: UTF-8 -*-

import uuid
import time
import re
import json
from com.database.ConnectDataBase import ConnectionDatabase


'''
    数据库连接
'''
def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn

def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn

##########################################读取附件信息到数据库############################################


###########################################批示件基本信息处理##############################################

def getComments(__conn):
    __sql = '''
        SELECT Rowguid, doctitle, replytitle, commentguid, commentsubguid, method, filingdate,
            finishdate, commentleader, commentdate, urgency, securitylevel, fromdept, hostdept,
            assistantdept, opinion, SignUserGuid, SignUserName, signerName FROM sj_comments_old
    '''
    return __conn.mssql_findList(__sql)

def insertComments(__conn, comments):
    __sql = '''
        INSERT INTO SJ_COMMENTS (RowGuid, pviguid, doctitle, replytitle,
        commentguid, commentsubguid, method, filingdate, finishdate, commentleader, 
        commentdate, urgency, securitylevel, fromdept, hostdept, assistantdept, opinion, 
        SignUserGuid, SignUserName, signerName, imported) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d)
    '''
    __params = (comments['RowGuid'], comments['pviguid'], comments['doctitle'], comments['replytitle'],
                comments['commentguid'], comments['commentsubguid'], comments['method'],
                comments['filingdate'], comments['finishdate'], comments['commentleader'],
                comments['commentdate'], comments['urgency'], comments['securitylevel'],
                comments['fromdept'], comments['hostdept'], comments['assistantdept'],
                comments['opinion'], comments['SignUserGuid'], comments['SignUserName'],
                comments['signerName'], comments['imported'])
    # print(__sql % __params)
    return  __conn.mssql_exe_sql(__sql, __params)

def handleComments():
    __conn = getConnect_old()
    records = getComments(__conn)
    counter = 0
    for record in records:
        comments = {}
        comments['RowGuid'] = record[0]
        comments['pviguid'] = record[0]
        comments['doctitle'] = record[1]
        comments['replytitle'] = record[2]
        comments['commentguid'] = record[3]
        comments['commentsubguid'] = record[4]
        comments['method'] = record[5]

        filingdate = record[6]
        if filingdate:
            filingdate = re.sub('[^0-9|\/|:| ]', '', str(filingdate))
        comments['filingdate'] = filingdate

        finishdate = record[7]
        if finishdate:
            finishdate = re.sub('[^0-9|\/|:| ]', '', str(finishdate))
        comments['finishdate'] = finishdate

        comments['commentleader'] = record[8]

        commentdate = record[9]
        if commentdate:
            commentdate = re.sub('[^0-9|\/|:| ]', '', str(commentdate))
        comments['commentdate'] = commentdate

        urgency = record[10]
        if not urgency:
            urgency = '一般'
        comments['urgency'] = urgency

        securitylevel = record[11]
        if not securitylevel:
            securitylevel = '非密'
        comments['securitylevel'] = securitylevel

        comments['fromdept'] = record[12]
        comments['hostdept'] = record[13]
        comments['assistantdept'] = record[14]
        comments['opinion'] = record[15]
        comments['SignUserGuid'] = record[16]
        comments['SignUserName'] = record[17]
        comments['signerName'] = record[18]
        comments['imported'] = 1

        if insertComments(__conn, comments):
            counter += 1
            print('已经添加： %d 条数据。'%counter)

        if counter % 1000 == 0:
            __conn.commitData()

    __conn.commitData()
    __conn.closeConn()


#####################################################流程信息处理############################################################

def getCommentsWorkflow(__conn):
    __sql = '''
        SELECT UNID, subject, SignDate, RegDate, U_UnitIndex, U_UnitName, U_UnitUserTitle, U_UnitEndTime, 
            U_UnitAction, U_UnitToTitle FROM sj_comments_workflow
    '''
    return __conn.mssql_findList(__sql)


def insertCommentsWorkflow(__conn, workflow):
    __sql = '''
        INSERT INTO [oa_old].[dbo].[sj_comments_workflow_copy] ([rowguid], [﻿﻿UNID], [subject], [signdate], [regdate], 
            [U_UnitIndex], [U_UnitName], [U_UnitUserTitle], [U_UnitEndTime], [U_UnitAction], [U_UnitToTitle])
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (workflow['rowguid'], workflow['UNID'], workflow['subject'], workflow['signdate'],
                workflow['RegDate'], workflow['U_UnitIndex'],
                workflow['U_UnitName'], workflow['U_UnitUserTitle'], workflow['U_UnitEndTime'],
                workflow['U_UnitAction'], workflow['U_UnitToTitle'])
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

'''
    处理流程记录信息
'''
def handleCommentsWorkflow():
    __conn = getConnect_old()
    records = getCommentsWorkflow(__conn)
    counter = 0
    for record in records:
        UNID = record[0]
        subject = record[1]
        signdate = record[2]
        RegDate = record[3]
        U_UnitIndexStr = record[4]
        U_UnitNameStr = record[5]
        U_UnitUserTitleStr = record[6]
        U_UnitEndTimeStr = record[7]
        U_UnitActionStr = record[8]
        U_UnitToTitleStr = record[9]
        if U_UnitIndexStr:
            workflow = {}
            workflow['UNID'] = UNID
            workflow['rowguid'] = UNID
            workflow['subject'] = subject
            workflow['signdate'] = signdate
            workflow['RegDate'] = RegDate
            U_UnitIndexs = str(U_UnitIndexStr).split(',')
            for i in range(len(U_UnitIndexs)):
                try:
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
                except Exception as e:
                    print(e)
                    print(record)

                if insertCommentsWorkflow(__conn, workflow):
                    counter += 1
                    print('已经插入: %d 条数据。'%counter)
                if counter % 1000 == 0:
                    __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


#====================================分割线流程意见信息处理============================================
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
            select rowguid,UNID,subject,RegDate,U_UnitName,U_UnitEndTime,U_UnitUserTitle, U_UnitIndex, U_UnitAction, U_UnitToTitle from 
                sj_comments_workflow_copy where UNID='%s' order by U_UnitEndTime ASC
        ''' % pviguid
    # conn = getConnect()
    records = conn.mssql_findList(sql)
    workitemMap = {}
    workitemlist = []
    counter = 0
    if records:
        for coursor in records:
            # print(coursor)
            workflow = {}
            workflow['rowguid'] = coursor[0]
            workflow['UUID'] = coursor[1]
            workflow['wd25Title'] = coursor[2]
            senddate = coursor[3]
            if senddate:
                senddate = re.sub('[^0-9 | \/ | :]', '', senddate)
            else:
                senddate = ''
            workflow['senddate'] = senddate
            workflow['U_UnitName'] = coursor[4]
            U_UnitEndTime = coursor[5]
            if U_UnitEndTime:
                U_UnitEndTime = re.sub('[^0-9 | - | :]', '', U_UnitEndTime)
            else:
                U_UnitEndTime = ''
            workflow['U_UnitEndTime'] = U_UnitEndTime
            workflow['U_UnitUserTitle'] = coursor[6]
            workflow['U_UnitAction'] = coursor[8]
            U_UnitToTitleStr = coursor[9]
            if U_UnitToTitleStr:
                U_UnitToTitleStr = str(U_UnitToTitleStr).replace('等','')
            workflow['U_UnitToTitle'] = U_UnitToTitleStr
            if coursor[1] and coursor[5] and coursor[7]:
                workflow['opinionbody'] = workflow_opinion(coursor[5], coursor[1], coursor[7], coursor[6], conn)
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
        try:
            unitEndTimeStr = re.sub('[^0-9- :]', '', unitEndTimeStr)
            unitEndTime = time.strptime(unitEndTimeStr, '%Y-%m-%d %H:%M:%S')
            unitEndTimeStr = time.strftime('%Y-%m-%d %H:%M', unitEndTime)
        except Exception as e:
            print(e)
            print(unitEndTimeStr)
    try:
        sql = '''
            SELECT opinionTime,OPINIONBODY,parentUnid FROM sj_comments_opinion1 WHERE ParentUnid = '%s' 
                AND OPINIONUSERTITLE = '%s' ORDER BY opinionTime ASC
        ''' % (parentUnid, opinionUserTitle)
        records = conn.mssql_findList(sql)
    except Exception as e:
        print(e)
        print(sql)
    opinionBody = ''
    if records:
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
def workflowdata(pviguid, title, senddate, workitemListJson):
    if senddate:
        senddate = re.sub('[^0-9 | \/ | :]', '', senddate)
    else:
        senddate = ''
    workflow = {}
    workflow['rowguid'] = str(uuid.uuid1())
    workflow['processVersionInstanceGuid'] = pviguid
    workflow['processVersionInstanceName'] = title
    workflow['processVersionGuid'] = ''
    workflow['initiatorname'] = ''
    workflow['startDate'] = senddate
    workflow['endTime'] = ''
    workflow['terminateDate'] = ''
    workflow['status'] = 0
    workflow['tag'] = '2'
    workflow['note'] = ''
    workflow['workitemjson'] = workitemListJson
    workflow['instancejson'] = ''
    workflow['defXml'] = ''
    workflow['operatedate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return  workflow

'''
    插入工作流数据
'''
def insertWorkflowData(workflowData, __conn):
    sql = \
        '''
            insert into workflow_pvi_sd_comments(rowguid,processVersionInstanceGuid,processVersionInstanceName,processVersionGuid,			
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
def workflowListData():
    sql = 'SELECT w1.UNID, w1.subject, w1.RegDate FROM sj_comments_workflow w1'
    __conn1 = getConnect_old()
    cursors = __conn1.mssql_findList(sql)
    counter = 0
    start = time.time()
    for cursor in cursors:
        # print(cursor)
        workitemlist = workitemList(cursor[0], __conn1)
        workitemListJson = json.dumps(workitemlist)
        begin = time.time()
        workflowData = workflowdata(cursor[0], cursor[1], cursor[2], workitemListJson)
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
    print('总共插入：%d, 总用时：%f'%(counter, over-start))
    __conn1.commitData()
    __conn1.closeConn()

##################################################处理单位反馈时间信息##############################################
def insertReadtime(__conn, readtime):
    sql = '''
        INSERT INTO sj_comments_deptreadtime_copy(rowguid, parentguid, hostdept, readtime) VALUES(%s, %s, %s, %s)
    '''
    params = (readtime['rowguid'], readtime['parentguid'], readtime['hostdept'], readtime['readtime'])
    return __conn.mssql_exe_sql(sql, params)


def handle_deptreadtime():
    __conn = getConnect_old()
    sql = 'SELECT rowguid,hostdept,readtime FROM sj_comments_deptreadtime'
    records = __conn.mssql_findList(sql)
    counter = 0
    for record in records:
        readtimeObj = {}
        parentguid = record[0]
        readtimeObj["parentguid"] = parentguid

        hostdeptStr = record[1]
        readtimeStr = record[2]
        try:
            if hostdeptStr:
                hostdepts = hostdeptStr.split(',')
            readtimes = readtimeStr.split(',')
            for i in range(0,len(hostdepts)):
                rowguid = str(uuid.uuid1())
                readtimeObj['rowguid'] = rowguid
                hostdept = hostdepts[i]
                readtimeObj['hostdept'] = hostdept
                if len(readtimes) > 0 and len(readtimes) > 6+i:
                    readtime = readtimes[6+i]
                elif len(readtimes) > 0:
                    readtime = readtimes[0]
                else:
                    readtime = None
                if readtime:
                    readtime = re.sub('[^0-9|\/|:| ]', '', str(readtime))
                readtimeObj['readtime'] = readtime
                if insertReadtime(__conn, readtimeObj):
                    counter += 1
                    print("已经插入：%d 条数据"%counter)
                    if counter % 1000 == 0:
                        __conn.commitData()
        except Exception as e:
            print(e)
            print(parentguid)
            return
    __conn.commitData()
    __conn.closeConn()

##################################################### 附件处理 #######################################################
def handle_Attach():
    __conn = getConnect_old()
    sql = 'SELECT DocUnid,Unid,attachnum,createdate,attachtitle FROM sj_comments_attach1 WHERE attachnum>0'
    results = __conn.mssql_findList(sql)
    counter = 0
    for record in results:
        attachInfo = {}
        CliengGuid = record[0]
        if CliengGuid:
            CliengGuid = re.sub('[^a-zA-Z | 0-9]', '', CliengGuid)
        attachInfo['CliengGuid'] = CliengGuid

        attachInfo['CliengTag'] = 'attach'

        attachInfo['StorageType'] = 'NasShareDirectory'

        attachNum = int(record[2])
        UploadDateTimeStr = '2019-01-17'
        attachInfo['UploadDateTime'] = UploadDateTimeStr

        uploadFilePath = 'E:\OA9Attach\\' + 'BigFileUpLoadStorage/temp/' + UploadDateTimeStr + '/' + CliengGuid + '/'
        attachInfo['FilePath'] = uploadFilePath

        attachTitleStr = str(record[4])
        if attachNum > 1:
            attachTitles = attachTitleStr.split(',')
            for attachName in attachTitles:
                attachInfo['AttachFileName'] = attachName
                attachInfo['ContentType'] = attachName[attachName.find('.'):len(attachName)]
                AttachGuid = str(uuid.uuid1())
                if AttachGuid:
                    AttachGuid = re.sub('[^a-zA-Z | 0-9]', '', AttachGuid)
                attachInfo['AttachGuid'] = AttachGuid

                attachInfo['AttachStorageGuid'] = CliengGuid
                if insertAttachInfo(attachInfo, __conn):
                    counter += 1
                    print('附件信息已经插入：%d 条'%counter)
        else:
            attachInfo['AttachFileName'] = attachTitleStr
            attachInfo['ContentType'] = attachTitleStr[attachTitleStr.find('.'):len(attachTitleStr)]
            AttachGuid = str(uuid.uuid1())
            if AttachGuid:
                AttachGuid = re.sub('[^a-zA-Z | 0-9]', '', AttachGuid)
            attachInfo['AttachGuid'] = AttachGuid

            attachInfo['AttachStorageGuid'] = CliengGuid
            if insertAttachInfo(attachInfo, __conn):
                counter += 1
                print('附件信息已经插入：%d 条'%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


'''
    插入附件信息
'''
def insertAttachInfo(attachInfo, __conn):
    sql = '''
        INSERT INTO Frame_AttachInfo_comments(AttachGuid, AttachFileName, CliengGuid, CliengTag, UploadDateTime,
            ContentType, FilePath, AttachStorageGuid, StorageType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (attachInfo['AttachGuid'], attachInfo['AttachFileName'], attachInfo['CliengGuid'], attachInfo['CliengTag'],
              attachInfo['UploadDateTime'], attachInfo['ContentType'], attachInfo['FilePath'], attachInfo['AttachStorageGuid'],
              attachInfo['StorageType'])
    # print(sql%params)
    return __conn.mssql_exe_sql(sql, params)

#############################################################处理单位反馈意见信息##########################################

'''
    获取单位反馈意见信息
'''
def getFeedbackOpinion(__conn, parentguid, deptname):
    sql = '''
        SELECT OPINIONBODY, feedbackunid FROM sj_comments_unitopinion1 WHERE [﻿﻿ParentUnid]='%s' AND opiniondept='%s'
    '''%(parentguid, deptname)
    # print(sql)
    return __conn.mssql_findList(sql)

'''
    获取部门签收情况
'''
def getDeptReadDetail(__conn):
    sql = '''
        SELECT parentguid, hostdept, readtime FROM sj_comments_deptreadtime_copy
    '''
    return __conn.mssql_findList(sql)

#获取对应反馈的附件信息
def getAttachinfo(__conn, feedbackunid):
    sql = '''
        SELECT attachguid, attachfilename, cliengguid FROM Frame_AttachInfo_feedback WHERE cliengguid = '%s'
    '''\
    %feedbackunid
    # print(sql)
    return __conn.mssql_findList(sql)

'''
    获取部门的签收时间
'''
def getDeptSignDate(__conn, unid, deptname):
    sql = '''
       SELECT rowguid,CONVERT(varchar(100), readtime, 20) as signdate FROM sj_comments_deptreadtime_copy WHERE parentguid='%s' AND hostdept='%s'
    ''' %(unid,deptname)
    return __conn.mssql_findList(sql)

'''
    处理单位反馈意见信息
'''
def handleDeptFeedback():
    __conn = getConnect_old()
    records = getDeptReadDetail(__conn)
    for record in records:
        feedback = {}
        feedbackguid =  ''
        parentguid = record[0]
        feedback['outboxguid'] = parentguid
        deptname = record[1]
        feedback['deptname'] = deptname

        #单位签收时间
        readtime = record[2]
        feedback['feedbackdate'] = readtime
        # print(signDateStr)
        # if signDateStr:
        #     signDateStr = re.sub('[^0-9|\/|:| ]', '', str(signDateStr))
        # signDateStr = ''
        # if signDates:
        #     for signdate in signDates:
        #         signDateStr = signdate[1]
        # feedback['feedbackdate'] = signDateStr

        feedbackcontent = ''
        feedbackResult = getFeedbackOpinion(__conn, parentguid, deptname)
        if feedbackResult:
            feedbackcontent = feedbackResult[0][0]
            feedbackguid = feedbackResult[0][1]
        feedback['feedbackguid'] = feedbackguid
        feedback['feedbackcontent'] = feedbackcontent

        # print(signAndFeedback)
        insertSignFeedback(__conn, feedback)
    __conn.commitData()
    __conn.closeConn()

'''
    插入签收数据
'''
def insertSignFeedback(__conn, feedback):
    sql = '''
        INSERT INTO arce_feedback(feedbackguid, outboxguid, deptname, feedbackdate, feedbackcontent) 
            VALUES (%s, %s, %s, %s, %s)
    '''
    params = (feedback['feedbackguid'], feedback['outboxguid'], feedback['deptname'],
              feedback['feedbackdate'], feedback['feedbackcontent'])
    # print(sql%params)
    return __conn.mssql_exe_sql(sql, params)

'''
    插入反馈信息
'''
def insertFeedbackDetail(__conn, feedback):
    sql = '''
        INSERT INTO sj_comments_feedback(rowguid, parentguid, feedbacktime, feedbackcontent, attachLink) 
            VALUES (%s, %s, %s, %s, %s);
    '''
    params = (feedback['rowguid'], feedback['parentguid'], feedback['feedbacktime'],
              feedback['feedbackcontent'], feedback['attachLink'])
    return __conn.mssql_exe_sql(sql, params)


if __name__ == '__main__':
    handleComments()
    # handleCommentsWorkflow()
    #  workflowListData()
    # handle_Attach()
    # handle_deptreadtime()
    handleDeptFeedback()
    # handleWorkflowAndOpinion()