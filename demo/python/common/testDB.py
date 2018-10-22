import pymysql
from ConnectDataBase import ConnectionMyslq
def insert():
    print("添加数据：")
    conn = ConnectionMyslq("localhost", "root",
             "Gepoint", "pythondb", 3306)
    #sql = "UPDATE user SET age=26  WHERE rowid=7"
    sql = "insert into user(name,age,sex) values('mark',20,'男')"
    conn.exe_sql(sql)

def findlist():
    print("查询数据：")
    conn = ConnectionMyslq("localhost", "root",
                       "Gepoint", "pythondb", 3306)
    sql = "SELECT * FROM user"
    list = conn.findList(sql)
    for row in list:
        id = row[0]
        name = row[1]
        age = row[2]
        sex = row[3]
        print("序号:"+str(id)+"名字："+str(name)+"年龄："+str(age)+"性别："+str(sex))

def deleteRecord():
    print("删除数据：")
    conn = ConnectionMyslq("localhost", "root",
                           "Gepoint", "pythondb", 3306)
    sql = "DELETE FROM user WHERE name='mark'"
    conn.exe_sql(sql)

def updateRecord():
    print("更新数据：")
    conn = ConnectionMyslq("localhost", "root",
                           "Gepoint", "pythondb", 3306)
    sql = "UPDATE user SET age=26  WHERE rowid=7"
    conn.exe_sql(sql)

findlist()
#insert()
#deleteRecord()
#updateRecord()

'''
testdb = pymysql.connect(
    host="localhost",
    user="root",
    passwd="Gepoint",
    db="pythondb",
    port=3306,
    charset="utf8")

sql = "UPDATE user SET age=1  WHERE rowid=7"
cursor = testdb.cursor()
result = cursor.execute(sql)
testdb.commit()
testdb.close()
'''