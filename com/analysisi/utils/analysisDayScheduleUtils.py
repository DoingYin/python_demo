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
    解析日程信息
'''
def analysisDayScheduleCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    head_row = next(csvFile)
    # print(head_row)
    __conn = getConnect_old()
    counter = 0
    for row in csvFile:
        if len(row) != 32:
            continue
        schedule = {}
        # print(row)
        userguid = row[0]
        userguid = str(userguid).replace("CN=", "").replace("O=", "")
        userguid = Utils.getInitUserGuid(userguid, __conn)
        schedule['userguid'] = userguid
        # if not userguid:
        #     print(leader, row[0])
        #     return
        year = row[1]
        schedule['year'] = year
        week = row[2]
        schedule['weekflag'] = re.sub('[^0-9]', "", week)
        leader = row[3]
        schedule['leader'] = leader
        #周一至周日的数据
        for i in range(1, 8):
            # print(i)
            #一周一天的数据
            schedule['RowGuid'] = str(uuid.uuid1())
            day1 = row[4*i]
            if len(day1) < 1:
                continue
            daytime = Utils.formatStrToTime(day1)
            schedule['scheduletime'] = Utils.fromatTimeToStr(daytime, '%Y-%m-%d')
            weekday1 = row[4*i+1]
            schedule['weekday'] = weekday1
            amcontent1 = row[4*i+2]
            schedule['amcontent'] = amcontent1
            pmcontent1 = row[4*i+3]
            schedule['pmcontent'] = pmcontent1
            if insertDaySchedule(__conn, schedule):
                counter += 1
            print("插入日程数据：%d 条。"%counter)
            if counter % 1000 == 0:
                __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

'''
    插入日程信息
'''
def insertDaySchedule(__conn, schedule):
    sql = '''
        INSERT INTO sj_personal_schedule(RowGuid, YearFlag, userid, weekflag, scheduletime, amcontent, pmcontent, imported) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %d)
    '''
    params = (schedule['RowGuid'], schedule['year'], schedule['userguid'], schedule['weekflag'],
              schedule['scheduletime'], schedule['amcontent'], schedule['pmcontent'], 1)
    # print(sql%params)
    return __conn.mssql_exe_sql(sql, params)