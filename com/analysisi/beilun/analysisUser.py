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
    插入用户数据
'''
def insertUser(__conn, user):
    __sql = '''
        INSERT INTO frame_user(UserGuid, LoginID, password, OUGuid, DisplayName, 
            IsEnabled, sex, publicopinion)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (user['UserGuid'], user['LoginID'], user['password'], user['OUGuid'],
              user['DisplayName'], user['IsEnabled'], user['sex'], user['publicopinion'])
    # 执行sql语句
    try:
        effect = __conn.mssql_exe_sql(__sql, params)
    except Exception as e:
        print(e)
        print(__sql%params)
    return effect


def getUser(__conn):
    __sql = "SELECT lastname, shortname FROM bl_user"
    return __conn.mssql_findList(__sql)

'''
    解析文件数据
'''
def analysisUserCsv():
    __conn = getConnect_old()
    # __conn1 = getConnect_new()
    userRecords = getUser(__conn)
    counter = 0
    for record in userRecords:
        user = {}
        user['UserGuid'] = str(uuid.uuid1())
        user['LoginID'] = record[1]
        user['password'] = '7B21848AC9AF35BE0DDB2D6B9FC3851934DB8420'
        user['OUGuid'] = '252d664b-f7f3-4447-a5cb-9eb8dd1561a6'
        user['DisplayName'] = record[0]
        user['sex'] = '男'
        user['IsEnabled'] = 1
        user['publicopinion'] = 1
        if insertUser(__conn, user):
            counter += 1

        if counter % 1000 == 0:
            __conn.commitData()

    __conn.commitData()
    # __conn1.closeConn()
    __conn.closeConn()

if __name__ == "__main__":
    analysisUserCsv()