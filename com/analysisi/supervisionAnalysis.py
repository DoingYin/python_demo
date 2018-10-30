#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import xlrd
from com.database.ConnectDataBase import ConnectionDatabase


# 解析数据
def analysisSupervision():
    file = open('F:\松江OA\OA数据解析\supervision', 'r', encoding='utf-8')
    i = 1
    for line in file.readlines():
        i += 1
        lineArr = line.split(',')
        if (len(lineArr) > 1):
            supervision = {}
            # unid
            print(lineArr)
            guid = lineArr[0].strip('"').strip()
            supervision["rowguid"] = guid
            # 排序号
            ordernum = lineArr[1].strip('"').strip()
            supervision["ordernum"] = int(ordernum)
            # 信息类别
            typeguid = lineArr[2].strip('"').strip()
            supervision["typeguid"] = typeguid
            # 名称
            taskname = lineArr[3].strip('"').strip()
            supervision["taskname"] = taskname
            # 任务状态
            # taskstatus = lineArr[4]
            # supervision["taskstatus"] = taskstatus
            # 责任部门
            responseouname = lineArr[4].strip('"').strip()
            supervision["responseouname"] = responseouname
            # 配合部门
            peiheouname = lineArr[5].strip('"').strip()
            supervision["peiheouname"] = peiheouname
            # 节点是否填写
            # hasNode = lineArr[7]
            # supervision["hasNode"] = hasNode
            # 登记人
            registername = lineArr[6].strip('"').strip()
            supervision["registername"] = registername
            # 登记时间
            registertime = lineArr[7].strip('"').strip()
            # regtime = time.strptime(registertime, '%Y/%m/%d')
            registertime = time.strptime(registertime, '%Y/%m/%d')
            supervision["registertime"] = time.strftime('%Y-%m-%d %H:%M:%S', registertime)
            # 类别名称
            typename = lineArr[8].strip('"').strip()
            supervision["typename"] = typename
            # 类别层次
            typelevl = lineArr[9].strip('"').strip()
            typelevl = typelevl.replace("_", "/")
            supervision["typelevl"] = typelevl
            # 分管领导
            fenguanname = lineArr[10].strip('"').strip()
            supervision["fenguanname"] = fenguanname
            # 反馈时间
            feedbacktime = lineArr[11].strip('"').strip()
            feedbacktime = time.strptime(feedbacktime, '%Y/%m/%d')
            supervision["feedbacktime"] = time.strftime('%Y-%m-%d %H:%M:%S', feedbacktime)
            # 反馈周期
            feedbackcyvle = lineArr[12].strip('"').strip()
            supervision["feedbackcyvle"] = feedbackcyvle
            # 节点交流是否完成
            isfinished = lineArr[13].strip('"').strip()
            supervision["isfinished"] = int(isfinished)
            # 责任部门电话
            responseoutel = lineArr[14].strip('"').strip()
            supervision["responseoutel"] = responseoutel
            # 工作年份
            jobyear = lineArr[15].strip('"').strip()
            supervision["jobyear"] = int(jobyear)
            # 配合部门电话
            peiheoutel = lineArr[16].strip('"').strip()
            supervision["peiheoutel"] = peiheoutel
            # print(peiheoutel)
            # print(peiheoutel == "")
            # insertData(supervision)
            # print(supervision)
            # if i > 1:
            #     break
    print(i)

# 解析xls文件
def analysisXsl(path):
    workbook = xlrd.open_workbook(path)
    print(workbook)
    sheet = workbook.sheet_by_index(0)
    return sheet

def analysisSupervision():
    path = 'F:\松江OA\OA数据解析\supervision1.xls'
    sheet = analysisXsl(path)
    print(sheet)
    # for row in sheet.row_values():
    #     print(row)

# 插入数据
def insertData(supervision):
    conn = ConnectionDatabase("localhost", "sa", "11111", "oa_supervision")
    sql = "INSERT INTO SJ_SUPERVISION_TASK_REGISTER(rowguid, ordernum, taskname, " \
          "responseouname, peiheouname, registername, registertime, " \
          "typename, typelevel, fenguanname, feedbacktime, feedbackcyvle, isfinished," \
          "responseoutel, peiheoutel, jobyear) VALUES('%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', %d)"\
          % (supervision["rowguid"], supervision["ordernum"], supervision["taskname"],
             supervision["responseouname"], supervision["peiheouname"], supervision["registername"],
             supervision["registertime"], supervision["typename"], supervision["typelevl"],
             supervision["fenguanname"], supervision["feedbacktime"], supervision["feedbackcyvle"],
             supervision["isfinished"], supervision["responseoutel"], supervision["peiheoutel"],
             supervision["jobyear"])
    # print(sql)
    results = conn.mssql_exe_sql(sql)
    print("-" * 50, "sqlserver", "-" * 50)
    print(results)

def findList():
    conn = ConnectionDatabase("localhost", "sa", "11111", "oa_supervision")
    sql = "SELECT * FROM SJ_SUPERVISION_TASK_REGISTER"
    result = conn.mssql_findList(sql)
    for line in result:
        print(line)

if __name__ == "__main__":
    # analysisSupervision()
    # findList()
    analysisSupervision()
