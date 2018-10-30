# 导入 pymysql
import pymysql
import pymssql

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
        if not cursor:
            raise (NameError,"数据库连接失败")
        try:
            # 执行SQL语句
            cursor.execute(MsSQL_sql)
            # 获取所有记录列表
            results = cursor.fetchall()
        except Exception:
            print("Error: unable to fetch data")
            print(Exception)
            self.MsSQL_db.close()
        self.MsSQL_db.close()
        return results

    # 数据增删改查（sqlserver）
    def mssql_exe_sql(self, sql):
        cursor = self.MsSQL_db.cursor()
        MsSQL_sql = sql
        if not cursor:
            raise (NameError,"数据库连接失败")
        try:
            # 执行SQL语句
            cursor.execute(MsSQL_sql)
            self.MsSQL_db.commit()
        except Exception:
            print("Error: unable to fetch data")
            print(Exception)
            self.MsSQL_db.close()
        self.MsSQL_db.close()



