#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import re
from com.analysisi import analysisWdCsv

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
    # return subwebFlowOuGuid
    return getUnitBaseOuGUid()

#单位ouguid
def getUnitBaseOuGUid(filepath):
    # filepath = analysisWdCsv.testFilePath
    ouguid = None
    #财政局
    if filepath.find("财政局") != -1:
        ouguid = 'a8ed0362-2053-4f8e-a757-94c87db6f494'
    #泖港镇
    elif filepath.find("泖港镇") != -1:
        ouguid = 'aafb367b-e701-4649-b690-fa39febc05c2'
    #民政局
    elif filepath.find("民政局") != -1:
        ouguid = '0fe1d23f-dc1f-48c2-9e4b-291ba991aa57'
    #人保局
    elif filepath.find("人保局") != -1:
        ouguid = '68b0d9b7-9925-41b6-a016-e62a81ab2051'
    #卫计委
    elif filepath.find("卫生健康委") != -1:
        ouguid = '64912b40-1af6-4231-8ef2-4693fc457cb2'
    #文化旅游
    elif filepath.find("文化旅游") != -1:
        ouguid = '65b242b7-ae2e-45f1-9c74-66b9669a370b'
    #新浜镇
    elif filepath.find("新浜镇") != -1:
        ouguid = '023ccfa6-8a0b-429b-88c1-4b02009787e9'
    #新桥镇
    elif filepath.find("新桥镇") != -1:
        ouguid = '10a8b72a-c0c1-4df8-bbf4-d7fbcb50a993'
    #城管执法大队
    elif filepath.find("城管执法大队") != -1:
        ouguid = 'b985cfef-039f-497a-b33f-92fb6143bb3f'
    #中山街道
    elif filepath.find("中山街道") != -1:
        ouguid = 'ea789c06-6cf5-4de8-99d0-20c7c26be041'
    #环保局
    elif filepath.find("环保局") != -1:
        ouguid = 'f255ac0e-ace4-40e0-ad80-42d9ff93f91b'
    #交通委
    elif filepath.find("交通委") != -1:
        ouguid = '76adf758-19a4-47f6-9671-cdc0bbbe2e92'

    #教育局
    elif filepath.find("教育局") != -1:
        ouguid = '10bab3ad-525e-486f-a39f-aab60adee670'

    #科委
    elif filepath.find("科委") != -1:
        ouguid = '7d9406fe-2038-471d-8e6b-dc5c42dd2d4c'
    #审计局
    elif filepath.find("审计局") != -1:
        ouguid = '9c1ae5ec-ce63-4517-9036-20e74e4f94ab'
    #石湖荡
    elif filepath.find("石湖荡") != -1:
        ouguid = '534cdac9-fe95-4df9-9d49-9e2501fac3c6'
    #司法局
    elif filepath.find("司法局") != -1:
        ouguid = '34e5997e-8030-4b2d-9101-63f777de6793'
    #体育局
    elif filepath.find("体育局") != -1:
        ouguid = 'afe877cc-5085-42ef-a338-12463a989e5a'
    #统计局
    elif filepath.find("统计局") != -1:
        ouguid = '044f3592-bf5d-4f3f-8bab-f00145fb94e7'
    #应急管理
    elif filepath.find("应急管理") != -1:
        ouguid = '42f99f7d-bcc5-46aa-8db7-bdb8a22856c1'
    #总工会
    elif filepath.find("总工会") != -1:
        ouguid = '4ff42ebf-ecf0-43a0-a9fb-43c967aa62a7'
    #残联
    elif filepath.find("残联") != -1:
        ouguid = '174c520e-5457-45bd-83a2-a6a18a61f7b5'
    #档案局
    elif filepath.find("档案局") != -1:
        ouguid = '6b99288f-d518-41bc-93e5-6ab4a8179ec6'
    #发改委
    elif filepath.find("发改委") != -1:
        ouguid = '300dd97a-7046-43d7-b8e6-95a077c88344'
    #法制办
    elif filepath.find("法制办") != -1:
        ouguid = '0aab1975-dca9-4560-9013-c91d2884c0f9'
    #房管局
    elif filepath.find("房管局") != -1:
        ouguid = '2443785e-c49f-48e1-ab12-28688570dd7a'
    #规划资源
    elif filepath.find("规划资源") != -1:
        ouguid = '88e59eb4-808f-4880-838d-bccc23deb2ad'
    #合作交流
    elif filepath.find("合作交流") != -1:
        ouguid = 'edfed302-5e73-48c1-bd2b-5e54e6d62dfe'
    #红十字
    elif filepath.find("红十字") != -1:
        ouguid = '1de8d42f-87f3-460b-a880-d9e9fde6ec37'
    #机管局
    elif filepath.find("机管局") != -1:
        ouguid = 'e603253b-acb6-4f09-bcd9-62902b5c9324'
    #绿化市容局
    elif filepath.find("绿化市容局") != -1:
        ouguid = '6496d899-2fcc-40e9-abf8-b63903dede27'
    #民防办
    elif filepath.find("民防办") != -1:
        ouguid = '87fca859-078a-4d0d-9cb7-16ac748a9415'
    #民族宗教
    elif filepath.find("民族宗教") != -1:
        ouguid = 'ab4fe4bc-1482-4064-977e-f7f05b467cdf'
    #社治办
    elif filepath.find("社治办") != -1:
        ouguid = 'd604321a-1ced-42b1-a0be-41671a36162f'
    #史志办
    elif filepath.find("史志办") != -1:
        ouguid = '42b8e811-374a-4716-9bc4-475d3fa69159'
    #市场监督管理局
    elif filepath.find("市场监督管理局") != -1:
        ouguid = '947d6a40-93c8-4df6-aae4-886a956214e8'
    #水务局
    elif filepath.find("水务局") != -1:
        ouguid = '9273c08e-055f-4f85-b495-a17b01ef17c3'
    #台办
    elif filepath.find("台办") != -1:
        ouguid = '9273c08e-055f-4f85-b495-a17b01ef17c3'
    #外事办
    elif filepath.find("外事办") != -1:
        ouguid = '9273c08e-055f-4f85-b495-a17b01ef17c3'
    #信访办
    elif filepath.find("信访办") != -1:
        ouguid = '5b49ce13-f522-4a2c-8871-3136ec492506'
    #医保局
    elif filepath.find("医保局") != -1:
        ouguid = '7c2c4e5c-2772-4d47-93cc-1b3611c40107'
    #编办
    elif filepath.find("编办") != -1:
        ouguid = '8a5ee087-1523-421b-85a7-53f6e8ddf07f'
    #车墩镇
    elif filepath.find("车墩镇") != -1:
        ouguid = '7f3ef50e-5e5d-4e6f-9baf-7110eca2f4b3'
    #方松街道
    elif filepath.find("方松街道") != -1:
        ouguid = '5cde9b06-c448-45d4-a574-b29eef36937b'
    #广富林街道
    elif filepath.find("广富林街道") != -1:
        ouguid = '136c7291-b193-4c45-a69f-dd8530d32301'
    #国资委
    elif filepath.find("国资委") != -1:
        ouguid = 'd3406696-1693-4777-9fcb-9c3a4aec55b8'
    #建管委
    elif filepath.find("建管委") != -1:
        ouguid = '4085af80-cd26-4d2f-9888-d28138d5e077'
    #经济技术开发区
    elif filepath.find("经济技术开发区") != -1:
        ouguid = '84e9b93d-6dda-4a1a-b6c7-5903ca356a81'
    #经委
    elif filepath.find("经委") != -1:
        ouguid = '009c34f7-47d5-4686-9dd2-4bcaed74fb16'
    #农委
    elif filepath.find("农委") != -1:
        ouguid = 'df3f61c3-1be9-4d99-b6b1-9e0942c40aca'
    #气象局
    elif filepath.find("气象局") != -1:
        ouguid = 'f1faac6b-cb96-4e9d-bfd6-efe7a88cfb91'
    #侨办
    elif filepath.find("侨办") != -1:
        ouguid = '519fc137-8e79-414f-9859-5d54e98cc88f'
    #投促中心
    elif filepath.find("投促中心") != -1:
        ouguid = '6f468395-1b31-4fca-9d5a-48631154d54e'
    #文化执法大队
    elif filepath.find("文化执法大队") != -1:
        ouguid = '375e85be-ac3b-488a-b2be-d89330746709'
    #永丰街道
    elif filepath.find("永丰街道") != -1:
        ouguid = '46864edf-b632-443d-8429-0b1c05639bbb'
    #岳阳街道
    elif filepath.find("岳阳街道") != -1:
        ouguid = '88aab4bb-0bc7-43e5-a868-72674a1371ba'
    #政务服务中心
    elif filepath.find("政务服务中心") != -1:
        ouguid = '3a96ce47-2bf7-4837-b55e-8a42ab954ff3'
    #洞泾镇
    elif filepath.find("洞泾镇") != -1:
        ouguid = '55323fc2-12bc-4ebe-9c92-4c2753096401'
    #公安局
    elif filepath.find("公安局") != -1:
        ouguid = '7b10c1e1-76c6-4d13-a6ef-449d71d0d670'
    #九里亭街道
    elif filepath.find("九里亭街道") != -1:
        ouguid = '2471a143-2100-4163-9dea-eba6239c95c6'
    #九亭镇
    elif filepath.find("九亭镇") != -1:
        ouguid = 'd89b1059-e251-477f-8b63-5d2c0c88c71c'
    #佘山镇
    elif filepath.find("佘山镇") != -1:
        ouguid = '3779a024-ba58-4df4-9df2-334f34b4baad'
    #泗泾镇
    elif filepath.find("泗泾镇") != -1:
        ouguid = '9ce2ddfe-0f43-4e51-b389-947e8bc5ae41'
    #小昆山镇
    elif filepath.find("小昆山镇") != -1:
        ouguid = '07bbc6e0-a661-45cd-bbee-7807e07b7988'
    #叶榭镇
    elif filepath.find("叶榭镇") != -1:
        ouguid = '196fd3ed-7732-4783-bd91-e64dac1b69b0'
    #人大
    elif filepath.find("人大") != -1:
        ouguid = 'a611e42e-eaf9-41db-8b99-ba9bac3ab385'
    #区府办
    elif filepath.find("人民政府") != -1:
        ouguid = 'c8e1f500-bfea-45f2-8342-a5d8071303cb'
    return ouguid


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

import pinyin

#输入路径
def getFirst_alpha(filePath):
    names = filePath.split("\\")
    name = names[len(names) - 2]
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")])

#输入name
def getFirst_alphaByName(name):
    return "".join([i[0] for i in pinyin.get(name, " ").split(" ")])

#获取文件标识
def getFileTag(filepath):
    tag = None
    if filepath.find("发文") != -1:
        tag = "wd24"
    elif filepath.find("收文") != -1:
        tag = "wd25"
    elif filepath.find("会议") != -1:
        tag = "meeting"
    return tag

#获取文件标识
def getFileTag_ch(filepath):
    tag = None
    if filepath.find("发文") != -1:
        tag = "发文管理"
    elif filepath.find("收文") != -1:
        tag = "收文管理"
    elif filepath.find("会议") != -1:
        tag = "会议通知"
    return tag

#获取输出路径
def getFileOutPutPath(unitname, tag):
    return analysisWdCsv.outputForderName + unitname + "/" + tag + "/"


if __name__ == "__main__":
    # formatStrToTime('2018/7/25 17:30')
    # linkStr = '<a href=/egov\Receival.nsf/0/C32D77BD14A4512C4825841C0023C56D?openDocument target=_blank>关于批准松江区2018年第42批次建设项目被征地
    # 员落实就业和社会保障方案的请示</a><br>'
    # print(handleRelateLink(linkStr))
    # testFilePath = "F:\松江OA\OA数据解析\单位数据\新浜镇\发文"
    # print(getFirst_alpha(testFilePath))
    print(getUnitBaseOuGUid())