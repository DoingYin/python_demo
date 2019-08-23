#!/usr/bin/python
# -*- coding: UTF-8 -*-
import uuid

import xlrd
import time
import datetime
import json
from com.database.ConnectDataBase import ConnectionDatabase

'''
    数据库连接
'''
def getConnect():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn

'''
     解析xls文件
'''
def analysisXsl():
    workbook=xlrd.open_workbook(r"C:\Users\YinYichang\Desktop\新建 XLSX 工作表.xlsx")
    sheet = workbook.sheet_by_index(0)
    # rowlen = sheet.nrows
    # print(rowlen)
    counter = 0

    '''
        解析xls时的数据类型
        ctype :  0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    '''
    for rownum in range(sheet.nrows):
        if (counter > 0):
            supervision = {}
            lineArr = sheet.row_values(rownum)
            # print(sheet.cell(rownum, 0).ctype)
            # 主键unid
            # print(lineArr)
            guid = sheet.cell(rownum, 0).value
            supervision["rowguid"] = guid

            # 排序号
            ordernum = sheet.cell(rownum, 1).value
            # supervision["ordernum"] = int(ordernum)
            if (sheet.cell(rownum, 1).ctype == 2):
                supervision["ordernum"] = int(ordernum)

            # 信息类别
            typeguid = sheet.cell(rownum, 2).value
            if (sheet.cell(rownum, 2).ctype == 2):
                if int(typeguid) == 1:
                    supervision["typeguid"] = '54774d35-b901-40cb-8c2a-df8749d1473d'
                elif int(typeguid) == 2:
                    supervision["typeguid"] = '1f7a7fb9-9a4f-4cc6-9e64-28a0f3fe4b6f'
                elif int(typeguid) == 3:
                    supervision["typeguid"] = '812cdf9b-9e29-44d4-a482-9c9ca20b9bf9'
                elif int(typeguid) == 4:
                    supervision["typeguid"] = 'c40c0d94-7887-4a91-8cb6-f4ff223f3714'
                elif int(typeguid) == 5:
                    supervision["typeguid"] = '65a6789c-e461-4812-83ab-d55d63c02cac'
                elif int(typeguid) == 6:
                    supervision["typeguid"] = '9697c7d4-102a-4b69-a2de-ec9c4f7a1656'
                else:
                    supervision["typeguid"] = ''

                    # 名称
            taskname = sheet.cell(rownum, 3).value
            taskname = taskname.replace('<font color="red">', '')
            taskname = taskname.replace('</font>', '');
            supervision["taskname"] = taskname
            # 任务状态
            # taskstatus = lineArr[4]
            # supervision["taskstatus"] = taskstatus
            # 责任部门
            responseouname = sheet.cell(rownum, 4).value
            supervision["responseouname"] = responseouname

            # 配合部门
            peiheouname = sheet.cell(rownum, 5).value
            supervision["peiheouname"] = peiheouname

            # 节点是否填写
            # hasNode = lineArr[7]
            # supervision["hasNode"] = hasNode
            # 登记人
            registername = sheet.cell(rownum, 6).value
            supervision["registername"] = registername

            # 登记时间
            registertime = sheet.cell(rownum, 7).value
            if (sheet.cell(rownum, 7).ctype == 3):
                date_value = xlrd.xldate_as_tuple(registertime, workbook.datemode)
                supervision["registertime"] = datetime.datetime(*date_value[:3]).strftime('%Y-%m-%d')

            # 类别名称
            typename = sheet.cell(rownum, 8).value
            supervision["typename"] = typename

            # 类别层次
            typelevl = sheet.cell(rownum, 9).value
            typelevl = typelevl.replace("_", "/")
            supervision["typelevl"] = typelevl

            # 分管领导
            fenguanname = sheet.cell(rownum, 10).value
            supervision["fenguanname"] = fenguanname

            # 反馈时间
            feedbacktime = sheet.cell(rownum, 11).value
            if (sheet.cell(rownum, 11).ctype == 3):
                date_value = xlrd.xldate_as_tuple(feedbacktime, workbook.datemode)
                supervision["feedbacktime"] = datetime.datetime(*date_value[:3]).strftime('%Y-%m-%d')

            # 反馈周期
            feedbackcyvle = sheet.cell(rownum, 12).value
            supervision["feedbackcyvle"] = feedbackcyvle

            # 节点交流是否完成
            isfinished = sheet.cell(rownum, 13).value
            supervision["isfinished"] = int(isfinished)

            # 责任部门电话
            responseoutel = sheet.cell(rownum, 14).value
            if (sheet.cell(rownum, 14).ctype == 2):
                supervision["responseoutel"] = int(responseoutel)
            else:
                supervision["responseoutel"] = responseoutel

            # 工作年份
            jobyear = sheet.cell(rownum, 15).value
            supervision["jobyear"] = int(jobyear)

            # 配合部门电话
            peiheoutel = sheet.cell(rownum, 16).value
            if (sheet.cell(rownum, 16).ctype == 2):
                supervision["peiheoutel"] = int(peiheoutel)
            else:
                supervision["peiheoutel"] = peiheoutel
            # print(supervision)
            insertData(supervision)
        counter += 1
    # for row in sheet.get_rows():
    #     for coln in row:
    #         print(coln)
    # print(sheet.row_values(0))
    # return sheet

'''
    插入督查督办数据
'''
def insertData(supervision):
    conn = getConnect()
    sql = "INSERT INTO SJ_SUPERVISION_TASK_REGISTER(rowguid, ordernum, taskname, " \
          "responseouname, peiheouname, registername, registertime, " \
          "typename, typelevel, fenguanname, feedbacktime, feedbackcyvle, isfinished," \
          "responseoutel, peiheoutel, jobyear) VALUES('%s', %d, '%s', '%s', '%s', '%s'," \
          " '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', %d)" \
          % (supervision["rowguid"], supervision["ordernum"], supervision["taskname"],
             supervision["responseouname"], supervision["peiheouname"], supervision["registername"],
             supervision["registertime"], supervision["typename"], supervision["typelevl"],
             supervision["fenguanname"], supervision["feedbacktime"], supervision["feedbackcyvle"],
             supervision["isfinished"], supervision["responseoutel"], supervision["peiheoutel"],
             supervision["jobyear"])
    # print(sql)
    conn.mssql_exe_sql(sql)
    # print("-" * 50, "sqlserver", "-" * 50)

'''
    解析督查督办xls文件
'''
def analysisSupervision():
    path = 'F:\松江OA\OA数据解析\supervision.xlsx'
    sheet = analysisXsl(path)
    # print(sheet)
    # for row in sheet.row_values():
    #     print(row)




if __name__ == "__main__":
    analysisXsl()
    #analysisUser_info()
    #analusisWd24Opinion()
    # handle_wd24_flow_test()
    # workflowListData()