#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import re

'''
    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.
'''

#将时间字符串转为时间
def formatStrToTime(timeStr):
    if len(timeStr) < 8:
        return None
    timeStr = str(timeStr).replace("/", "-")
    timeStr = re.sub('[^0-9|\/|:|\-| ]', '', timeStr)
    if len(timeStr) < 8:
        return None
    regStr = None
    # print(len(timeStr))
    if len(timeStr) <= 10:
        regStr = "%Y-%m-%d"
    elif len(timeStr) <= 16:
        regStr = "%Y-%m-%d %H:%M"
    else:
        regStr = "%Y-%m-%d %H:%M:%S"
    newtime = time.strptime(str(timeStr), regStr)
    return newtime


'''
    时间转时间字符串
'''
def fromatTimeToStr(oldtime, timeReg):
    return time.strftime(timeReg, oldtime)

'''
    根据用户名称获取用户guid
'''
def getInitUserGuid(initUserName, __conn):
    __sql = "SELECT frame_userguid FROM user_info WHERE fullname = '%s'" % initUserName
    result = __conn.mssql_findList(__sql)
    if result and len(result) >= 1:
        return result[0][0]
    else:
        return None

'''
    提取用户的guid
'''
def getUserGuid(userGuidStr):
    return re.sub("[^U\d{1,5}]", "", userGuidStr)

'''
    获取部门guid
'''
def getBaseOuGuid(initUserGuid, __conn):
    __sql = '''
        SELECT baseouguid FROM Frame_OU WHERE ouguid = (
            SELECT ouguid FROM Frame_User WHERE userguid = '%s'
        )
    ''' %initUserGuid
    result = __conn.mssql_findList(__sql)
    if result and len(result) >= 1:
        return result[0][0]
    else:
        return None

'''
    根据部门名称获取部门guid
'''
def getInitDeptGuid(initDeptName, __conn):
    __sql = "SELECT ouguid FROM frame_ou WHERE ouname = '%s'" % initDeptName
    result = __conn.mssql_findList(__sql)
    if result and len(result) == 1:
        return result[0][0]
    elif len(result) > 1:
        return 1
    else:
        return 2

'''
    获取自流转部门guid
'''
def getSubWebFlowOuGuid(tablename, unid, __conn):
    sql = "SELECT u_unituser FROM %s WHERE uuid= '%s'"%(tablename, unid)
    records = __conn.mssql_findList(sql)
    if not records:
        # print(sql)
        return None
    subwebFlowOuGuid = None
    for record in records:
        # print(record)
        userguid = getInitUserGuid(record, __conn)
        # print(userguid)
        if not userguid:
            continue
        subwebFlowOuGuid = getBaseOuGuid(userguid, __conn)
        # print(subwebFlowOuGuid)
        if subwebFlowOuGuid:
            break
    return subwebFlowOuGuid

'''
    处理相关链接
'''
def handleRelateLink(relateLinStr):
    pattern = re.compile('[0-9|a-z|A-Z]{30,50}')
    matchStr = pattern.search(relateLinStr)
    if matchStr and matchStr.group():
        relateLinkUnid = matchStr.group()
    else:
        return None
    relateLink = 'href="../../../../../oa9/archive/forms/wd25/wd25imported?ProcessVersionInstanceGuid=%s"'%relateLinkUnid
    return re.sub('href=.*openDocument', relateLink, relateLinStr)

'''
    正则表达式获取字符串
'''
def getStrByReg(oldStr, reg):
    pattern = re.compile(reg)
    if pattern.findall(oldStr):
        return pattern.findall(oldStr)
    else:
        return None



if __name__ == "__main__":
    # formatStrToTime('2018/7/25 17:30')
    linkStr = '<a href=/egov\Receival.nsf/0/C32D77BD14A4512C4825841C0023C56D?openDocument target=_blank>关于批准松江区2018年第42批次建设项目被征地人员落实就业和社会保障方案的请示</a><br>'
    print(handleRelateLink(linkStr))