#!/usr/bin/python
# -*- coding: UTF-8 -*-

import uuid
import time
import re
import json
from tkinter import filedialog
import xlrd
import sys
from com.analysisi.utils import Utils

sys.path.append("E:\IdeaWorkspace\python_demo")
from com.database.ConnectDataBase import ConnectionDatabase

'''
    数据库连接
'''


def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn


def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn


'''
    打开文件
'''


def openFile():
    __fileName = filedialog.askopenfilename(title='打开文件', filetypes=[('All Files', '*'), ('All Files', '*')])
    return __fileName


def getSheet():
    __fileName = openFile()
    __workbook = xlrd.open_workbook(__fileName, encoding_override='utf-8')
    return __workbook.sheet_by_index(0)


def findAllWd25(conn):
    __sql = '''
        SELECT UNID,subject,DocMark,DocMark_ZB,Subject_Leader,DocNum,HandleOrView,SourceUnit,FileCategory,
            RegPerson,C_CreateUser,UrgentLevel,SecLevel,DocType,KeepTerm,QueryLevel,ArchiveType,SignDate,
            RegDate,DealUnit,DealDate,Deadline,IsReturnFile,Attachment,remark,RegDeptTitle,RegDept FROM Sheet1
    '''
    results = conn.mssql_findList(__sql)
    return results


'''
    导入Excel数据
'''
def import_wd25():
    counter = 0
    __conn = getConnect_new()
    __conn_1 = getConnect_old()
    results = findAllWd25(__conn_1)
    # __conn_1.closeConn()
    for record in results:
        Wd25 = {}

        # 主键
        # UNID = sheet.cell(rownum, 0).value
        UNID = record[0]

        if not UNID:
            UNID = None
            continue
        else:
            UNID = re.sub('[^0-9|a-zA-Z]', '', UNID)
        if UNID == '':
            # print("跳过该数据:%s"%UNID)
            continue
        Wd25["RowGuid"] = UNID
        Wd25["ProcessVersionInstanceGuid"] = UNID

        # 标题
        # subject = sheet.cell(rownum, 1).value
        subject = record[1]
        if not subject:
            subject = None
        Wd25["TxtTitle"] = subject

        # 文件字号
        # DocMark = sheet.cell(rownum, 2).value
        DocMark = record[2]
        if not DocMark:
            DocMark = None
        Wd25["txtlaiwenhao"] = DocMark

        # 发文字号
        # DocMark_ZB = sheet.cell(rownum, 3).value
        DocMark_ZB = record[3]
        if not DocMark_ZB:
            DocMark_ZB = None
        Wd25["ShouWenFileNumber"] = DocMark_ZB

        # 答复意见
        # Subject_Leader = sheet.cell(rownum, 4).value
        Subject_Leader = record[4]
        if not Subject_Leader:
            Subject_Leader = None
        Wd25["replyTitle"] = Subject_Leader

        # 流水号
        # DocNum = sheet.cell(rownum, 5).value
        DocNum = record[5]
        if not DocNum:
            DocNum = None
        Wd25["flowNum"] = DocNum

        # 文件标识
        # HandleOrView = sheet.cell(rownum, 6).value
        HandleOrView = record[6]
        if not HandleOrView:
            HandleOrView = None
        Wd25["fileCode"] = HandleOrView

        # 来文单位
        # SourceUnit = sheet.cell(rownum, 7).value
        SourceUnit = record[7]
        if not SourceUnit:
            SourceUnit = None
        Wd25["txtlaiwendept"] = SourceUnit

        # 收文分类
        # FileCategory = sheet.cell(rownum, 8).value
        FileCategory = record[8]
        if not FileCategory:
            FileCategory = None
        Wd25["fileStyle"] = FileCategory

        # 登记人
        # RegPerson = sheet.cell(rownum, 9).value
        RegPerson = record[9]
        if not RegPerson:
            RegPerson = None
        Wd25["initUserDisplayName"] = RegPerson

        # 登记人guid
        C_CreateUser = record[10]
        C_CreateUser = Utils.getInitUserGuid(C_CreateUser, __conn_1)
        if not C_CreateUser:
            C_CreateUser = None
        elif C_CreateUser == 2:
            C_CreateUser = ''
        Wd25["InitUserGuid"] = C_CreateUser

        # 紧急程度
        # UrgentLevel = sheet.cell(rownum, 11).value
        UrgentLevel = record[11]
        if not UrgentLevel:
            UrgentLevel = None
        Wd25["jinji"] = UrgentLevel

        # 文件密级
        # SecLevel = sheet.cell(rownum, 12).value
        SecLevel = record[12]
        if not SecLevel:
            SecLevel = None
        Wd25["jpdMiji"] = SecLevel

        # 文种
        # DocType = sheet.cell(rownum, 13).value
        DocType = record[13]
        if not DocType:
            DocType = None
        Wd25["Arch_Type"] = DocType

        # 保管期限
        # KeepTerm = sheet.cell(rownum, 14).value
        KeepTerm = record[14]
        if not KeepTerm:
            KeepTerm = None
        Wd25["saveTime"] = KeepTerm

        # 查询级别
        # QueryLevel = sheet.cell(rownum, 15).value
        QueryLevel = record[15]
        if not QueryLevel:
            QueryLevel = None
        Wd25["searchLevel"] = QueryLevel

        # 归档类型
        # ArchiveType = sheet.cell(rownum, 16).value
        ArchiveType = record[16]
        if not ArchiveType:
            ArchiveType = None
        Wd25["clearFileType"] = ArchiveType

        # 发文日期
        # SignDate = sheet.cell(rownum, 17).value
        SignDate = record[17]
        if not SignDate:
            SignDate = time.localtime()
        else:
            # SignDate = re.sub('[^0-9 | \/]', '', SignDate)
            SignDateTime = Utils.formatStrToTime(SignDate)
        SignDate = Utils.fromatTimeToStr(SignDateTime, "%Y-%m-%d")
        Wd25["TxtFileDate"] = SignDate

        # 收文日期
        # RegDate = sheet.cell(rownum, 18).value
        RegDate = record[18]
        jpdshouwenyear = None
        if not RegDate:
            RegDateTime = time.localtime()
        else:
            jpdshouwenyear = RegDate.split('/')[0]
            jpdshouwenyear = re.sub('[^0-9]', '', jpdshouwenyear)
            # RegDate = re.sub('[^0-9 | \/]', '', RegDate)
            RegDateTime = Utils.formatStrToTime(RegDate)
        RegDate = Utils.fromatTimeToStr(RegDateTime, "%Y-%m-%d")
        Wd25["TxtShouWenDate"] = str(RegDate)
        Wd25["jpdshouwenyear"] = jpdshouwenyear

        # 主办单位
        # DealUnit = sheet.cell(rownum, 19).value
        DealUnit = record[19]
        if not DealUnit:
            DealUnit = None
        Wd25["txtzhuban"] = DealUnit

        # 交办日期
        # DealDate = sheet.cell(rownum, 20).value
        DealDateStr = record[20]
        if not DealDateStr:
            DealDateTime = time.localtime()
        else:
            DealDateStrs = str(DealDateStr).split(',')
            # DealDateStr = re.sub('[^0-9 | \/]', '', str(DealDateStrs[0]))
            DealDateTime = Utils.formatStrToTime(DealDateStrs[0])
        DealDateStr = Utils.fromatTimeToStr(DealDateTime, "%Y-%m-%d")
        Wd25["banjieDate"] = DealDateStr

        # 办理期限
        # Deadline = sheet.cell(rownum, 21).value
        Deadline = record[21]
        if not Deadline:
            DeadlineTime = time.localtime()
        else:
            # Deadline = re.sub('[^0-9 | \/]', '', Deadline)
            DeadlineTime = Utils.formatStrToTime(Deadline)

        Deadline = Utils.fromatTimeToStr(DeadlineTime, "%Y-%m-%d")
        Wd25["overTime"] = Deadline

        # 是否退文
        # IsReturnFile = sheet.cell(rownum, 22).value
        IsReturnFile = record[22]
        if not IsReturnFile:
            IsReturnFile = None
        Wd25["isQuit"] = IsReturnFile

        # 文件附件
        # Attachment = sheet.cell(rownum, 23).value
        Attachment = record[23]
        if not Attachment:
            Attachment = None
        Wd25["attach"] = Attachment

        # 备注
        # remark = sheet.cell(rownum, 24).value
        remark = record[24]
        if not remark:
            remark = None
        Wd25["bark"] = remark

        # 收文员所属科室
        # RegDeptTitle = sheet.cell(rownum, 25).value
        RegDeptTitle = record[25]
        if not RegDeptTitle:
            RegDeptTitle = None
        Wd25["ouname"] = RegDeptTitle

        # 收文员所属科室Guid
        # RegDeptTitleGuid = sheet.cell(rownum, 26).value
        RegDept = record[26]
        # RegDept = getInitDeptGuid(RegDeptTitle, __conn)
        # if not RegDept:
        #     RegDept = ''
        # elif RegDept == 1:
        #     RegDept = 'a'
        # elif RegDept == 2:
        #     RegDept = ''
        Wd25["ouguid"] = RegDept

        # 迁移数据状态
        Wd25["imported"] = "1"
        Wd25["ArchiveState"] = "1"
        SubWebFlowOuGuid = Utils.getSubWebFlowOuGuid('wd25_workflow_done', UNID, __conn)
        Wd25['SubWebFlowOuGuid'] = SubWebFlowOuGuid
        if insertWd25(Wd25, __conn) > 0:
            counter += 1
            print("已经插入：%d条数据。" % counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()
    __conn_1.closeConn()


'''
    向数据库表（Wd_25）插入数据
'''


def insertWd25(Wd25, __conn):
    sql = '''
        insert into wd_25(
            RowGuid, ProcessVersionInstanceGuid, txttitle, txtlaiwenhao, ShouWenFileNumber, replyTitle, 
            flowNum, fileCode, txtlaiwendept, fileStyle, initUserDisplayName, InitUserGuid, jinji,
            jpdMiji, Arch_Type, saveTime, searchLevel, clearFileType, TxtFileDate, TxtShouWenDate, jpdshouwenyear,
            txtzhuban, banjieDate, overTime, isQuit, attach, bark, ouname, ouguid, imported, ArchiveState, 
            SubWebFlowOuGuid
        ) values (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    '''
    params = (
        Wd25["RowGuid"], Wd25["ProcessVersionInstanceGuid"], Wd25["TxtTitle"], Wd25["txtlaiwenhao"],
        Wd25["ShouWenFileNumber"],
        Wd25["replyTitle"], Wd25["flowNum"], Wd25["fileCode"], Wd25["txtlaiwendept"], Wd25["fileStyle"],
        Wd25["initUserDisplayName"],
        Wd25["InitUserGuid"], Wd25["jinji"], Wd25["jpdMiji"], Wd25["Arch_Type"], Wd25["saveTime"], Wd25["searchLevel"],
        Wd25["clearFileType"], Wd25["TxtFileDate"], Wd25["TxtShouWenDate"], Wd25["jpdshouwenyear"], Wd25["txtzhuban"],
        Wd25["banjieDate"], Wd25["overTime"], Wd25["isQuit"], Wd25["attach"], Wd25["bark"], Wd25["ouname"],
        Wd25["ouguid"], Wd25["imported"], Wd25["ArchiveState"], Wd25['SubWebFlowOuGuid']
    )
    # print(sql)
    result = 0
    try:
        result = __conn.mssql_exe_sql(sql, params)
        # print(sql%params)
    except Exception as e:
        print(e)
    return result


############################################流程意见处理#################################################
'''
    导出要处理的审批意见数据
'''


def getAllOpinions(__conn):
    sql = "SELECT a.ParentUnid, a.OpinionUser,a.OpinionUserTitle,a.time,a.opinionbody,a.opiniontype,a.unitIndex FROM wd25_opinion15 a"
    results = __conn.mssql_findList(sql)
    return results


'''
    处理数据
'''


def handleOpinion():
    __conn = getConnect_old()
    records = getAllOpinions(__conn)
    counter = 0
    for record in records:
        wd25Opinion = {}
        parentUnid = record[0]
        if not parentUnid:
            parentUnid = ''
        else:
            parentUnid = re.sub('[^0-9 | a-zA-Z]', '', parentUnid)
        wd25Opinion['parentUnid'] = parentUnid

        wd25Opinion['opinionUser'] = record[1]
        wd25Opinion['opinionUserTitle'] = record[2]
        opinionTime = record[3]
        if not opinionTime:
            opinionTime = ''
        else:
            opinionTime = re.sub('[^0-9 | \/ | :]', '', opinionTime)
        wd25Opinion['opinionTime'] = opinionTime

        wd25Opinion['opinionbody'] = record[4]
        wd25Opinion['opiniontype'] = record[5]
        unitIndex = record[6]
        try:
            if not unitIndex:
                unitIndex = 0
            elif unitIndex == '':
                unitIndex = 0
            wd25Opinion['unitIndex'] = int(unitIndex)
        except Exception as e:
            print(parentUnid)
            print(e)

        if insertOpinion(wd25Opinion, __conn):
            counter += 1
            print('已经插入数据：%d 条。' % counter)
            if counter % 1000 == 0:
                __conn.commitData()
        else:
            break
    __conn.commitData()
    __conn.closeConn()


'''
    插入流程意见信息
'''


def insertOpinion(Wd25Opinion, __conn):
    sql = '''
        INSERT INTO wd25_opinions(ParentUnid, OpinionUser, OpinionUserTitle, opinionTime, opinionbody, opiniontype, unitIndex) 
        VALUES(%s, %s, %s, %s, %s, %s, %d)
    '''
    params = (
    Wd25Opinion['parentUnid'], Wd25Opinion['opinionUser'], Wd25Opinion['opinionUserTitle'], Wd25Opinion['opinionTime'],
    Wd25Opinion['opinionbody'], Wd25Opinion['opiniontype'], Wd25Opinion['unitIndex'])
    print(sql % params)
    return __conn.mssql_exe_sql(sql, params)


############################################工作流处理###################################################

'''
    工作流数据处理
'''
def handle_wd25_workflow():
    conn = getConnect_old()
    sql = '''
            SELECT w1.UNID, w1.s_flowunid, w1.c_flowunid, w1.subject, w1.SignDate, w1.RegDate, w1.U_UnitName, w1.U_UnitIndex, 
            w1.U_UnitUser,w1.U_UnitUserTitle, w1.U_UnitEndTime, w1.U_UnitToTitle, w1.U_UnitAction FROM wd25_workflow w1
        '''
    # 分页处理数据
    # sql = '''
    #     SELECT w1.UNID, w1.s_flowunid, w1.c_flowunid, w1.subject, w1.SignDate, w1.RegDate, w1.U_UnitName, w1.U_UnitIndex,
    #         w1.U_UnitUserTitle, w1.U_UnitEndTime, w1.U_UnitToTitle, w1.U_UnitAction FROM wd25_workflow_test w1, (
    #         SELECT TOP 1000 row_number() OVER (ORDER BY UNID DESC) n, UNID FROM wd25_workflow_test
    #     ) w2 WHERE w1.UNID = w2.UNID AND w2.n > 0 ORDER BY w2.n ASC
    # '''
    records = conn.mssql_findList(sql)
    counter = 0
    exCounter = 0
    for record in records:
        # print(record)
        wd25Workflow = {}
        # uuid
        UNID = record[0]
        if not UNID:
            UNID = ''
        else:
            UNID = re.sub('[^0-9 | a-zA-Z]', '', UNID)
        wd25Workflow["UNID"] = str(UNID)

        # s_flowunid
        s_flowunid = str(record[1])
        if not s_flowunid:
            s_flowunid = ''
        else:
            s_flowunid = re.sub('[^0-9 | a-zA-Z]', '', s_flowunid)
        wd25Workflow["s_flowunid"] = s_flowunid

        # c_flowunid
        c_flowunid = record[2]
        if not c_flowunid:
            c_flowunid = ''
        else:
            c_flowunid = re.sub('[^0-9 | a-zA-Z]', '', c_flowunid)
        wd25Workflow["c_flowunid"] = str(c_flowunid)

        # subject
        subject = record[3]
        wd25Workflow["subject"] = subject

        # signdate
        SignDate = record[4]
        if SignDate:
            SignDate = re.sub('[^0-9 | \/ | :]', '', SignDate)
        else:
            SignDate = ''
        wd25Workflow["SignDate"] = SignDate

        # RegDate
        RegDate = record[5]
        if RegDate:
            RegDate = re.sub('[^0-9 | \- ]', '', RegDate)
        else:
            RegDate = ''
        wd25Workflow["RegDate"] = RegDate

        # 步骤名称
        if record[6] is not None:
            unitNameStr = record[6]
            unitNames = unitNameStr.split(',')

            for i in range(len(unitNames)):
                rowguid = uuid.uuid1()
                wd25Workflow["rowguid"] = str(rowguid)

                # print(rowguid)
                wd25Workflow["U_UnitName"] = unitNames[i]
                # U_UnitName = unitNames[i]

                # 审批环节类型
                U_UnitType = ""
                if unitNames[i] == "退回意见":
                    U_UnitType = "Back"
                elif unitNames[i] == "批示意见":
                    U_UnitType = "PSopinion"
                elif unitNames[i] == "审核意见":
                    U_UnitType = "Read0"
                elif unitNames[i] == "协办意见":
                    U_UnitType = "Read3"
                elif unitNames[i] == "拟办意见":
                    U_UnitType = "Read4"
                elif unitNames[i] == "批阅意见":
                    U_UnitType = "Vatify"
                elif unitNames[i] == "文管理":
                    U_UnitType = "文管理"
                else:
                    U_UnitType = ""

                wd25Workflow["U_UnitType"] = U_UnitType

                # unitindex
                unitIndexStr = record[7]
                unitIndexStrs = unitIndexStr.split(',')
                # if unitIndexStrs[i]:
                #     wd25Workflow["U_UnitIndex"] = int(unitIndexStrs[i])
                # else:
                #     wd25Workflow["U_UnitIndex"] = 0
                wd25Workflow["U_UnitIndex"] = 0

                # 审批人guid
                unitUserStr = record[8]
                unitUsers = unitUserStr.split(',')
                wd25Workflow["U_UnitUser"] = unitUsers[i]

                # 审批人名称
                unitUserTitleStr = record[9]
                unitUserTitles = unitUserTitleStr.split(',')
                wd25Workflow["U_UnitUserTitle"] = unitUserTitles[i]
                # U_UnitUserTitle = unitUserTitles[i]

                # 审批时间
                unitEndTimeStr = record[10]
                unitEndTimes = unitEndTimeStr.split(',')
                U_UnitEndTime = unitEndTimes[i]
                if U_UnitEndTime:
                    U_UnitEndTime = re.sub('[^0-9 | \- | : ]', '', U_UnitEndTime)
                else:
                    U_UnitEndTime = ''
                wd25Workflow["U_UnitEndTime"] = U_UnitEndTime
                # U_UnitEndTime = unitEndTimes[i]

                # 接收人
                unitToTitleStr = record[11]
                unitToTitles = unitToTitleStr.split(',')
                wd25Workflow["U_UnitToTitle"] = unitToTitles[i]
                # U_UnitToTitle = unitToTitles[i]

                # 流程动作
                unitActionStr = record[12]
                unitActions = unitActionStr.split(',')
                wd25Workflow["U_UnitAction"] = unitActions[i]
                # U_UnitAction = unitActions[i]

                # print(wd25Workflow)
                # print(unid)
                counter += 1
                result = insertFullWd25Workflow(wd25Workflow, conn)
                if result:
                    pass
                else:
                    break

                print("插入记录计数器：%d, 结果：%s" % (counter, result))
                if counter % 1000 == 0:
                    conn.commitData()

        else:
            continue
            rowguid = uuid.uuid1()
            wd25Workflow["rowguid"] = str(rowguid)
            # print(unid)
            counter += 1
            result = insertLackWd25Workflow(wd25Workflow, conn)
            if result:
                pass
            else:
                break

            print("插入记录计数器：%d, 结果：%s" % (counter, result))
            if counter % 1000 == 0:
                conn.commitData()

    conn.commitData()
    conn.closeConn()


'''
    插入审批流程信息（完整）
'''


def insertFullWd25Workflow(wd25Workflow, conn):
    # conn = getConnect()
    sql = '''
        INSERT INTO wd25_workflow_copy(rowguid,UNID, s_flowunid, c_flowunid, subject, SignDate, RegDate,U_UnitIndex,U_UnitName,
            U_UnitUser,U_UnitUserTitle, U_UnitEndTime, U_UnitToTitle, U_UnitType, U_UnitAction) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %d, %s, %s, %s, %s, %s, %s, %s)
          '''
    params = (wd25Workflow["rowguid"], wd25Workflow["UNID"], wd25Workflow["s_flowunid"], wd25Workflow["c_flowunid"],
              wd25Workflow["subject"], wd25Workflow["SignDate"], wd25Workflow["RegDate"], wd25Workflow["U_UnitIndex"],
              wd25Workflow["U_UnitName"], wd25Workflow["U_UnitUser"], wd25Workflow["U_UnitUserTitle"],
              wd25Workflow["U_UnitEndTime"],
              wd25Workflow["U_UnitToTitle"], wd25Workflow["U_UnitType"], wd25Workflow["U_UnitAction"])

    try:
        conn.mssql_exe_sql(sql, params)
    except Exception as e:
        print(sql % params)
        print(e)
        return False

    return True
    # return conn.mssql_exe_sql(sql)


'''
    插入审批流程信息（缺少数据）
'''


def insertLackWd25Workflow(wd25Workflow, conn):
    # conn = getConnect()
    sql = '''
        INSERT INTO wd25_workflow_copy(rowguid, UNID, s_flowunid, c_flowunid, subject, SignDate, RegDate) 
            VALUES(%s, %s, %s, %s, %s, %s, %s)
          '''
    params = (wd25Workflow["rowguid"], wd25Workflow["UNID"], wd25Workflow["s_flowunid"], wd25Workflow["c_flowunid"],
              wd25Workflow["subject"], wd25Workflow["SignDate"], wd25Workflow["RegDate"])
    # print(sql)
    conn.mssql_exe_sql(sql, params)

    return True
    # return conn.mssql_exe_sql(sql)


def insertHandle25Workflow(wd25Workflow, conn):
    # conn = getConnect()
    sql = '''
        INSERT INTO wd25_workflow_done(UNID, U_UnitName, U_UnitUserTitle, U_UnitEndTime, U_UnitAction,
            U_UnitToTitle, U_UnitUser) VALUES(%s, %s, %s, %s, %s, %s, %s)
          '''
    params = (wd25Workflow["UNID"], wd25Workflow["U_UnitName"], wd25Workflow["U_UnitUserTitle"],
              wd25Workflow['U_UnitEndTime'], wd25Workflow["U_UnitAction"], wd25Workflow["U_UnitToTitle"],
              wd25Workflow["U_UnitUser"])
    # print(sql)
    try:
        conn.mssql_exe_sql(sql, params)
    except Exception as e:
        print(sql % params)
        print(e)
        return False
    return True
    # return conn.mssql_exe_sql(sql)


# ====================================分割线流程意见信息处理============================================
'''
    意见信息处理
'''
# 获取表wd25_opinion1-wd25_opinion15的数据
def getOpinionData(__conn, tbl):
    sql = '''
        SELECT [ParentUnid], [UNID], [OpinionUser], [OPINIONUSERTITLE], [OpinionField], 
            [LastModified], [time], [OPINIONBODY], [OPINIONTYPE], [UnitIndex] FROM %s
    ''' % tbl
    return __conn.mssql_findList(sql)


# 将所有opinion的数据存储到wd25_opinions
def insertToOpinions(__conn, opinion):
    sql = '''
        INSERT INTO wd25_opinions (ParentUnid, UNID, OpinionUser, OPINIONUSERTITLE, OpinionField, 
            LastModified, opinionTime, OPINIONBODY, OPINIONTYPE, UnitIndex) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (opinion['ParentUnid'], opinion['UNID'], opinion['OpinionUser'], opinion['OPINIONUSERTITLE'],
              opinion['OpinionField'], opinion['LastModified'], opinion['opinionTime'], opinion['OPINIONBODY'],
              opinion['OPINIONTYPE'], opinion['UnitIndex'])
    try:
        result = __conn.mssql_exe_sql(sql, params)
    except Exception as e:
        print(sql % params)
        print(e)
    return result


# 处理多个意见库的信息
def handleOpinons():
    __conn = getConnect_old()
    tbl = 'wd25_opinion'
    counter = 0
    for i in range(1, 15):
        tbl = tbl + str(i)
        records = getOpinionData(__conn, tbl)
        tbl = 'wd25_opinion'
        for record in records:
            opinion = {}
            opinion['ParentUnid'] = str(record[0])
            opinion['UNID'] = str(record[1])
            opinion['OpinionUser'] = str(record[2])
            opinion['OPINIONUSERTITLE'] = str(record[3])
            opinion['OpinionField'] = str(record[4])
            opinion['LastModified'] = str(record[5])
            opinion['opinionTime'] = str(record[6])
            opinion['OPINIONBODY'] = str(record[7])
            opinion['OPINIONTYPE'] = str(record[8])
            opinion['UnitIndex'] = str(record[9])
            if insertToOpinions(__conn, opinion):
                counter += 1
                print("插入：%d 条意见信息。" % counter)
            if (counter % 1000 == 0):
                __conn.commitData()

    __conn.commitData()
    __conn.closeConn()


################################################流程步骤意见信息封装处理#############################################
'''
    数据迁移,封装流程步骤对应的数据
'''
def workitemdata(wd25workflow):
    objworkitem = {}
    objworkitem['workItemGuid'] = str(uuid.uuid1())
    objworkitem['activityName'] = wd25workflow['U_UnitName']
    objworkitem['workItemName'] = ''
    objworkitem['workItemType'] = ''
    objworkitem['handleUrl'] = ''
    objworkitem['status'] = ''
    objworkitem['readDate'] = wd25workflow['U_UnitEndTime']
    objworkitem['operationDate'] = wd25workflow['U_UnitEndTime']
    objworkitem['createDate'] = wd25workflow['U_UnitEndTime']
    objworkitem['endDate'] = wd25workflow['U_UnitEndTime']
    objworkitem['opinion'] = wd25workflow['opinionbody']
    objworkitem['terminateDate'] = ''
    objworkitem['processVersionInstanceGuid'] = wd25workflow['UNID']
    objworkitem['operationType'] = ''
    objworkitem['transactorName'] = wd25workflow['U_UnitUserTitle']
    objworkitem['operatorName'] = wd25workflow['U_UnitAction']
    objworkitem['operationname'] = wd25workflow['U_UnitAction']
    objworkitem['operatorForDisplayName'] = wd25workflow['U_UnitUserTitle']
    objworkitem['senderName'] = wd25workflow['U_UnitUserTitle']
    objworkitem['note'] = ''
    return objworkitem


'''
    审批流程对应的步骤数据列表
'''
def workitemList(conn,pviguid, subject,SignDate):
    # 通过流程guid获取相关的审批步骤数据
    sql = \
        '''
            select UNID,U_UnitName,U_UnitEndTime,U_UnitUser,U_UnitUserTitle, U_UnitAction, U_UnitToTitle, opinionbody from 
                wd25_workflow_test where UNID='%s' order by U_UnitEndTime ASC
        ''' % pviguid
    # conn = getConnect()
    records = conn.mssql_findList(sql)
    workitemMap = {}
    workitemlist = []
    counter = 0
    if records and len(records) > 0:
        for coursor in records:
            # print(coursor)
            wd25workflow = {}
            if len(coursor[1]) < 2 or len(coursor[4]) < 2:
                continue
            wd25workflow['UNID'] = coursor[0]
            wd25workflow['wd25Title'] = subject
            senddate = SignDate
            if senddate:
                senddate = re.sub('[^0-9 | \/ | :]', '', senddate)
            else:
                senddate = ''
            wd25workflow['senddate'] = senddate
            wd25workflow['U_UnitName'] = coursor[1]
            U_UnitEndTime = coursor[2]
            if U_UnitEndTime:
                U_UnitEndTime = re.sub('[^0-9 | \/ | :]', '', U_UnitEndTime)
            else:
                U_UnitEndTime = ''
            wd25workflow['U_UnitEndTime'] = U_UnitEndTime
            wd25workflow['U_UnitUser'] = coursor[3]
            wd25workflow['U_UnitUserTitle'] = coursor[4]
            wd25workflow['U_UnitAction'] = coursor[5]
            U_UnitToTitleStr = coursor[6]
            if U_UnitToTitleStr:
                U_UnitToTitleStr = str(U_UnitToTitleStr).replace('等', '')
            wd25workflow['U_UnitToTitle'] = U_UnitToTitleStr
            wd25workflow['opinionbody'] = coursor[7]

            #流程步骤对应的信息处理
            workitem = workitemdata(wd25workflow)
            workitemlist.append(workitem)
            counter += 1
            print("流程步骤信息处理了 %d 条。" % counter)
    workitemMap['workitemlist'] = workitemlist
    return workitemMap


'''
    获取对应的意见信息
'''
def workflow_opinion(unitEndTimeStr, parentUnid, unitIndex, opinionUserTitle, conn):
    try:
        if unitEndTimeStr:
            unitEndTimeStr = re.sub('[^0-9]', '', unitEndTimeStr)[:-2]
    except Exception as e:
        print(parentUnid)
        print(e)

    sql = '''
            SELECT opinionTime,OPINIONBODY,parentUnid FROM wd25_opinions WHERE ParentUnid = '%s' AND OPINIONUSERTITLE = '%s'
                ORDER BY opinionTime ASC
        ''' % (parentUnid, int(unitIndex), opinionUserTitle)
    records = conn.mssql_findList(sql)
    opinionBody = ''
    if records and len(records) == 1:
        opinionBody = records[0][1]
    elif records and len(records) > 1:
        for record in records:
            opinionTimeStr = record[0]
            try:
                if opinionTimeStr:
                    # 转为数字比较
                    opinionTimeStr = re.sub('[^0-9]', '', opinionTimeStr)[:-2]
                if unitEndTimeStr == opinionTimeStr:
                    opinionBody = record[1]
                    break
            except Exception as e:
                print(parentUnid)
                print(e)
                break
    else:
        opinionBody = ''

    return opinionBody


'''
    workflow对应的一条数据模型
'''
def workflowdata(pviguid, title, senddate, workitemListJson):
    if senddate:
        senddate = re.sub('[^0-9 | \/ | :]', '', senddate)
    else:
        senddate = ''
    workflow = {}
    workflow['rowguid'] = str(uuid.uuid1())
    workflow['processVersionInstanceGuid'] = pviguid
    workflow['processVersionInstanceName'] = title
    workflow['processVersionGuid'] = ''
    workflow['initiatorname'] = ''
    workflow['startDate'] = senddate
    workflow['endTime'] = ''
    workflow['terminateDate'] = ''
    workflow['status'] = 0
    workflow['tag'] = '2'
    workflow['note'] = ''
    workflow['workitemjson'] = workitemListJson
    workflow['instancejson'] = ''
    workflow['defXml'] = ''
    workflow['operatedate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return workflow


'''
    插入工作流数据
'''
def insertWorkflowData(workflowData, __conn):
    sql = \
        '''
            insert into Workflow_PVI_SD_wd25(rowguid,processVersionInstanceGuid,processVersionInstanceName,processVersionGuid,			
                initiatorname,startDate,endTime,terminateDate,status,tag,note,workitemjson,instancejson,defXml) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%d,%s,%s,%s,%s,%s)
        '''
    params = (
    workflowData['rowguid'], workflowData['processVersionInstanceGuid'], workflowData['processVersionInstanceName'], \
    workflowData['processVersionGuid'], workflowData['initiatorname'], workflowData['startDate'],
    workflowData['endTime'], \
    workflowData['terminateDate'], workflowData['status'], workflowData['tag'], workflowData['note'], \
    workflowData['workitemjson'], workflowData['instancejson'], workflowData['defXml'])
    # print(sql % params)
    return __conn.mssql_exe_sql(sql, params)


'''
    workflow数据集，构建迁移数据模型，插入数据
'''
def workflowListData():
    sql = 'SELECT w1.UNID, w1.subject, w1.signdate FROM wd25_workflow w1'
    __conn1 = getConnect_old()
    # __conn2 = getConnect_new()
    cursors = __conn1.mssql_findList(sql)
    counter = 0
    start = time.time()
    for cursor in cursors:
        # print(cursor)
        workitemlist = workitemList(__conn1, cursor[0], cursor[1], cursor[2])
        workitemListJson = json.dumps(workitemlist)
        begin = time.time()
        workflowData = workflowdata(cursor[0], cursor[1], cursor[2], workitemListJson)
        # print(workflowData)
        if (insertWorkflowData(workflowData, __conn1)):
            counter += 1
            pass
        else:
            break
        end = time.time()
        if counter % 1000 == 0:
            __conn1.commitData()
        print('工作流数据已插入：%d, 用时为：%f' % (counter, end - begin))
    over = time.time()
    __conn1.commitData()
    print('总共插入：%d, 总用时：%f' % (counter, over - start))
    __conn1.closeConn()


##################################################### 附件处理 #######################################################
def handle_wd25Attach():
    __conn = getConnect_old()
    sql = 'SELECT DocUnid,Unid,attachnum,createdate,attachtitle FROM wd25_attach WHERE attachnum>0'
    results = __conn.mssql_findList(sql)
    counter = 0
    for record in results:
        attachInfo = {}
        CliengGuid = record[0]
        if CliengGuid:
            CliengGuid = re.sub('[^a-zA-Z | 0-9]', '', CliengGuid)
        attachInfo['CliengGuid'] = CliengGuid

        attachInfo['CliengTag'] = 'attach'

        attachInfo['StorageType'] = 'NasShareDirectory'

        attachNum = int(record[2])
        UploadDateTimeStr = '2018-12-20'
        attachInfo['UploadDateTime'] = UploadDateTimeStr

        uploadFilePath = 'E:\OA9Attach\\' + 'BigFileUpLoadStorage/temp/' + UploadDateTimeStr + '/' + CliengGuid + '/'
        attachInfo['FilePath'] = uploadFilePath

        attachTitleStr = str(record[4])
        if attachNum > 1:
            attachTitles = attachTitleStr.split(',')
            for attachName in attachTitles:
                attachInfo['AttachFileName'] = attachName
                attachInfo['ContentType'] = attachName[attachName.find('.'):len(attachName)]
                AttachGuid = str(uuid.uuid1())
                if AttachGuid:
                    AttachGuid = re.sub('[^a-zA-Z | 0-9]', '', AttachGuid)
                attachInfo['AttachGuid'] = AttachGuid

                attachInfo['AttachStorageGuid'] = CliengGuid
                if insertAttachInfo(attachInfo, __conn):
                    counter += 1
                    print('附件信息已经插入：%d 条' % counter)
        else:
            attachInfo['AttachFileName'] = attachTitleStr
            attachInfo['ContentType'] = attachTitleStr[attachTitleStr.find('.'):len(attachTitleStr)]
            AttachGuid = str(uuid.uuid1())
            if AttachGuid:
                AttachGuid = re.sub('[^a-zA-Z | 0-9]', '', AttachGuid)
            attachInfo['AttachGuid'] = AttachGuid

            attachInfo['AttachStorageGuid'] = CliengGuid
            if insertAttachInfo(attachInfo, __conn):
                counter += 1
                print('附件信息已经插入：%d 条' % counter)
        if counter % 1000 == 0:
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


'''
    插入附件信息
'''


def insertAttachInfo(attachInfo, __conn):
    sql = '''
        INSERT INTO frame_attachinfo(AttachGuid, AttachFileName, CliengGuid, CliengTag, UploadDateTime,
            ContentType, FilePath, AttachStorageGuid, StorageType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (attachInfo['AttachGuid'], attachInfo['AttachFileName'], attachInfo['CliengGuid'], attachInfo['CliengTag'],
              attachInfo['UploadDateTime'], attachInfo['ContentType'], attachInfo['FilePath'],
              attachInfo['AttachStorageGuid'],
              attachInfo['StorageType'])
    # print(sql%params)
    return __conn.mssql_exe_sql(sql, params)


##################################################### 流程意见信息处理 #######################################################
'''
    流程处理信息
'''
def getWorkflow(__conn):
    __sql = '''
        SELECT UNID,U_UNITNAME,U_UnitUser,U_UnitUserTitle,U_UnitEndTime FROM wd25_workflow_done
    '''
    return __conn.mssql_findList(__sql)


'''
    添加流程处理信息
'''
def insertWorkflowHandle(workflowhandle, __conn):
    __sql = '''
        INSERT INTO archive_handle(rowguid, archiveRowguid, archiveType, processversionInstanceGuid, 
            activityName, HandleUserGuid, handleUserName, isdone, donedate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    __params = (workflowhandle['rowguid'], workflowhandle['archiveRowguid'], workflowhandle['archiveType'],
                workflowhandle['processversionInstanceGuid'], workflowhandle['activityName'],
                workflowhandle['HandleUserGuid'],
                workflowhandle['handleUserName'], workflowhandle['isdone'], workflowhandle['donedate'])
    # print(__sql%__params)
    return __conn.mssql_exe_sql(__sql, __params)


'''
    流程处理信息
'''
def archiveHandle():
    __conn = getConnect_old()
    records = getWorkflow(__conn)
    counter = 0
    for record in records:
        workflowhandle = {}
        workflowhandle['rowguid'] = str(uuid.uuid1())
        workflowhandle['archiveRowguid'] = record[0]
        workflowhandle['archiveType'] = 'WD_25'
        workflowhandle['processversionInstanceGuid'] = record[0]
        workflowhandle['activityName'] = record[1]
        workflowhandle['HandleUserGuid'] = record[2]
        workflowhandle['handleUserName'] = record[3]
        workflowhandle['isdone'] = "1"
        if record[2] == '办理完毕':
            workflowhandle['isdone'] = "1"
        doneDate = record[4]
        if doneDate:
            doneDate = re.sub('[^0-9 | \/ | :]', '', doneDate)
        else:
            doneDate = ''
        workflowhandle['donedate'] = doneDate
        if insertWorkflowHandle(workflowhandle, __conn) > 0:
            counter += 1
            print('流程处理信息已经添加：%d 条' % counter)
        if counter % 1000 == 0:
            pass
            __conn.commitData()
    __conn.commitData()
    __conn.closeConn()


'''
    ###########################################处理步骤和意见的对应关系#############################
'''
#获取流程步骤信息
def getWorkflow(__conn, unid):
    __sql = '''
        SELECT UNID, U_UnitName, U_UnitUser, U_UnitUserTitle, U_UnitEndTime, U_UnitAction, U_UnitToTitle 
            FROM wd25_workflow_copy WHERE unid = '%s' 
    ''' % unid

    return __conn.mssql_findList(__sql)

#获取流程步骤审批意见信息
def getWorkflowOpinion(__conn, unid):
    __sql = '''
        SELECT opinionuser, opiniontime, OpinionBody FROM wd25_opinions WHERE parentunid = '%s'
    '''% unid
    return __conn.mssql_findList(__sql)

#处理流程步骤和意见信息
def handleWorkflowAndOpinion():
    __conn = getConnect_old()
    __sql = "SELECT DISTINCT unid FROM wd25_workflow_copy"
    unidRecords = __conn.mssql_findList(__sql)
    counter = 0
    for unidRecord in unidRecords:
        workflows = getWorkflow(__conn, unidRecord[0])
        opinions = getWorkflowOpinion(__conn, unidRecord[0])
        unituser = ''
        opinionuser = ''
        preUnittime = ''
        for workflow in workflows:
            #流程步骤信息
            workflowitem = {}
            workflowitem['UNID'] = workflow[0]
            workflowitem['U_UnitName'] = workflow[1]
            workflowitem['U_UnitUser'] = workflow[2]
            workflowitem['U_UnitUserTitle'] = workflow[3]
            workflowitem['U_UnitEndTime'] = workflow[4]
            workflowitem['U_UnitAction'] = workflow[5]
            workflowitem['U_UnitToTitle'] = workflow[6]
            unituser = workflow[2]
            unituser = str(unituser).replace("/SJGOV", "")
            unittime = workflow[4]
            opinionbody = ''
            #将时间转为数字（例：201801011012），作为比较
            if unittime:
                unittime = re.sub('[^0-9]', '', unittime)[:-2]
            if opinions:
                for opinion in opinions:
                    opinionuser = opinion[0]
                    opiniontime = opinion[1]
                    if opiniontime:
                        opiniontime = re.sub('[^0-9]', '', opiniontime)[:-2]
                    #流程步骤人和意见反馈人相同，则再判断时间
                    if unituser == opinionuser:
                        if opiniontime == unittime:
                            opinionbody = opinion[2]
                            # print("opinionBody1:", opinion[2])
                        elif len(preUnittime) > 0 and opiniontime < unittime and opiniontime > preUnittime:
                            opinionbody = opinion[2]
                            # print("opinionBody2:", opinion[2])
            workflowitem['opinionBody'] = opinionbody
            preUnittime = unittime
            if insertWorkflowItem(__conn, workflowitem):
                counter += 1
                print("已插入：%d 条数据。"% counter)
            if counter % 1000 == 0:
                __conn.commitData()
    __conn.commitData()
    __conn.closeConn()

#插入分析后的工作流数据
def insertWorkflowItem(__conn, workflowitem):
    __sql = '''
        INSERT INTO wd25_workflow_test(UNID, U_UnitName, U_UnitUser, U_UnitEndTime, U_UnitAction, U_UnitToTitle, 
            opinionBody, U_UnitUserTitle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (workflowitem['UNID'], workflowitem['U_UnitName'], workflowitem['U_UnitUser'], workflowitem['U_UnitEndTime'],
              workflowitem['U_UnitAction'], workflowitem['U_UnitToTitle'], workflowitem['opinionBody'],
              workflowitem['U_UnitUserTitle'])
    try:
        result = __conn.mssql_exe_sql(__sql, params)
    except Exception as e:
        print(__sql % params)
        print(e)
    return result

if __name__ == "__main__":
    # handle_wd25_workflow()

    #处理流程步骤信息
    workflowListData()
    # import_wd25()
    # handleOpinion()
    # handle_wd25Attach()
    # archiveHandle()
    # handleOpinons()
    # handleWorkflowAndOpinion()