#!/usr/bin/python
# -*- coding: UTF-8 -*-
import uuid
import re
from com.analysisi.utils import Utils
from com.database.ConnectDataBase import ConnectionDatabase

'''
    数据库连接
'''
def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn

def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa9History")
    return __conn

def getConnect_oa_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn

'''
    获取要处理的通知数据
'''
def getNoticeData(__conn):
    __sql = '''
        SELECT UNID,subject,Content,regDate,ShowDate,Location,AttendPeopleTitle,
            ChairmanTitle,NoticeUnit,NoticeUnitName,
            NoticePeople,NoticePeopleTitle,isSendSMS,isFeedBackGX,SMSContent,createuser,
            createPeople,CreateDate,docword FROM notice
    '''
    return __conn.mssql_findList(__sql)

'''
    处理通知数据
'''
def handleMeetingSend():
    __conn = getConnect_old()
    __conn_oa = getConnect_oa_old()
    noticeRecords = getNoticeData(__conn)
    counter = 0
    for record in noticeRecords:
        meetingSend = {}
        meetingSend['RowGuid'] = record[0]
        meetingSend['MeetingName'] = record[1]
        meetingSend['Maincontent'] = record[2]
        MeetingDate = record[3]
        if MeetingDate:
            MeetingDate = Utils.formatStrToTime(MeetingDate)
            if MeetingDate:
                MeetingDate = Utils.fromatTimeToStr(MeetingDate, "%Y-%m-%d %H:%M:%S")
        else:
            MeetingDate = None
        meetingSend['MeetingDate'] = MeetingDate
        MeetingEndDate = record[4]
        if MeetingEndDate:
            MeetingEndDate = Utils.formatStrToTime(MeetingEndDate)
            if MeetingEndDate:
                MeetingEndDate = Utils.fromatTimeToStr(MeetingEndDate, "%Y-%m-%d %H:%M:%S")
        else:
            MeetingEndDate = None
        meetingSend['MeetingEndDate'] = MeetingEndDate
        meetingSend['MeetingPlace'] = record[5]
        meetingSend['AttendanceLeader'] = record[6]
        meetingSend['Hoster'] = record[7]
        meetingSend['ReceiveOuGuids'] = record[8]
        meetingSend['ReceiveOuNames'] = record[9]
        meetingSend['ReceiveUserGuids'] = record[10]
        meetingSend['ReceiveUserNames'] = record[11]
        meetingSend['SMSNotice'] = record[12]
        meetingSend['Backlognotice'] = record[13]
        meetingSend['feedback'] = record[13]
        meetingSend['msgcontent'] = record[14]
        meetingSend['SendUserGuid'] = getFrame_userguid(__conn_oa, record[15])
        meetingSend['SendUserName'] = record[16]
        operatedate = record[17]
        if operatedate:
            operatedate = Utils.formatStrToTime(operatedate)
            if operatedate:
                operatedate = Utils.fromatTimeToStr(operatedate, "%Y-%m-%d %H:%M:%S")
        else:
            operatedate = None
        meetingSend['operatedate'] = operatedate

        #通知类型
        docWord = record[18]
        draft = "1"
        if docWord and docWord != "" and docWord == "常务会议":
            draft = "0"
        meetingSend['Draft'] = draft
        meetingSend['imported'] = "1"
        #是否是督查通知，默认（0）：不是
        meetingSend['issupervisor'] = "0"
        meetingSend['sendState'] = "1"
        if insertMeetingSend(__conn, meetingSend):
            counter += 1
            print("数据已经插入：%d 条。"%counter)
        # print(record)
        # print(meetingSend)
        # return
        # pass
    print(counter)
    __conn.commitData()
    __conn.closeConn()
    __conn_oa.closeConn()

'''
    插入会议通知信息
'''
def insertMeetingSend(__conn, meetingSend):
    __sql = '''
        INSERT INTO OA_MEETINGSEND (
            RowGuid, MeetingName, Maincontent, MeetingDate, MeetingEndDate, MeetingPlace, AttendanceLeader, 
            Hoster, ReceiveOuGuids, ReceiveOuNames, ReceiveUserGuids, ReceiveUserNames, SMSNotice, BacklogNotice,
            msgcontent, SendUserGuid, SendUserName,operatedate, draft, imported, issupervisor, sendState, feedback) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (
        meetingSend['RowGuid'], meetingSend['MeetingName'], meetingSend['Maincontent'], meetingSend['MeetingDate'],
        meetingSend['MeetingEndDate'], meetingSend['MeetingPlace'], meetingSend['AttendanceLeader'], meetingSend['Hoster'],
        meetingSend['ReceiveOuGuids'], meetingSend['ReceiveOuNames'], meetingSend['ReceiveUserGuids'],
        meetingSend['ReceiveUserNames'], meetingSend['SMSNotice'], meetingSend['Backlognotice'], meetingSend['msgcontent'],
        meetingSend['SendUserGuid'], meetingSend['SendUserName'], meetingSend['operatedate'], meetingSend['Draft'],
        meetingSend['imported'], meetingSend['issupervisor'], meetingSend['sendState'], meetingSend['feedback']
    )
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

'''
    获取通知接收信息
'''
def getMeetingReceive(__conn):
    __sql = '''
        SELECT RowGuid,MeetingName,ReceiveOuGuids,ReceiveOuNames,ReceiveUserGuids,SendUserGuid,ReceiveUserNames,
            SendUserName,MeetingDate,MeetingEndDate, draft, isSupervisor
        FROM OA_MEETINGSEND 
    '''
    # WHERE DATALENGTH(ReceiveUserGuids) > 1
    return __conn.mssql_findList(__sql)

#通过用户guid获取部门guid
def getFrame_OuGuid(__conn, userguid):
    __sql = '''
        SELECT ouguid FROM frame_user where userguid = '%s'
    '''%userguid
    records = __conn.mssql_findList(__sql)
    result = userguid
    if records:
        result = records[0]
    return result

#获取框架用户guid
def getFrame_userguid(__conn, userid):
    if userid:
        matchObj = re.search('U[0-9]{2,5}', userid)
        if matchObj:
            userid = matchObj.group()
    __sql = '''
        SELECT frame_userguid FROM user_info WHERE uid='%s'
    '''%userid
    # print(__sql)
    records = __conn.mssql_findList(__sql)
    result = None
    if records:
        result = records[0]
    return result

'''
    获取老系统对应的部门guid
'''
def getOuGuid(__conn, ouid):
    __sql = '''
        SELECT ouguid FROM dept_ou where unitguid = '%s'
    '''%ouid
    records = __conn.mssql_findList(__sql)
    result = None
    if records:
        result = records[0]
    return result

'''
    处理通知信息
'''
def handleMeetingReceive():
    __conn = getConnect_old()
    __conn_oa = getConnect_oa_old()
    records = getMeetingReceive(__conn)
    counter = 0
    for record in records:
        meetingReceive = {}

        meetingReceive['RowGuid'] = str(uuid.uuid1())
        meetingReceive['MeetingGuid'] = record[0]
        meetingReceive['MeetingName'] = record[1]
        receiveOuGuids = record[2]
        receiveOuNames = record[3]
        receiveUserGuids = record[4]
        receiveUserNames = record[6]
        SendUserGuid = record[5]
        meetingReceive['SendUserGuid'] = SendUserGuid
        SendUserName = record[7]
        meetingReceive['SendUserName'] = SendUserName
        meetingReceive['MeetingDate'] = record[8]
        meetingReceive['MeetingEndDate'] = record[9]
        meetingReceive['SignState'] = 1
        meetingReceive['SignDate'] = record[8]
        meetingReceive['cancel'] = 0
        meetingReceive['imported'] = 1
        #默认不是区委督查
        meetingReceive['draft'] = record[10]
        meetingReceive['issupervisor'] = record[11]
        #接收部门为空则为接收人
        if receiveOuGuids and len(receiveOuGuids) > 0:
            noticetype = "ou"
            receiveOuGuids = str(receiveOuGuids).split(",")
            receiveOuNames =  str(receiveOuNames).split(",")
            for i in range(0, len(receiveOuGuids)):
                meetingReceive['NoticeType'] = noticetype
                meetingReceive['OuName'] = receiveOuNames[i]
                OuGuid = receiveOuGuids[i]
                meetingReceive['OuGuid'] = getFrame_OuGuid(__conn_oa, OuGuid)
                ReceiverGuid = None
                ReceiverName = None
                if receiveUserGuids and len(receiveUserGuids) > 0:
                    receiveUserNameStr = str(receiveUserNames).split(",")
                    receiveUserGuidStr = str(receiveUserGuids).split(",")
                    if i < len(receiveUserGuidStr):
                        ReceiverGuid = receiveUserGuidStr[i]
                        if getFrame_userguid(__conn_oa, ReceiverGuid):
                            ReceiverGuid = getFrame_userguid(__conn_oa, ReceiverGuid)

                    if i < len(receiveUserNameStr):
                        ReceiverName = receiveUserNameStr[i]
                        if ReceiverName:
                            matchObj = re.search('[\u4e00-\u9fa5]{2,3}', ReceiverName)
                            if matchObj:
                                ReceiverName = matchObj.group()
                if not ReceiverGuid:
                    continue
                meetingReceive['ReceiverGuid'] = ReceiverGuid
                meetingReceive['ReceiverName'] = ReceiverName
                meetingReceive['OuGuid'] = OuGuid
                if insertMeetingReceive(__conn, meetingReceive):
                    counter += 1
                    print("已经插入接收数据： %d 条。"%counter)
                if counter % 2000 == 0:
                    __conn.commitData()
        elif receiveUserGuids and len(receiveUserGuids) > 0:
            meetingReceive['OuGuid'] = None
            meetingReceive['OuName'] = None
            noticetype = "user"
            meetingReceive['NoticeType'] = noticetype
            receiveUserGuidStr = str(receiveUserGuids).split(",")
            receiveUserNames = str(receiveUserNames).split(",")
            for i in range(0, len(receiveUserGuidStr)):
                receiveUserGuid = receiveUserGuidStr[i]
                receiveUserGuid = getFrame_userguid(__conn_oa, receiveUserGuid)
                receiveUserName = receiveUserNames[i]
                if receiveUserName:
                    matchObj = re.search('[\u4e00-\u9fa5]{2,3}', receiveUserName)
                    if matchObj:
                        receiveUserName = matchObj.group()
                meetingReceive['ReceiverGuid'] = receiveUserGuid
                meetingReceive['ReceiverName'] = receiveUserName
                if insertMeetingReceive(__conn, meetingReceive):
                    counter += 1
                    print("已经插入接收数据： %d 条。"%counter)
                if counter % 2000 == 0:
                    __conn.commitData()
        else:
            continue
    __conn.commitData()
    __conn.closeConn()
    __conn_oa.closeConn()


'''
    插入接收数据
'''
def insertMeetingReceive(__conn, meetingReceive):
    __sql = '''
        INSERT INTO OA_MEETINGRECEIVE (RowGuid, MeetingGuid, ReceiverGuid, ReceiverName, OuGuid, OuName, NoticeType, 
            SendUserGuid, SendUserName, SignState, SignDate, MeetingName, MeetingDate, cancel, imported, draft, 
            issupervisor) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (
        meetingReceive['RowGuid'], meetingReceive['MeetingGuid'], meetingReceive['ReceiverGuid'],
        meetingReceive['ReceiverName'], meetingReceive['OuGuid'], meetingReceive['OuName'], meetingReceive['NoticeType'],
        meetingReceive['SendUserGuid'], meetingReceive['SendUserName'], meetingReceive['SignState'],
        meetingReceive['SignDate'], meetingReceive['MeetingName'], meetingReceive['MeetingDate'],
        meetingReceive['cancel'], meetingReceive['imported'], meetingReceive['draft'], meetingReceive['issupervisor']
    )
    # print(__sql % __params)
    return __conn.mssql_exe_sql(__sql, __params)

####################################################反馈信息处理##################################################
'''
    通知反馈信息处理
'''
def getFeedbacks(__conn):
    __sql = '''
        SELECT ParentUnid, FeedbackUserId, FeedbackPeople, 
        FeedbackTime, FeedbackBody FROM feedback
    '''
    # , FeedBackType,AttendPeopleTitle,isAttend
    return __conn.mssql_findList(__sql)

def handleFeedback():
    __conn = getConnect_old()
    __conn_oa = getConnect_oa_old()
    records = getFeedbacks(__conn)
    counter = 0
    for record in records:
        feedback = {}
        feedback['RowGuid'] = str(uuid.uuid1())
        feedback['MeetingGuid'] = record[0]
        feedbackerGuid = record[1]
        if getFrame_userguid(__conn_oa, feedbackerGuid):
            feedbackerGuid = getFrame_userguid(__conn_oa, feedbackerGuid)
        feedback['FeedBackUserGuid'] = feedbackerGuid
        feedback['FeedBackUserName'] = record[2]
        FeedBackDate = record[3]
        FeedBackDate = Utils.formatStrToTime(FeedBackDate)
        if FeedBackDate:
            FeedBackDate = Utils.fromatTimeToStr(FeedBackDate, "%Y-%m-%d %H:%M:%S")
        feedback['FeedBackDate'] = FeedBackDate
        feedback['FeedBackContent'] = record[4]
        feedback['imported'] = 1
        if insertFeedback(__conn, feedback):
            counter += 1
            print("已经插入反馈数据： %d 条。"%counter)
    __conn.commitData()
    __conn.closeConn()

'''
    插入数据
'''
def insertFeedback(__conn, feedback):
    __sql = '''
        INSERT INTO OA_MEETINGFEEDBACK (
                RowGuid, FeedBackUserGuid, FeedBackUserName, MeetingGuid, FeedBackContent, FeedBackDate, imported
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (feedback['RowGuid'], feedback['FeedBackUserGuid'], feedback['FeedBackUserName'], feedback['MeetingGuid'],
                feedback['FeedBackContent'], feedback['FeedBackDate'], feedback['imported'])
    return __conn.mssql_exe_sql(__sql, __params)


if __name__ == "__main__":
    handleMeetingSend()
    # handleMeetingReceive()
    # handleFeedback()