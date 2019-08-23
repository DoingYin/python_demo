#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入 pymysql
import os
import pymysql
import pymssql

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

'''
数据库连接
'''
class ConnectionDatabase(object):
    # 连接mysql数据库
    def __init__(self, ip, user_name, passwd, db, char='utf8'):
        self.ip = ip
        # self.port = port
        self.username = user_name
        self.passwd = passwd
        self.mysqldb = db
        self.char = char

        # self.MySQL_db = pymysql.connect(
        #     host=self.ip,
        #     user=self.username,
        #     passwd=self.passwd,
        #     db=self.mysqldb,
        #     port=3306,
        #     charset=self.char)

        self.MsSQL_db = pymssql.connect(
            host=self.ip,
            user=self.username,
            password=self.passwd,
            database=self.mysqldb,
            charset=self.char)
    # 查询数据（mysql）
    # def mysql_findList(self, sql):
    #     cursor = self.MySQL_db.cursor()
    #     MySQL_sql = sql
    #     if not cursor:
    #         raise (NameError,"数据库连接失败")
    #     try:
    #         # 执行SQL语句
    #         cursor.execute(MySQL_sql)
    #         # 获取所有记录列表
    #         results = cursor.fetchall()
    #     except Exception:
    #         print("Error: unable to fetch data")
    #         print(Exception)
    #         self.MySQL_db.close()
    #     self.MySQL_db.close()
    #     return results
    #
    # # 数据增删改查（mysql）
    # def mysql_exe_sql(self, sql):
    #     cursor = self.MySQL_db.cursor()
    #     MySQL_sql = sql
    #     if not cursor:
    #         raise (NameError,"数据库连接失败")
    #     try:
    #         # 执行SQL语句
    #         cursor.execute(MySQL_sql)
    #         self.MySQL_db.commit()
    #     except Exception:
    #         print("Error: unable to fetch data")
    #         print(Exception)
    #         self.MySQL_db.close()
    #     self.MySQL_db.close()

    # 查询数据（sqlserver）
    def mssql_findList(self, sql):
        cursor = self.MsSQL_db.cursor()
        MsSQL_sql = sql
        results = None
        if not cursor:
            raise (NameError,"数据库连接失败")
        try:
            # 执行SQL语句
            cursor.execute(MsSQL_sql)
            # 获取所有记录列表
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            self.MsSQL_db.close()
        if results:
            return results
        else:
            return None

    # 数据增删改查（sqlserver）
    def mssql_exe_sql(self, sql, params):
        cursor = self.MsSQL_db.cursor()
        MsSQL_sql = sql
        result = 0
        if not cursor:
            raise (NameError,"数据库连接失败")
        try:
            # 执行SQL语句
            cursor.execute(MsSQL_sql, params)
            result = cursor.rowcount
        except Exception as e:
            print(e)
            self.MsSQL_db.rollback()
            self.MsSQL_db.close()

        return result>0

    # 数据增删改查（sqlserver）
    def mssql_exemany_sql(self, sql, values):
        cursor = self.MsSQL_db.cursor()
        MsSQL_sql = sql
        if not cursor:
            raise (NameError,"数据库连接失败")
        try:
            # 执行SQL语句
            cursor.executemany(MsSQL_sql, values)
            result = cursor.rowcount
        except Exception as e:
            print(e)
            self.MsSQL_db.rollback()
            self.MsSQL_db.close()
        return result>0

    '''
        提交数据集
    '''
    def commitData(self):
        try:
            self.MsSQL_db.commit()
        except Exception as e:
            print(e)

    '''
        关闭数据库连接
    '''
    def closeConn(self):
        if self.MsSQL_db:
            self.MsSQL_db.close()


if __name__ == "__main__":

    param = (('193c56a6-fc1c-11e8-a409-a81e84aff407', '07FDAFB44C3FCBFA48257F46000CD549', '4837AACE48CB820748257F4600212945', '07479B81E1F4963248257BA6002CF36D'), ('193c56a7-fc1c-11e8-b16b-a81e84aff407', '07FDAFB44C3FCBFA48257F46000CD549', '4837AACE48CB820748257F4600212945', '07479B81E1F4963248257BA6002CF36D'))
    sql = "INSERT INTO test(rowguid,UUID, s_flowunid, c_flowunid) VALUES(%s, %s, %s, %s)"
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    __conn.mssql_exemany_sql(sql, param)



