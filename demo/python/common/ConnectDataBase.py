# 导入 pymysql
import pymysql

'''
数据库连接
'''
class ConnectionMyslq(object):
    def __init__(self, ip, user_name, passwd, db, port, char='utf8'):
        self.ip = ip
        self.port = port
        self.username = user_name
        self.passwd = passwd
        self.mysqldb = db
        self.char = char

        self.MySQL_db = pymysql.connect(
            host=self.ip,
            user=self.username,
            passwd=self.passwd,
            db=self.mysqldb,
            port=self.port,
            charset=self.char)

    # 查询数据
    def findList(self, sql):
        cursor = self.MySQL_db.cursor()
        MySQL_sql = sql
        try:
            # 执行SQL语句
            cursor.execute(MySQL_sql)
            # 获取所有记录列表
            results = cursor.fetchall()
        except Exception:
            print("Error: unable to fetch data")
            print(Exception)
            self.MySQL_db.close()
        self.MySQL_db.close()
        return results

    # 数据增删改查
    def exe_sql(self, sql):
        cursor = self.MySQL_db.cursor()
        MySQL_sql = sql
        try:
            # 执行SQL语句
            cursor.execute(MySQL_sql)
            self.MySQL_db.commit()
        except Exception:
            print("Error: unable to fetch data")
            print(Exception)
            self.MySQL_db.close()
        self.MySQL_db.close()



