#!/usr/bin/python
# -*- coding: UTF-8 -*-
import uuid
import xlrd
import time
import datetime
import json
import re
from com.database.ConnectDataBase import ConnectionDatabase

'''
    数据库连接
'''

def getConnect():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn

'''
    插入用户数据
'''
def insertUserinfoData(userinfo):
    conn = getConnect()
    sql = "INSERT INTO user_info(rowguid, uid, fullname, name, loginname, cellphone, ouname, " \
          "baseouname, job, email) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (userinfo["rowguid"], userinfo["uid"], userinfo["fullname"], userinfo["name"],
             userinfo["loginname"], userinfo["cellphone"], userinfo["ouname"],
             userinfo["baseouname"], userinfo["job"], userinfo["email"])
    # print(sql)
    conn.mssql_exe_sql(sql)

'''
    解析用户信息
'''
def analysisUser_info():
    filepath="F:\\松江OA\\OA数据解析\\userInfo1.xlsx"
    workbook=xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_index(1)
    sheets = workbook.sheets()
    for rownum in range(sheet.nrows):
        if (rownum > 0):
            userinfo = {}

            #主键
            userinfo["rowguid"] = uuid.uuid1()

            #全名称
            fullname = sheet.cell(rownum, 0).value
            if (sheet.cell(rownum, 0).ctype == 0):
                fullname = ""
            userinfo["fullname"] = fullname

            #用户id
            uid = sheet.cell(rownum, 1).value
            if (sheet.cell(rownum, 1).ctype == 0):
                uid = ""
            userinfo["uid"] = uid

            #用户名称
            name = sheet.cell(rownum, 2).value
            userinfo["name"] = name

            #用户登录名
            loginname = sheet.cell(rownum, 3).value
            userinfo["loginname"] = loginname

            #电话
            cellphone = sheet.cell(rownum, 4).value
            userinfo["cellphone"] = cellphone

            #部门名称
            ouname = sheet.cell(rownum, 5).value
            userinfo["ouname"] = ouname

            #单位名称
            baseouname = sheet.cell(rownum, 6).value
            userinfo["baseouname"] = baseouname

            #职务
            job = sheet.cell(rownum, 7).value
            userinfo["job"] = job

            #邮件
            email = sheet.cell(rownum, 8).value
            userinfo["email"] = email
            # insertUserinfoData(userinfo)

'''
    插入审批意见信息
'''
def insertOpinionData(opinion):
    conn = getConnect()
    sql = "INSERT INTO wd24_opinion(rowguid, parentnuid, OPINIONUSER, OPINIONUSERTITLE, OpinionField, LastModifiedTime, opinionTime, " \
          "OPINIONBODY, OPINIONTYPE) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (opinion["rowguid"], opinion["parentnuid"], opinion["opinionuser"], opinion["opinionusertitle"],
             opinion["OpinionField"], opinion["LastModifiedTime"], opinion["opinionTime"],
             opinion["opinionbody"], opinion["opiniontype"])
    # print(sql)
    conn.mssql_exe_sql(sql)

'''
    审批意见
'''
def analysisWd24Opinion():
    filepath="F:\\松江OA\\OA数据解析\\wd24Opinion.xlsx"
    workbook=xlrd.open_workbook(filepath, encoding_override='utf-8')
    # sheet = workbook.sheet_by_index(1)
    # sheets = workbook.sheets()
    sheet = workbook.sheet_by_index(4)
    for rownum in range(sheet.nrows):
        if (rownum > 0):
            opinion = {}

            #主键
            opinion["rowguid"] = sheet.cell(rownum, 1).value

            #关联的附件id
            opinion["parentnuid"] = sheet.cell(rownum, 0).value

            #反馈用户id
            opinion["opinionuser"] = sheet.cell(rownum, 2).value

            #反馈用户名称
            opinion["opinionusertitle"] = sheet.cell(rownum, 3).value

            #意见步骤
            opinion["OpinionField"] = sheet.cell(rownum, 4).value

            #修改时间
            LastModifiedTime = sheet.cell(rownum, 5).value
            if (sheet.cell(rownum, 5).ctype == 3):
                date_value = xlrd.xldate_as_tuple(LastModifiedTime, workbook.datemode)
                opinion["LastModifiedTime"] = datetime.datetime(*date_value[:6]).strftime('%Y-%m-%d %H:%M:%S')
            else:
                # LastModifiedTime = LastModifiedTime.replace(' ','')
                # date_value = xlrd.xldate_as_tuple(LastModifiedTime, workbook.datemode)
                # opinion["LastModifiedTime"] = datetime.datetime(*date_value[:6]).strftime('%Y-%m-%d %H:%M:%S')
                opinion["LastModifiedTime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            #反馈时间
            opinionTime = sheet.cell(rownum, 6).value
            if (sheet.cell(rownum, 6).ctype == 3):
                date_value = xlrd.xldate_as_tuple(opinionTime, workbook.datemode)
                opinion["opinionTime"] = datetime.datetime(*date_value[:6]).strftime('%Y-%m-%d %H:%M:%S')
            else:
                # opinionTime = opinionTime.replace(' ','')
                # date_value = xlrd.xldate_as_tuple(opinionTime.replace(' ',''), workbook.datemode)
                # opinion["opinionTime"] = datetime.datetime(*date_value[:6]).strftime('%Y-%m-%d %H:%M:%S')
                opinion["opinionTime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            #反馈内容
            opinion["opinionbody"] = sheet.cell(rownum, 7).value

            #意见类型
            opinion["opiniontype"] = sheet.cell(rownum, 8).value

            # insertOpinionData(opinion)

'''
    工作流数据处理
'''
def handle_wd24_flow_test():
    conn = getConnect()
    # sql = "SELECT top 500 * FROM wd24_flow "
    sql = '''
        SELECT w1.* FROM wd24_flow w1, (
            SELECT TOP 5000 row_number() OVER (ORDER BY UUID DESC) n, UUID FROM wd24_flow
        ) w2 WHERE w1.UUID = w2.UUID AND w2.n > 4500 ORDER BY w2.n ASC 
    '''
    records = conn.mssql_findList(sql)
    counter = 1
    for record in records:
        print(record)
        wd24flow = {}
        #uuid
        unid = record[4]
        wd24flow["UUID"] = unid

        #s_flowunid
        s_flowunid = record[5]
        wd24flow["s_flowunid"] = s_flowunid

        #c_flowunid
        c_flowunid = record[6]
        wd24flow["c_flowunid"] = c_flowunid

        #步骤名称
        unitNameStr = record[0]
        unitNames = unitNameStr.split(',')

        wd24flows = []
        for i in range(len(unitNames)):
            rowguid = uuid.uuid1()
            wd24flow["rowguid"] = rowguid

            # print(rowguid)
            wd24flow["U_UnitName"] = unitNames[i]
            # U_UnitName = unitNames[i]
            #审批人名称
            unitUserTitleStr = record[1]
            unitUserTitles = unitUserTitleStr.split(',')
            wd24flow["U_UnitUserTitle"] = unitUserTitles[i]
            # U_UnitUserTitle = unitUserTitles[i]

            #审批环节类型
            U_UnitType = ""
            if unitNames[i] == "审核":
                U_UnitType = "Verify"
            elif unitNames[i] == "签发":
                U_UnitType = "Sign"
            elif unitNames[i] == "校对":
                U_UnitType = "checkMen"
            elif unitNames[i] == "退回":
                U_UnitType = "Back"
            elif unitNames[i] == "退回":
                U_UnitType = "CoSign"
            else:
                U_UnitType = ""

            wd24flow["U_UnitType"] = U_UnitType

            #审批时间
            unitEndTimeStr = record[2]
            unitEndTimes = unitEndTimeStr.split(',')
            wd24flow["U_UnitEndTime"] = unitEndTimes[i]
            # U_UnitEndTime = unitEndTimes[i]

            #接收人
            unitToTitleStr = record[3]
            unitToTitles = unitToTitleStr.split(',')
            wd24flow["U_UnitToTitle"] = unitToTitles[i]
            # U_UnitToTitle = unitToTitles[i]


            #流程动作
            unitActionStr = record[7]
            unitActions = unitActionStr.split(',')
            wd24flow["U_UnitAction"] = unitActions[i]
            # U_UnitAction = unitActions[i]

            # wd24flow = (rowguid, unid, s_flowunid, c_flowunid, U_UnitName, U_UnitUserTitle, U_UnitEndTime, U_UnitToTitle, U_UnitType, U_UnitAction)
            # print(wd24flow)
            # wd24flows.append(wd24flow)
            insertWd24flowData(wd24flow)
            print("插入记录计数器：",counter)
            counter += 1


'''
    插入审批流程信息
'''
def insertWd24flowData(wd24flow):
    conn = getConnect()
    sql = "INSERT INTO wd24_flow1_copy(rowguid,UUID, s_flowunid, c_flowunid, U_UnitName, U_UnitUserTitle, U_UnitEndTime, U_UnitToTitle, " \
          "U_UnitType, U_UnitAction) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
          % (wd24flow["rowguid"], wd24flow["UUID"], wd24flow["s_flowunid"], wd24flow["c_flowunid"],
             wd24flow["U_UnitName"], wd24flow["U_UnitUserTitle"], wd24flow["U_UnitEndTime"],
             wd24flow["U_UnitToTitle"], wd24flow["U_UnitType"], wd24flow["U_UnitAction"])
    # print(sql)
    conn.mssql_exe_sql(sql)

'''
    数据迁移,封装流程步骤对应的数据
'''
def workitemdata(wd24workflow):
    objworkitem = {}
    objworkitem['workItemGuid'] = str(uuid.uuid1())
    objworkitem['activityName'] = wd24workflow['U_UnitName']
    objworkitem['workItemName'] = ''
    objworkitem['workItemType'] = ''
    objworkitem['handleUrl'] = ''
    objworkitem['status'] = ''
    objworkitem['readDate'] = wd24workflow['U_UnitEndTime']
    objworkitem['operationDate'] = wd24workflow['U_UnitEndTime']
    objworkitem['createDate'] = wd24workflow['U_UnitEndTime']
    objworkitem['endDate'] = wd24workflow['U_UnitEndTime']
    objworkitem['opinion'] = wd24workflow['opinionbody']
    objworkitem['terminateDate'] = ''
    objworkitem['processVersionInstanceGuid'] = wd24workflow['UNID']
    objworkitem['operationType'] = ''
    objworkitem['transactorName'] = wd24workflow['U_UnitUserTitle']
    objworkitem['operatorName'] = wd24workflow['U_UnitAction']
    objworkitem['operationname'] = wd24workflow['U_UnitAction']
    objworkitem['operatorForDisplayName'] = wd24workflow['U_UnitUserTitle']
    objworkitem['senderName'] = wd24workflow['U_UnitUserTitle']
    objworkitem['note'] = ''
    return objworkitem

'''
    审批流程对应的步骤数据列表
'''
def workitemList(conn,pviguid, subject,draftdate):
    # 通过流程guid获取相关的审批步骤数据
    sql = \
        '''
            select UNID,U_UnitName,U_UnitEndTime,U_UnitUser,U_UnitUserTitle, U_UnitAction, U_UnitToTitle, opinionbody from 
                wd24_workflow_test where UNID='%s' order by U_UnitEndTime ASC
        ''' % pviguid
    # conn = getConnect()
    records = conn.mssql_findList(sql)
    workitemMap = {}
    workitemlist = []
    counter = 0
    if records and len(records) > 0:
        for coursor in records:
            # print(coursor)
            wd24workflow = {}
            if len(coursor[1]) < 2 or len(coursor[4]) < 2:
                continue
            wd24workflow['UNID'] = coursor[0]
            wd24workflow['wd25Title'] = subject
            senddate = draftdate
            if senddate:
                senddate = re.sub('[^0-9 | \/ | :]', '', senddate)
            else:
                senddate = ''
            wd24workflow['senddate'] = senddate
            wd24workflow['U_UnitName'] = coursor[1]
            U_UnitEndTime = coursor[2]
            if U_UnitEndTime:
                U_UnitEndTime = re.sub('[^0-9 | \/ | :]', '', U_UnitEndTime)
            else:
                U_UnitEndTime = ''
            wd24workflow['U_UnitEndTime'] = U_UnitEndTime
            wd24workflow['U_UnitUser'] = coursor[3]
            wd24workflow['U_UnitUserTitle'] = coursor[4]
            wd24workflow['U_UnitAction'] = coursor[5]
            U_UnitToTitleStr = coursor[6]
            if U_UnitToTitleStr:
                U_UnitToTitleStr = str(U_UnitToTitleStr).replace('等', '')
            wd24workflow['U_UnitToTitle'] = U_UnitToTitleStr
            wd24workflow['opinionbody'] = coursor[7]

            #流程步骤对应的信息处理
            workitem = workitemdata(wd24workflow)
            workitemlist.append(workitem)
            counter += 1
            print("流程步骤信息处理了 %d 条。" % counter)
    workitemMap['workitemlist'] = workitemlist
    return workitemMap

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
    return workflow

'''
    插入工作流数据
'''
def insertWorkflowData(workflowData, __conn):
    sql = \
        '''
            insert into Workflow_PVI_SD_wd24(rowguid,processVersionInstanceGuid,processVersionInstanceName,processVersionGuid,			
                initiatorname,startDate,endTime,terminateDate,status,tag,note,workitemjson,instancejson,defXml) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%d,%s,%s,%s,%s,%s)
        '''
    params = (
        workflowData['rowguid'], workflowData['processVersionInstanceGuid'], workflowData['processVersionInstanceName'], \
        workflowData['processVersionGuid'], workflowData['initiatorname'], workflowData['startDate'],
        workflowData['endTime'], \
        workflowData['terminateDate'], workflowData['status'], workflowData['tag'], workflowData['note'], \
        workflowData['workitemjson'], workflowData['instancejson'], workflowData['defXml'])
    # print(sql % params)
    return __conn.mssql_exe_sql(sql, params)

'''
    workflow数据集，构建迁移数据模型，插入数据
'''
def workflowListData():
    sql = 'SELECT distinct w1.UNID, w1.subject, w1.draftdate FROM wd24_workflow_done w1'
    __conn1 = getConnect()
    cursors = __conn1.mssql_findList(sql)
    counter = 0
    start = time.time()
    for cursor in cursors:
        # print(cursor)
        workitemlist = workitemList(__conn1, cursor[0], cursor[1], cursor[2])
        workitemListJson = json.dumps(workitemlist)
        begin = time.time()
        workflowData = workflowdata(cursor[0], cursor[1], cursor[2], workitemListJson)
        # print(workflowData)
        if (insertWorkflowData(workflowData, __conn1)):
            counter += 1
            pass
        else:
            break
        end = time.time()
        if counter % 1000 == 0:
            __conn1.commitData()
        print('工作流数据已插入：%d, 用时为：%f' % (counter, end - begin))
    over = time.time()
    __conn1.commitData()
    print('总共插入：%d, 总用时：%f' % (counter, over - start))
    __conn1.closeConn()


############################################工作流处理###################################################

'''
    工作流数据处理
'''
def handle_wd24_workflow():
    conn = getConnect()
    sql = '''
            SELECT w1.UUID, w1.U_UnitName, w1.U_UnitUser,w1.U_UnitUserTitle,
                w1.U_UnitEndTime, w1.U_UnitToTitle, w1.U_UnitAction FROM wd24_workflow w1
        '''
    records = conn.mssql_findList(sql)
    counter = 0
    exCounter = 0
    for record in records:
        # print(record)
        wd24Workflow = {}
        # uuid
        UNID = record[0]
        if not UNID:
            UNID = ''
        else:
            UNID = re.sub('[^0-9 | a-zA-Z]', '', UNID)
        wd24Workflow["UNID"] = str(UNID)

        # 步骤名称
        if record[1] is not None:
            unitNameStr = record[1]
            unitNames = unitNameStr.split(',')

            for i in range(len(unitNames)):
                rowguid = uuid.uuid1()
                wd24Workflow["rowguid"] = str(rowguid)

                # print(rowguid)
                wd24Workflow["U_UnitName"] = unitNames[i]

                # 审批人guid
                unitUserStr = record[2]
                unitUsers = unitUserStr.split(',')
                wd24Workflow["U_UnitUser"] = unitUsers[i]

                # 审批人名称
                unitUserTitleStr = record[3]
                unitUserTitles = unitUserTitleStr.split(',')
                wd24Workflow["U_UnitUserTitle"] = unitUserTitles[i]
                # U_UnitUserTitle = unitUserTitles[i]

                # 审批时间
                unitEndTimeStr = record[4]
                unitEndTimes = unitEndTimeStr.split(',')
                U_UnitEndTime = unitEndTimes[i]
                if U_UnitEndTime:
                    U_UnitEndTime = re.sub('[^0-9 | \- | : ]', '', U_UnitEndTime)
                else:
                    U_UnitEndTime = ''
                wd24Workflow["U_UnitEndTime"] = U_UnitEndTime
                # U_UnitEndTime = unitEndTimes[i]

                # 接收人
                unitToTitleStr = record[5]
                unitToTitles = unitToTitleStr.split(',')
                wd24Workflow["U_UnitToTitle"] = unitToTitles[i]
                # U_UnitToTitle = unitToTitles[i]

                # 流程动作
                unitActionStr = record[6]
                unitActions = unitActionStr.split(',')
                wd24Workflow["U_UnitAction"] = unitActions[i]

                counter += 1
                result = insertHandle24Workflow(wd24Workflow, conn)
                if result:
                    pass
                else:
                    break

                print("插入记录计数器：%d, 结果：%s" % (counter, result))
                if counter % 1000 == 0:
                    conn.commitData()
    conn.commitData()
    conn.closeConn()

'''
    解析流程办理数据
'''
def insertHandle24Workflow(wd24Workflow, conn):
    # conn = getConnect()
    sql = '''
        INSERT INTO wd24_workflow_done(UNID, U_UnitName, U_UnitUserTitle, U_UnitEndTime, U_UnitAction,
            U_UnitToTitle, U_UnitUser) VALUES(%s, %s, %s, %s, %s, %s, %s)
          '''
    params = (wd24Workflow["UNID"], wd24Workflow["U_UnitName"], wd24Workflow["U_UnitUserTitle"],
              wd24Workflow['U_UnitEndTime'],wd24Workflow["U_UnitAction"], wd24Workflow["U_UnitToTitle"], wd24Workflow["U_UnitUser"])
    # print(sql)
    try:
        conn.mssql_exe_sql(sql, params)
    except Exception as e:
        print(sql%params)
        print(e)
        return False
    return True
    # return conn.mssql_exe_sql(sql)



##################################################### 流程意见信息处理 #######################################################
'''
    流程处理信息
'''
def getWorkflow(__conn):
    __sql = '''
        SELECT UNID,U_UNITNAME,U_UnitUser,U_UnitUserTitle,U_UnitEndTime FROM wd24_workflow_done
    '''
    return __conn.mssql_findList(__sql)

'''
    添加流程处理信息
'''
def insertWorkflowHandle(workflowhandle, __conn):
    __sql = '''
        INSERT INTO archive_handle(rowguid, archiveRowguid, archiveType, processversionInstanceGuid, 
            activityName, HandleUserGuid, handleUserName, isdone, donedate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (workflowhandle['rowguid'], workflowhandle['archiveRowguid'], workflowhandle['archiveType'],
                workflowhandle['processversionInstanceGuid'], workflowhandle['activityName'], workflowhandle['HandleUserGuid'],
                workflowhandle['handleUserName'], workflowhandle['isdone'], workflowhandle['donedate'])
    # print(__sql%__params)
    return __conn.mssql_exe_sql(__sql, __params)

'''
    流程处理信息
'''
def archiveHandle():
    __conn = getConnect()
    records = getWorkflow(__conn)
    counter = 0
    for record in records:
        workflowhandle = {}
        workflowhandle['rowguid'] = str(uuid.uuid1())
        workflowhandle['archiveRowguid'] = record[0]
        workflowhandle['archiveType'] = 'WD_24'
        workflowhandle['processversionInstanceGuid'] = record[0]
        workflowhandle['activityName'] = record[1]
        workflowhandle['HandleUserGuid'] = record[2]
        workflowhandle['handleUserName'] = record[3]
        workflowhandle['isdone'] = "1"
        if record[2] == '办理完毕':
            workflowhandle['isdone'] = "1"
        doneDate = record[4]
        if doneDate:
            doneDate = re.sub('[^0-9 | \/ | :]', '', doneDate)
        else:
            doneDate = ''
        workflowhandle['donedate'] = doneDate
        if insertWorkflowHandle(workflowhandle, __conn) > 0:
            counter += 1
            print('流程处理信息已经添加：%d 条'%counter)
        if counter % 1000 == 0:
            pass
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


############################################流程意见处理#################################################
'''
    导出要处理的审批意见数据
'''


def getAllOpinions(__conn, tbl):
    sql = "SELECT ParentUnid, unid, OpinionUser,OpinionUserTitle,opiniontime,opinionbody FROM %s" % tbl
    print(sql)
    return  __conn.mssql_findList(sql)


'''
    处理数据
'''
def handleOpinion():
    __conn = getConnect()
    counter = 0
    for i in range(1, 4):
        records = getAllOpinions(__conn, "wd24_opinion"+str(i))
        for record in records:
            wd24Opinion = {}
            parentUnid = record[0]
            if not parentUnid:
                parentUnid = ''
            else:
                parentUnid = re.sub('[^0-9 | a-zA-Z]', '', parentUnid)
            wd24Opinion['parentUnid'] = parentUnid

            UNID = record[1]
            if not UNID:
                UNID = ''
            else:
                UNID = re.sub('[^0-9 | a-zA-Z]', '', UNID)
            wd24Opinion['UNID'] = UNID

            wd24Opinion['opinionUser'] = str(record[2]).replace("/SJGOV", "")
            wd24Opinion['opinionUserTitle'] = record[3]
            opinionTime = record[4]
            if not opinionTime:
                opinionTime = ''
            else:
                opinionTime = re.sub('[^0-9 | \/ | :]', '', opinionTime)
            wd24Opinion['opinionTime'] = opinionTime

            wd24Opinion['opinionbody'] = record[5]

            if insertOpinion(wd24Opinion, __conn):
                counter += 1
                print('已经插入数据：%d 条。' % counter)
                if counter % 1000 == 0:
                    __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


'''
    插入流程意见信息
'''


def insertOpinion(wd24Opinion, __conn):
    sql = '''
        INSERT INTO wd24_opinions(ParentUnid, UNID, OpinionUser, OpinionUserTitle, opinionTime, opinionbody) 
        VALUES(%s, %s, %s, %s, %s, %s)
    '''
    params = (
        wd24Opinion['parentUnid'], wd24Opinion['UNID'], wd24Opinion['opinionUser'], wd24Opinion['opinionUserTitle'],
        wd24Opinion['opinionTime'], wd24Opinion['opinionbody'])
    return __conn.mssql_exe_sql(sql, params)


'''
    ###########################################处理步骤和意见的对应关系#############################
'''
#获取流程步骤信息
def getWorkflow(__conn, unid):
    __sql = '''
        SELECT UNID, U_UnitName, U_UnitUser, U_UnitUserTitle, U_UnitEndTime, U_UnitAction, U_UnitToTitle 
            FROM wd24_workflow_done WHERE unid = '%s' 
    ''' % unid

    return __conn.mssql_findList(__sql)

#获取流程步骤审批意见信息
def getWorkflowOpinion(__conn, unid):
    __sql = '''
        SELECT opinionuser, opiniontime, OpinionBody FROM wd24_opinions WHERE parentunid = '%s'
    '''% unid
    return __conn.mssql_findList(__sql)

#处理流程步骤和意见信息
def handleWorkflowAndOpinion():
    __conn = getConnect()
    __sql = "SELECT DISTINCT unid FROM wd24_workflow_done"
    unidRecords = __conn.mssql_findList(__sql)
    counter = 0
    for unidRecord in unidRecords:
        workflows = getWorkflow(__conn, unidRecord[0])
        opinions = getWorkflowOpinion(__conn, unidRecord[0])
        preUnittime = ''
        for workflow in workflows:
            #流程步骤信息
            workflowitem = {}
            workflowitem['UNID'] = workflow[0]
            workflowitem['U_UnitName'] = workflow[1]
            workflowitem['U_UnitUser'] = workflow[2]
            workflowitem['U_UnitUserTitle'] = workflow[3]
            workflowitem['U_UnitEndTime'] = workflow[4]
            workflowitem['U_UnitAction'] = workflow[5]
            workflowitem['U_UnitToTitle'] = workflow[6]
            unituser = workflow[2]
            unituser = str(unituser).replace("/SJGOV", "")
            unittime = workflow[4]
            opinionbody = ''
            #将时间转为数字（例：201801011012），作为比较
            if unittime:
                unittime = re.sub('[^0-9]', '', unittime)[:-2]
            if opinions:
                for opinion in opinions:
                    opinionuser = opinion[0]
                    opiniontime = str(opinion[1])
                    if opiniontime:
                        opiniontime = re.sub('[^0-9]', '', opiniontime)[:-2]
                    #流程步骤人和意见反馈人相同，则再判断时间
                    if unituser == opinionuser:
                        if opiniontime == unittime:
                            opinionbody = opinion[2]
                            # print("opinionBody1:", opinion[2])
                        elif len(preUnittime) > 0 and opiniontime < unittime and opiniontime > preUnittime:
                            opinionbody = opinion[2]
                            # print("opinionBody2:", opinion[2])
            workflowitem['opinionBody'] = opinionbody
            preUnittime = unittime
            if insertWorkflowItem(__conn, workflowitem):
                counter += 1
                print("已插入：%d 条数据。"% counter)
            if counter % 1000 == 0:
                __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

#插入分析后的工作流数据
def insertWorkflowItem(__conn, workflowitem):
    __sql = '''
        INSERT INTO wd24_workflow_test(UNID, U_UnitName, U_UnitUser, U_UnitEndTime, U_UnitAction, U_UnitToTitle, 
            opinionBody, U_UnitUserTitle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (workflowitem['UNID'], workflowitem['U_UnitName'], workflowitem['U_UnitUser'], workflowitem['U_UnitEndTime'],
              workflowitem['U_UnitAction'], workflowitem['U_UnitToTitle'], workflowitem['opinionBody'],
              workflowitem['U_UnitUserTitle'])
    try:
        result = __conn.mssql_exe_sql(__sql, params)
    except Exception as e:
        print(__sql % params)
        print(e)
    return result

if __name__ == "__main__":
    #analysisXsl()
    #analysisUser_info()
    #analusisWd24Opinion()
    # handle_wd24_flow_test()
    workflowListData()
    # handle_wd24_workflow()
    # handleOpinion()
    # archiveHandle()
    # handleWorkflowAndOpinion()