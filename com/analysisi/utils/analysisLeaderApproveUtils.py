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
