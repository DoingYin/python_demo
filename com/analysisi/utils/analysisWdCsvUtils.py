#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import csv
import uuid
import re
import time
import json

from com.database.ConnectDataBase import ConnectionDatabase
from com.analysisi.utils import Utils

######################################## 数据库连接 ####################################
'''
    数据库连接
'''
def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn

def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa9History")
    return __conn

############################################ 发文数据 ###############################
'''
    解析发文数据
'''
def analysisWd24Csv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 34:
            continue;
        wd24 = {}
        wd24['RowGuid'] = str(uuid.uuid1())
        wd24['ProcessVersionInstanceGuid'] = row[0]
        # print(row[0])
        wd24['pviguid'] = row[0]
        txttitle = row[1]
        if not txttitle:
            continue
        else:
            txttitle = re.sub('[\']{1,5}', "”", txttitle)
        wd24['txttitle'] = txttitle
        wd24['FaWenFileNumber'] = row[2]
        wd24['JpdFawenYear'] = re.sub('[^0-9]','', row[3])
        wd24['TxtFileNumber'] = re.sub('[^0-9]','', row[4])
        wd24['Ouname'] = row[5]
        sendfiledate = Utils.formatStrToTime(row[6])
        if sendfiledate:
            sendfiledate = Utils.fromatTimeToStr(sendfiledate, "%Y-%m-%d %H:%M:%S")
        wd24['sendfiledate'] = sendfiledate
        wd24['InitUserDisplayName'] = row[7]
        wd24['JpdMiji'] = row[8]
        wd24['secrecyTime'] = row[9]
        wd24['jpdhuanji'] = row[10]
        wd24['sanctionsTime'] = row[11]
        wd24['phone'] = row[12]
        wd24['secrecyExaminer'] = row[13]
        wd24['lawExaminer'] = row[14]
        wd24['categorynum'] = row[15]
        wd24['identfyFile'] = row[16]
        wd24['genresType'] = row[17]
        wd24['rulesFile'] = row[18]
        wd24['partyMixInfo'] = row[19]
        wd24['policyFiles'] = row[20]
        wd24['commonAttr'] = row[21]
        wd24['noPublicReason'] = row[22]
        wd24['drafttype'] = row[23]
        wd24['txtzhusong'] = row[24]
        wd24['txtchaosong'] = row[25]
        wd24['theme'] = row[26]
        wd24['sendFileType'] = row[27]
        wd24['pdfawendz'] = row[28]
        wd24['bark'] = row[29]
        relatedLink = row[30]
        if relatedLink and relatedLink != '':
            relatedLink = Utils.handleRelateLink(relatedLink)
        wd24['relatedLink'] = relatedLink
        C_CreateUser = row[31]
        C_CreateUser = Utils.getInitUserGuid(C_CreateUser, __conn)
        wd24["InitUserGuid"] = C_CreateUser
        wd24['JpdGongWenZhongLei'] = row[32]
        wd24['searchLevel'] = row[33]
        wd24['printNum'] = row[34]
        wd24['SubWebFlowOuGuid'] = Utils.getSubWebFlowOuGuid('workflows_done', row[0], __conn)
        wd24['imported'] = 1
        wd24['DelFlag'] = 0

        if insertWd24(__conn, wd24) > 0:
            counter += 1
        if counter % 1000 == 0:
            __conn.commitData()
    print("发文数据已经插入：%d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()

'''
    插入发文数据
'''
def insertWd24(__conn, wd24):
    __sql = '''
        INSERT INTO wd_24(
            RowGuid,txttitle,FaWenFileNumber,JpdFawenYear,TxtFileNumber,Ouname,sendfiledate,
            InitUserDisplayName,JpdMiji,secrecyTime,jpdhuanji,sanctionsTime,phone,secrecyExaminer,
            lawExaminer,categorynum,identfyFile,genresType,rulesFile,partyMixInfo,policyFiles,
            commonAttr,noPublicReason,txtzhusong,txtchaosong,theme,sendFileType,JpdFawendz,relatedLink,bark, imported,
            ProcessVersionInstanceGuid, pviguid, InitUserGuid, SubWebFlowOuGuid, DelFlag, JpdGongWenZhongLei, searchLevel,
            printNum, drafttype
            ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s)
    '''
    __params = (wd24['RowGuid'], wd24['txttitle'], wd24['FaWenFileNumber'], wd24['JpdFawenYear'], wd24['TxtFileNumber'],
                wd24['Ouname'], wd24['sendfiledate'], wd24['InitUserDisplayName'], wd24['JpdMiji'], wd24['secrecyTime'],
                wd24['jpdhuanji'], wd24['sanctionsTime'], wd24['phone'], wd24['secrecyExaminer'], wd24['lawExaminer'],
                wd24['categorynum'], wd24['identfyFile'], wd24['genresType'], wd24['rulesFile'], wd24['partyMixInfo'],
                wd24['policyFiles'], wd24['commonAttr'], wd24['noPublicReason'], wd24['txtzhusong'], wd24['txtchaosong'],
                wd24['theme'], wd24['sendFileType'], wd24['pdfawendz'], wd24['relatedLink'], wd24['bark'], wd24['imported'],
                wd24['ProcessVersionInstanceGuid'], wd24['pviguid'], wd24['InitUserGuid'], wd24['SubWebFlowOuGuid'],
                wd24['DelFlag'], wd24['JpdGongWenZhongLei'], wd24['searchLevel'], wd24['printNum'], wd24['drafttype'])
    # print(__sql % __params)
    # print(wd24)
    return __conn.mssql_exe_sql(__sql, __params)

#################################################### 收文数据 ######################################

'''
    解析收文数据
'''
def analysisWd25Csv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        # print(row)
        wd25 = {}
        wd25['RowGuid'] = str(uuid.uuid1())
        wd25['ProcessVersionInstanceGuid'] = row[0]
        txttitle = row[1]
        if txttitle:
            txttitle = re.sub('[\']{1,5}', "”", txttitle)
        else:
            continue
        wd25['TxtTitle'] = txttitle
        wd25['txtlaiwenhao'] = row[2]
        wd25['ShouWenFileNumber'] = row[3]
        wd25['replyTitle'] = row[4]
        wd25['flowNum'] = row[5]
        wd25['fileCode'] = row[6]
        wd25['txtlaiwendept'] = row[7]
        wd25['fileStyle'] = row[8]
        wd25['initUserDisplayName'] = row[9]
        wd25['jinji'] = row[10]
        wd25['jpdMiji'] = row[11]
        wd25['Arch_Type'] = row[12]
        saveTimeStr = row[13]
        #将时间字符串转为时间
        # if saveTimeStr == '短期':
        #     pass
        # elif saveTimeStr and str(saveTimeStr).strip() != '':
        #     saveTimeStr = Utils.formatStrToTime(saveTimeStr)
        #     if saveTimeStr:
        #         saveTimeStr = Utils.fromatTimeToStr(saveTimeStr, "%Y-%m-%d %H:%M:%S")
        # else:
        #     saveTimeStr = None
        wd25['saveTime'] = saveTimeStr

        wd25['searchLevel'] = row[14]
        wd25['clearFileType'] = row[15]
        txtFileDateStr = row[16]
        #将时间字符串转为时间
        if txtFileDateStr and txtFileDateStr != '':
            txtFileDateStr = Utils.formatStrToTime(txtFileDateStr)
            if txtFileDateStr:
                txtFileDateStr = Utils.fromatTimeToStr(txtFileDateStr, "%Y-%m-%d %H:%M:%S")
        else:
            txtFileDateStr = None
        wd25['TxtFileDate'] = txtFileDateStr

        txtShouWenDateStr = row[17]
        #将时间字符串转为时间
        if txtShouWenDateStr and txtShouWenDateStr != '':
            txtShouWenDateStr = Utils.formatStrToTime(txtShouWenDateStr)
            if txtShouWenDateStr:
                txtShouWenDateStr = Utils.fromatTimeToStr(txtShouWenDateStr, "%Y-%m-%d %H:%M:%S")
        else:
            txtShouWenDateStr = None
        wd25['TxtShouWenDate'] = txtShouWenDateStr

        wd25['txtzhuban'] = row[18]
        banjieDateStr = row[19]
        #将时间字符串转为时间
        if banjieDateStr and str(banjieDateStr).strip() != '':
            banjieDateStr = Utils.formatStrToTime(banjieDateStr)
            if banjieDateStr:
                banjieDateStr = Utils.fromatTimeToStr(banjieDateStr, "%Y-%m-%d %H:%M:%S")
        else:
            banjieDateStr = None
        wd25['banjieDate'] = banjieDateStr

        overTimeStr = row[20]
        #将时间字符串转为时间
        if overTimeStr and str(overTimeStr).strip() != '':
            overTimeStr = Utils.formatStrToTime(overTimeStr)
            if overTimeStr:
                overTimeStr = Utils.fromatTimeToStr(overTimeStr, "%Y-%m-%d %H:%M:%S")
        else:
            overTimeStr = None
        wd25['overTime'] = overTimeStr
        wd25['isQuit'] = row[21]
        wd25['attach'] = row[22]
        wd25['bark'] = row[23]
        wd25['Ouname'] = row[24]
        wd25['imported'] = 1
        wd25['DelFlag'] = 0
        C_CreateUser = Utils.getInitUserGuid(row[25], __conn)
        wd25['InitUserGuid'] = C_CreateUser
        wd25['SubWebFlowOuGuid'] = Utils.getSubWebFlowOuGuid('workflows_done', row[0], __conn)
        if insertWd25(__conn, wd25):
            counter += 1
        if counter % 1000 == 0:
            __conn.commitData()
        print("收文数据已经插入：%d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()

'''
    插入收文数据
'''
def insertWd25(__conn, wd25):
    __sql = '''
        INSERT INTO WD_25(
            RowGuid,ProcessVersionInstanceGuid,TxtTitle,txtlaiwenhao,ShouWenFileNumber,replyTitle,flowNum,fileCode,
            txtlaiwendept,fileStyle,initUserDisplayName,jinji,jpdMiji,Arch_Type,saveTime,searchLevel,clearFileType,
            TxtFileDate,SignReceiveDate,txtzhuban,banjieDate,overTime,isQuit,attach,bark,imported,Ouname,InitUserGuid,
            SubWebFlowOuGuid,DelFlag
        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    __params = (
        wd25['RowGuid'], wd25['ProcessVersionInstanceGuid'], wd25['TxtTitle'], wd25['txtlaiwenhao'],
        wd25['ShouWenFileNumber'], wd25['replyTitle'], wd25['flowNum'], wd25['fileCode'], wd25['txtlaiwendept'],
        wd25['fileStyle'], wd25['initUserDisplayName'], wd25['jinji'], wd25['jpdMiji'], wd25['Arch_Type'],
        wd25['saveTime'], wd25['searchLevel'], wd25['clearFileType'], wd25['TxtFileDate'], wd25['TxtShouWenDate'],
        wd25['txtzhuban'], wd25['banjieDate'], wd25['overTime'], wd25['isQuit'], wd25['attach'],
        wd25['bark'], wd25['imported'], wd25['Ouname'], wd25['InitUserGuid'], wd25['SubWebFlowOuGuid'],
        wd25['DelFlag']
    )
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)


################################################# 解析工作流程数据 #################################

'''
    解析文件
'''
def analysisWorkflowCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        workflow = {}
        workflow['﻿﻿UUID'] = row[0]
        subject = row[1]
        if subject:
            subject = re.sub('[\']{1,5}', "”", subject)
        workflow['subject'] = subject
        workflow['signdate'] = row[2]
        workflow['U_UnitName'] = row[3]
        workflow['U_UnitUser'] = row[4]
        workflow['U_UnitUserTitle'] = row[5]
        workflow['U_UnitEndTime'] = row[6]
        workflow['U_UnitAction'] = row[7]
        workflow['U_UnitToTitle'] = row[8]
        if insertWorkflows(__conn, workflow):
            counter += 1
        if counter % 1000 == 0:
            __conn.commitData()
    print("已经插入工作流数据： %d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()

'''
    插入工作流程数据
'''
def insertWorkflows(__conn, workflow):
    __sql = '''
        INSERT INTO workflows (
            UUID, U_UnitName, U_UnitUser, U_UnitUserTitle, U_UnitEndTime, U_UnitAction, U_UnitToTitle, subject, signdate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (
        workflow['﻿﻿UUID'], workflow['U_UnitName'], workflow['U_UnitUser'], workflow['U_UnitUserTitle'],
        workflow['U_UnitEndTime'], workflow['U_UnitAction'], workflow['U_UnitToTitle'], workflow['subject'],
        workflow['signdate']
    )
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)


'''
    工作流数据解析处理
'''
def handle_workflow():
    conn = getConnect_old()
    sql = '''
            SELECT w1.UUID, w1.subject, w1.SignDate, w1.U_UnitName, w1.U_UnitUser, w1.U_UnitUserTitle, 
                w1.U_UnitEndTime, w1.U_UnitToTitle, w1.U_UnitAction FROM workflows w1
        '''
    records = conn.mssql_findList(sql)
    counter = 0
    for record in records:
        # print(record)
        Workflow = {}
        # uuid
        UNID = record[0]
        if not UNID:
            UNID = ''
        else:
            UNID = re.sub('[^0-9 | a-zA-Z]', '', UNID)
        Workflow["UNID"] = str(UNID)

        # subject
        subject = record[1]
        Workflow["subject"] = subject

        # signdate
        SignDate = record[2]
        if SignDate:
            SignDate = re.sub('[^0-9 | \/ | :]', '', SignDate)
        else:
            SignDate = ''
        Workflow["SignDate"] = SignDate

        # 步骤名称
        unitNameStr = record[3]
        if unitNameStr is not None:
            unitNames = unitNameStr.split(',')
            for i in range(len(unitNames)):
                rowguid = uuid.uuid1()
                Workflow["rowguid"] = str(rowguid)

                # print(rowguid)
                Workflow["U_UnitName"] = unitNames[i]
                # U_UnitName = unitNames[i]

                # 审批人guid
                unitUserStr = record[4]
                unitUsers = unitUserStr.split(',')
                Workflow["U_UnitUser"] = unitUsers[i]

                # 审批人名称
                unitUserTitleStr = record[5]
                unitUserTitles = unitUserTitleStr.split(',')
                if len(unitUserTitles) < len(unitNames):
                    continue
                Workflow["U_UnitUserTitle"] = unitUserTitles[i]

                # 审批时间
                unitEndTimeStr = record[6]
                unitEndTimes = unitEndTimeStr.split(',')
                U_UnitEndTime = None
                if len(unitEndTimes) < len(unitNames):
                    continue
                U_UnitEndTime = unitEndTimes[i]
                if U_UnitEndTime:
                    U_UnitEndTime = re.sub('[^0-9 | \- | : ]', '', U_UnitEndTime)
                else:
                    U_UnitEndTime = ''
                Workflow["U_UnitEndTime"] = U_UnitEndTime

                # 接收人
                unitToTitleStr = record[7]
                unitToTitles = unitToTitleStr.split(',')
                U_UnitToTitle = None
                if len(unitToTitles) < len(unitNames):
                    continue
                U_UnitToTitle = unitToTitles[i]
                Workflow["U_UnitToTitle"] = U_UnitToTitle

                # 流程动作
                unitActionStr = record[8]
                unitActions = unitActionStr.split(',')
                U_UnitAction = None
                if len(unitActions) < len(unitNames):
                    continue
                U_UnitAction = unitActions[i]
                Workflow["U_UnitAction"] = U_UnitAction

                counter += 1
                result = insertWorkflows_done(Workflow, conn)
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
    插入审批流程解析后的数据
'''
def insertWorkflows_done(workflow, __conn):
    sql = '''
        INSERT INTO workflows_done(rowguid, UUID, subject, SignDate, U_UnitName,
            U_UnitUser,U_UnitUserTitle, U_UnitEndTime, U_UnitToTitle, U_UnitAction) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          '''
    params = (workflow["rowguid"], workflow["UNID"], workflow["subject"], workflow["SignDate"],
              workflow["U_UnitName"], workflow["U_UnitUser"], workflow["U_UnitUserTitle"],
              workflow["U_UnitEndTime"], workflow["U_UnitToTitle"], workflow["U_UnitAction"])
    try:
        __conn.mssql_exe_sql(sql, params)
    except Exception as e:
        print(sql % params)
        print(e)
        return False
    return True
    # return conn.mssql_exe_sql(sql)

################################################## 解析意见信息 ###########################################

'''
    解析意见信息
'''
def analysisOpinionCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        # print(row)
        if len(row) < 6:
            continue
        opinion = {}
        opinion['parentunid'] = row[0]
        opinion['UNID'] = row[1]
        opinion['OPINIONUSER'] = Utils.getUserGuid(row[2])
        opinion['OPINIONUSERTITLE'] = row[3]
        opinionTime = Utils.formatStrToTime(row[4])
        if opinionTime:
            opinionTimeStr = Utils.fromatTimeToStr(opinionTime, '%Y-%m-%d %H:%M')
        else:
            continue
        opinion['opinionTime'] = opinionTimeStr
        opinion['OPINIONBODY'] = row[5]
        feedbackunid = None
        if len(row) > 6:
            feedbackunid = row[6]

        opinion['feedbackunid'] = feedbackunid
        if insertOpinion(__conn, opinion):
            counter += 1
        if counter % 1000 == 0:
            __conn.commitData()
    print("已经插入意见信息： %d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()

'''
    插入意见信息
'''
def insertOpinion(__conn, opinion):
    __sql = '''
        INSERT INTO opinions (
            parentunid, OPINIONUSER, OPINIONUSERTITLE, opinionTime, OPINIONBODY, UNID, feedbackunid
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (
        opinion['parentunid'], opinion['OPINIONUSER'], opinion['OPINIONUSERTITLE'], opinion['opinionTime'],
        opinion['OPINIONBODY'], opinion['UNID'], opinion['feedbackunid']
    )
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

################################################### 通知信息 ############################################

'''
    解析通知信息
'''
def analysisNoticeCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        notice = {}
        notice['UNID'] = row[0]
        notice['subject'] = row[1]
        notice['Content'] = row[2]
        notice['RegDate'] = row[3]
        notice['ShowDate'] = row[4]
        notice['Location'] = row[5]
        notice['AttendPeopleTitle'] = row[6]
        notice['AttendPeople'] = row[7]
        notice['ChairmanTitle'] = row[8]
        notice['NoticeUnit'] = row[9]
        notice['NoticeUnitName'] = row[10]
        notice['NoticePeople'] = row[11]
        notice['NoticePeopleTitle'] = row[12]
        notice['isSendSMS'] = row[13]
        notice['IsFeedBackGX'] = row[14]
        notice['SMSContent'] = row[15]
        notice['CreateUser'] = row[16]
        notice['CreatePeople'] = row[17]
        notice['CreateDate'] = row[18]
        notice['DocWord'] = row[19]
        # print(notice)
        if insertNotice(__conn, notice):
            counter += 1
        if counter % 1000 == 0:
            __conn.commitData()
        # print(row)
    print("通知数据总数：%d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()

'''
    插入通知信息
'''
def insertNotice(__conn, notice):
    __sql = '''
        INSERT INTO notice (
            UNID, subject, Content, RegDate, ShowDate, Location, AttendPeopleTitle, AttendPeople, 
            ChairmanTitle, NoticeUnit, NoticeUnitName, NoticePeople, NoticePeopleTitle, isSendSMS, 
            IsFeedBackGX, SMSContent, createUser, CreatePeople, CreateDate, DocWord
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (
        notice['UNID'], notice['subject'], notice['Content'], notice['RegDate'], notice['ShowDate'], notice['Location'],
        notice['AttendPeopleTitle'], notice['AttendPeople'], notice['ChairmanTitle'], notice['NoticeUnit'],
        notice['NoticeUnitName'], notice['NoticePeople'], notice['NoticePeopleTitle'], notice['isSendSMS'],
        notice['IsFeedBackGX'], notice['SMSContent'], notice['CreateUser'], notice['CreatePeople'],
        notice['CreateDate'], notice['DocWord']
    )
    # print(notice)
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

####################################################### 通知反馈信息 #####################################

'''
    解析通知反馈信息
'''
def analysisNoticeFeedbackCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 11:
            continue
        feedback = {}
        feedback['ParentUnid'] = row[0]
        feedback['FeedbackUserID'] = row[1]
        feedback['FeedbackUnitTitle'] = row[2]
        feedback['FeedbackPeople'] = row[3]
        feedback['FeedbackUnitTitle1'] = row[4]
        feedback['FeedbackUnit'] = row[5]
        feedback['FeedBackTime'] = row[6]
        feedback['FeedbackBody'] = row[7]
        feedback['FeedBackType'] = row[8]
        feedback['AttendPeopleTitle'] = row[9]
        feedback['isAttend'] = row[10]
        if insertNoticeFeedback(__conn, feedback):
            counter += 1
    print("通知反馈数据总数：%d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()


'''
    插入通知反馈信息
'''
def insertNoticeFeedback(__conn, feedback):
    __sql = '''
        INSERT INTO feedback (
            ParentUnid, FeedbackUserID, FeedbackUnitTitle, FeedbackPeople, FeedbackUnitTitle1, FeedbackUnit, 
            FeedBackTime, FeedbackBody, FeedBackType, AttendPeopleTitle, isAttend
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (
        feedback['ParentUnid'], feedback['FeedbackUserID'], feedback['FeedbackUnitTitle'], feedback['FeedbackPeople'],
        feedback['FeedbackUnitTitle1'], feedback['FeedbackUnit'], feedback['FeedBackTime'], feedback['FeedbackBody'],
        feedback['FeedBackType'], feedback['AttendPeopleTitle'], feedback['isAttend']
    )
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)


'''
    ###########################################处理步骤和意见的对应关系#############################
'''
#获取流程步骤信息
def getWorkflow(__conn, unid):
    __sql = '''
        SELECT UUID, U_UnitName, U_UnitUser, U_UnitUserTitle, U_UnitEndTime, U_UnitAction, U_UnitToTitle 
            FROM workflows_done WHERE UUID = '%s' 
    ''' % unid

    return __conn.mssql_findList(__sql)

#获取流程步骤审批意见信息
def getWorkflowOpinion(__conn, unid):
    __sql = '''
        SELECT opinionuser, opiniontime, OpinionBody FROM opinions WHERE parentunid = '%s'
    '''% unid
    return __conn.mssql_findList(__sql)

#处理流程步骤和意见信息
def handleWorkflowAndOpinion():
    __conn = getConnect_old()
    __sql = "SELECT DISTINCT UUID FROM workflows"
    unidRecords = __conn.mssql_findList(__sql)
    counter = 0
    for unidRecord in unidRecords:
        workflows = getWorkflow(__conn, unidRecord[0])
        opinions = getWorkflowOpinion(__conn, unidRecord[0])
        unituser = ''
        opinionuser = ''
        preUnittime = ''
        workflowLen = 0
        opinionLen = 0
        if opinions:
            opinionLen = len(opinions)
        if workflows:
            workflowLen = len(workflows)
            matchCounter = 0
            for workflow in workflows:
                #流程步骤信息
                workflowitem = {}
                workflowitem['UUID'] = workflow[0]
                workflowitem['U_UnitName'] = workflow[1]
                workflowitem['U_UnitUser'] = workflow[2]
                workflowitem['U_UnitUserTitle'] = workflow[3]
                workflowitem['U_UnitEndTime'] = workflow[4]
                workflowitem['U_UnitAction'] = workflow[5]
                workflowitem['U_UnitToTitle'] = workflow[6]
                unituser = workflow[2]
                unituser = re.sub("[^0-9]", "", str(unituser))
                unittime = workflow[4]
                opinionbody = ''
                #将时间转为数字（例：201801011012），作为比较
                if unittime:
                    unittime = re.sub('[^0-9]', '', unittime)[:-2]
                if opinions:
                    for opinion in opinions:
                        opinionuser = opinion[0]
                        opinionuser = re.sub("[^0-9]", "", opinionuser)
                        opiniontime = opinion[1]
                        if opiniontime:
                            opiniontime = re.sub('[^0-9]', '', str(opiniontime))[:-2]
                        #先判断处理人在步骤中出现的次数，如果只出现一次则采用人对比, 否则通过时间判断
                        if getCount(unituser, workflows) == 1:
                            if unituser == opinionuser:
                                opinionbody = opinion[2]
                        else:
                            #流程步骤人和意见反馈人相同，则再判断时间
                            if unituser == opinionuser:
                                if opiniontime == unittime:
                                    opinionbody = opinion[2]
                                    # print("opinionBody1:", opinion[2])
                                elif len(preUnittime) > 0 and opiniontime < unittime and opiniontime > preUnittime:
                                    opinionbody = opinion[2]
                                    # print("opinionBody2:", opinion[2])
                if opinionbody != '':
                    matchCounter += 1
                workflowitem['opinionBody'] = opinionbody
                preUnittime = unittime
                if insertWorkflowItem(__conn, workflowitem):
                    counter += 1
                    print("已插入：%d 条数据。"% counter)
                if counter % 1000 == 0:
                    __conn.commitData()
                    # return
            # print(unidRecord[0])
            # print("当前流程记录数据： %d"%workflowLen)
            # print("当前流程意见数据： %d"%opinionLen)
            # print("匹配成功： %d 条。"% matchCounter)
    __conn.commitData()
    __conn.closeConn()

'''
    获取元素在数组中的个数
'''
def getCount(userguid, records):
    counter = 0
    for record in records:
        userunid = re.sub("[^0-9]", "", str(record[2]))
        if userguid == userunid:
            counter += 1
    return counter

'''
    插入分析后的工作流数据
'''
def insertWorkflowItem(__conn, workflowitem):
    __sql = '''
        INSERT INTO workflow_opinion(UUID, U_UnitName, U_UnitUser, U_UnitEndTime, U_UnitAction, U_UnitToTitle, 
            opinionBody, U_UnitUserTitle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (workflowitem['UUID'], workflowitem['U_UnitName'], workflowitem['U_UnitUser'], workflowitem['U_UnitEndTime'],
              workflowitem['U_UnitAction'], workflowitem['U_UnitToTitle'], workflowitem['opinionBody'],
              workflowitem['U_UnitUserTitle'])
    try:
        result = __conn.mssql_exe_sql(__sql, params)
    except Exception as e:
        print(__sql % params)
        print(e)
    return result


################################################ 流程步骤意见信息封装处理（workflow_pvi_sd）#############################
'''
    构建流程信息数据模型
'''
def handleWorkflowListData(note):
    sql = 'SELECT w1.UUID, w1.subject, w1.signdate FROM workflows w1'
    __conn = getConnect_old()
    cursors = __conn.mssql_findList(sql)
    counter = 0
    for cursor in cursors:
        subject = cursor[1]
        if subject:
            subject = re.sub('[\']{1,5}', "”", subject)
        else:
            continue
        if cursor[2]:
            signDate = str(cursor[2]).split(",")[0]
        else:
            signDate = None
        # print(cursor)
        workitemlist = workitemList(__conn, cursor[0], subject, signDate)
        workitemListJson = json.dumps(workitemlist)
        begin = time.time()
        workflowData = workflowdata(cursor[0], subject, signDate, workitemListJson, note)
        # print(workflowData)
        if (insertWorkflowData(workflowData, __conn)):
            counter += 1
            pass
        else:
            break
        end = time.time()
        if counter % 1000 == 0:
            __conn.commitData()
        print('工作流数据已插入：%d, 用时为：%f' % (counter, end - begin))
    __conn.commitData()
    __conn.closeConn()

'''
    审批流程对应的步骤数据列表
'''
def workitemList(conn,pviguid, subject,SignDate):
    # 通过流程guid获取相关的审批步骤数据
    sql = \
        '''
            select UUID,U_UnitName,U_UnitEndTime,U_UnitUser,U_UnitUserTitle, U_UnitAction, U_UnitToTitle, opinionbody 
                from workflow_opinion where UUID='%s' order by U_UnitEndTime ASC
        ''' % pviguid
    # conn = getConnect()
    records = conn.mssql_findList(sql)
    workitemMap = {}
    workitemlist = []
    counter = 0
    if records and len(records) > 0:
        for coursor in records:
            # print(coursor)
            workflow = {}
            if len(coursor[1]) < 2 or len(coursor[4]) < 2:
                continue
            workflow['UNID'] = coursor[0]
            workflow['wd25Title'] = subject
            senddate = SignDate
            if senddate:
                senddate = re.sub('[^0-9 | \/ | : | -]', '', senddate)
            else:
                senddate = ''
            workflow['senddate'] = senddate
            workflow['U_UnitName'] = coursor[1]
            U_UnitEndTime = coursor[2]
            if U_UnitEndTime:
                U_UnitEndTime = re.sub('[^0-9 | \/ | : | -]', '', U_UnitEndTime)
            else:
                U_UnitEndTime = ''
            workflow['U_UnitEndTime'] = U_UnitEndTime
            workflow['U_UnitUser'] = coursor[3]
            workflow['U_UnitUserTitle'] = coursor[4]
            workflow['U_UnitAction'] = coursor[5]
            U_UnitToTitleStr = coursor[6]
            if U_UnitToTitleStr:
                U_UnitToTitleStr = str(U_UnitToTitleStr).replace('等', '')
            workflow['U_UnitToTitle'] = U_UnitToTitleStr
            workflow['opinionbody'] = coursor[7]

            #流程步骤对应的信息处理
            workitem = workitemdata(workflow)
            workitemlist.append(workitem)
            counter += 1
            print("流程步骤信息处理了 %d 条。" % counter)
    workitemMap['workitemlist'] = workitemlist
    return workitemMap

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
    objworkitem['senderName'] = workflow['U_UnitUserTitle']
    objworkitem['note'] = ''
    return objworkitem

'''
    workflow对应的一条数据模型
'''
def workflowdata(pviguid, title, senddate, workitemListJson, note):
    # print(pviguid)
    if senddate and senddate != "":
        senddate = Utils.formatStrToTime(senddate)
        if senddate:
            senddate = Utils.fromatTimeToStr(senddate, "%Y-%m-%d")
        else:
            senddate = None
    else:
        senddate = None
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
    workflow['note'] = note
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
            insert into Workflow_PVI_SD(rowguid,processVersionInstanceGuid,processVersionInstanceName,processVersionGuid,			
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