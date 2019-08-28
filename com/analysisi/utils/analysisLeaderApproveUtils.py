#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import re
import uuid

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

'''
    解析领导批示件相关数据
'''
def analysisLeaderCsv(fileName):
    if fileName.find('signInfo') != -1:
        analysisApproveSignInfoCsv(fileName)
        pass
    else:
        analysisLeaderApproveCsv(fileName)
        pass


'''
    解析领导批示件csv文件
'''
def analysisLeaderApproveCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 19:
            continue
        comments = {}
        rowguid = row[0]
        comments['Rowguid'] = str(uuid.uuid1())
        comments['pviguid'] = rowguid
        comments['doctitle'] = row[1]
        comments['replytitle'] = row[2]
        comments['commentguid'] = row[3]
        comments['commentsubguid'] = row[4]
        comments['method'] = row[5]
        filingdateStr = row[6]
        if filingdateStr:
            filingdate = Utils.formatStrToTime(filingdateStr)
        if filingdate:
            filingdateStr = Utils.fromatTimeToStr(filingdate, '%Y-%m-%d')
        else:
            filingdateStr = None
        comments['filingdate'] = filingdateStr
        finishdateStr = row[7]
        if finishdateStr:
            finishdate = Utils.formatStrToTime(finishdateStr)
        if finishdate:
            finishdateStr = Utils.fromatTimeToStr(finishdate, '%Y-%m-%d')
        else:
            finishdateStr = None
        comments['finishdate'] = finishdateStr
        comments['commentleader'] = row[8]
        commentdateStr = row[9]
        if finishdateStr:
            finishdate = Utils.formatStrToTime(commentdateStr)
        if finishdate:
            commentdateStr = Utils.fromatTimeToStr(finishdate, '%Y-%m-%d')
        else:
            commentdateStr = None
        comments['commentdate'] = commentdateStr
        comments['urgency'] = row[10]
        comments['securitylevel'] = row[11]
        comments['fromdept'] = row[12]
        comments['hostdept'] = row[13]
        comments['assistantdept'] = row[14]
        comments['opinion'] = row[15]
        userguid = row[16]
        userguid = str(userguid).replace("CN=", "").replace("O=", "")
        userguid = Utils.getInitUserGuid(userguid, __conn)
        comments['SignUserGuid'] = userguid
        comments['SignUserName'] = row[17]
        comments['AddUserBaseouguid'] = Utils.getBaseOuGuid(userguid, __conn)
        signDateStr = row[18]
        if signDateStr:
            signDate = Utils.formatStrToTime(signDateStr)
        if signDate:
            signDateStr = Utils.fromatTimeToStr(signDate, '%Y-%m-%d')
        else:
            signDateStr = None
        comments['OperateDate'] = signDateStr
        comments['status'] = '已提交'
        comments['imported'] = 1
        if insertComments(__conn, comments):
            counter += 1
        print("插入日程数据：%d 条。"%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


'''
    插入数据
'''
def insertComments(__conn, comments):
    __sql = '''
        INSERT INTO SJ_COMMENTS (RowGuid, pviguid, doctitle, replytitle, commentguid, commentsubguid, method, 
        filingdate, finishdate, commentleader, commentdate, urgency, securitylevel, fromdept, hostdept, 
        assistantdept, opinion, signerguid, SignerName, AddUserBaseouguid, OperateDate, status, imported) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (comments['Rowguid'], comments['pviguid'], comments['doctitle'], comments['replytitle'],
                comments['commentguid'], comments['commentsubguid'], comments['method'],
                comments['filingdate'], comments['finishdate'], comments['commentleader'],
                comments['commentdate'], comments['urgency'], comments['securitylevel'],
                comments['fromdept'], comments['hostdept'], comments['assistantdept'],
                comments['opinion'], comments['SignUserGuid'], comments['SignUserName'],
                comments['AddUserBaseouguid'], comments['OperateDate'], comments['status'],
                comments['imported'])
    # print(__sql % __params)
    return  __conn.mssql_exe_sql(__sql, __params)


'''
    解析领导批示件签收情况信息
'''
def analysisApproveSignInfoCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) < 7:
            continue
        signInfo = {}
        signInfo['mainUnid'] = row[0]
        signInfo['unid'] = row[1]
        signInfo['unit'] = row[2]
        signInfo['unitId'] = row[3]
        signInfo['user'] = row[4]
        signInfo['userTitle'] = row[5]
        signInfo['time'] = row[6]
        # print(signInfo)
        if insertSignInfo(__conn, signInfo):
            counter += 1
            print("插入日程数据：%d 条。"%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入签收数据
'''
def insertSignInfo(__conn, signInfo):
    __sql = '''
        INSERT INTO comments_signinfo (MAINUNID, UNID, Unit, UNITID, [user], USERTITLE, [TIME]) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (signInfo['mainUnid'], signInfo['unid'], signInfo['unit'], signInfo['unitId'],
                signInfo['user'], signInfo['userTitle'], signInfo['time'])
    print(__sql % __params)
    return  __conn.mssql_exe_sql(__sql, __params)

'''
    获取未处理的签收数据
'''
def getAllSignInfo(__conn):
    __sql = 'SELECT c.mainunid, c.UNID, c.Unit, c.UNITID, c.[TIME] FROM comments_signInfo c'
    return __conn.mssql_findList(__sql)

'''
    处理签收情况
'''
def handleSignInfo():
    __conn = getConnect_old()
    records = getAllSignInfo(__conn)
    counter = 0
    for records in records:
        signInfo = {}
        signInfo['MAINUNID'] = records[0]
        signInfo['UNID'] = records[1]
        unitStr = records[2]
        if unitStr:
            units = str(unitStr).split(',')
            for i in range(len(units)):
                signInfo['Unit'] = units[i]

                unitIdStr = records[3]
                if not unitIdStr or unitIdStr == '':
                    continue
                unitIds = str(unitIdStr).split(',')
                if i < len(unitIds):
                    signInfo['UNITID'] = unitIds[i]

                # userStr = records[4]
                # if not userStr or userStr == '':
                #     continue
                # users = str(userStr).split(',')
                # if i < len(users):
                #     signInfo['User'] = users[i]
                #
                # userTitleStr = records[5]
                # if not userTitleStr or userTitleStr == '':
                #     continue
                # userTitles = str(userTitleStr).split(',')
                # if i < len(userTitles):
                #     signInfo['USERTITLE'] = userTitles[i]

                timeStr = records[4]
                if not timeStr or timeStr == '':
                    continue
                times = str(timeStr).split(',')
                if i < len(times):
                    timeStr = times[i]
                    time1 = Utils.formatStrToTime(timeStr)
                    timeStr = Utils.fromatTimeToStr(time1, '%Y-%m-%d %H:%M:%S')
                    signInfo['TIME'] = timeStr
                if insertSignInfoDone(__conn, signInfo):
                    counter += 1
                    print("插入签收记录数据：%d 条。"%counter)
                if counter % 1000 == 0:
                    __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入处理后的数据
'''
def insertSignInfoDone(__conn, signInfo):
    __sql = '''
        INSERT INTO comments_signinfo_done (MAINUNID, UNID, Unit, UNITID, TIME) 
        VALUES (%s, %s, %s, %s, %s)
    '''
    __params = (signInfo['MAINUNID'], signInfo['UNID'], signInfo['Unit'], signInfo['UNITID'], signInfo['TIME'])
    # print(__sql % __params)
    return  __conn.mssql_exe_sql(__sql, __params)


'''
    获取发送的单位数据
'''
def getSendDept(__conn):
    __sql = "SELECT pviguid, hostdept, assistantdept FROM SJ_COMMENTS"
    return __conn.mssql_findList(__sql)

'''
    获取单位签收数据
'''
def getDeptSignInfo(__conn, pviguid, deptName):
    __sql = "SELECT mainunid,unid,unit,time,UNITID FROM comments_signInfo_done WHERE mainunid='%s' AND unit = '%s'" \
            % (pviguid, deptName)
    # print(__sql)
    return __conn.mssql_findList(__sql)

'''
    处理单位签收数据
'''
def handleSignInfo_done():
    __conn = getConnect_old()
    records1 = getSendDept(__conn)
    counter = 0
    for record1 in records1:
        pviguid = record1[0]
        deptStr = str(record1[1]) + ',' + str(record1[2])
        depts = str(deptStr).split(',')
        for dept in depts:
            if dept and len(dept) > 1:
                record = getDeptSignInfo(__conn, pviguid, dept)
                signInfo = {}
                signInfo['MAINUNID'] = pviguid
                signInfo['Unit'] = dept
                # print(record)
                if record and len(record) > 0:
                    signInfo['UNID'] = record[0][1]
                    signInfo['TIME'] = record[0][3]
                    signInfo['UNITID'] = record[0][4]
                else:
                    signInfo['UNID'] = str(uuid.uuid1())
                    signInfo['TIME'] = None
                    signInfo['UNITID'] = None
                if insertSignInfoDone_c(__conn, signInfo):
                    counter += 1
                    print("插入签收记录数据：%d 条。"%counter)
                if counter % 1000 == 0:
                    __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入处理后的数据
'''
def insertSignInfoDone_c(__conn, signInfo):
    __sql = '''
        INSERT INTO comments_signinfo_done_copy (MAINUNID, UNID, Unit, UNITID, TIME) 
        VALUES (%s, %s, %s, %s, %s)
    '''
    __params = (signInfo['MAINUNID'], signInfo['UNID'], signInfo['Unit'], signInfo['UNITID'], signInfo['TIME'])
    # print(__sql % __params)
    return  __conn.mssql_exe_sql(__sql, __params)


######################################### 处理单位签收反馈情况 ########################################
'''
    获取单位签收数据
'''
def getDeptSignInfo_done(__conn):
    __sql = "SELECT MAINUNID, UNID, Unit, UNITID, TIME FROM comments_signInfo_done_copy"
    return __conn.mssql_findList(__sql)

'''
    获取单位反馈数据
'''
def getDeptFeedback(__conn, mainUnid, unitId):
    __sql = '''
        SELECT UNID, FeedBackBody FROM unitFeedback 
            WHERE mainUnid = '%s' AND feedbackUnitId = '%s'
    ''' % (mainUnid, unitId)
    return __conn.mssql_findList(__sql)

'''
    处理签收反馈数据
'''
def handleSignFeedback():
    __conn = getConnect_old()
    signRecords = getDeptSignInfo_done(__conn)
    counter = 0
    for signRecord in signRecords:
        signFeedback = {}
        parentId = signRecord[0]
        signFeedback['parentId'] = parentId
        signFeedback['deptName'] = signRecord[2]
        deptId = signRecord[3]
        signFeedback['signDate'] = signRecord[4]
        feedbackRecord = getDeptFeedback(__conn, parentId, deptId)
        if feedbackRecord:
            signFeedback['rowguid'] = feedbackRecord[0][0]
            signFeedback['feedbackcontent'] = feedbackRecord[0][1]
        else:
            signFeedback['rowguid'] = signRecord[1]
            signFeedback['feedbackcontent'] = None

        if insertSignFeedback(__conn, signFeedback):
            counter += 1
            print("插入签收反馈记录数据：%d 条。"%counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


def insertSignFeedback(__conn, signFeedback):
    __sql = '''
        INSERT INTO comments_signAndFeedback(rowguid, parentGuid, deptName, signDate, feedbackContent)
        VALUES (%s, %s, %s, %s, %s)
    '''
    __params = (signFeedback['rowguid'], signFeedback['parentId'], signFeedback['deptName'],
                signFeedback['signDate'], signFeedback['feedbackcontent'])
    return __conn.mssql_exe_sql(__sql, __params)


if __name__ == '__main__':
    handleSignInfo_done()
    # handleSignFeedback()