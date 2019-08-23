# coding=utf-8
import codecs
import os
import pymssql
import sys
import uuid
from com.database.ConnectDataBase import ConnectionDatabase

# 设置默认编码
from xml.etree import ElementTree

import xlrd

'''
    数据库连接
'''
def getConnect_new():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "EpointOATest3")
    return __conn

def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa_old")
    return __conn

##########################################################
#############遍历目录，读取xml文件，导入附件信息
##########################################################

# 遍历指定目录
def eachfile(filepath, sql, outputfile, state, count, conn):
    pathdir = os.listdir(filepath)
    for dir in pathdir:
        child = os.path.join('%s\%s' % (filepath, dir))
        if os.path.isfile(child):
            if child.find("basicInfo") != -1:
                readfile(child, sql, outputfile, count, state, conn)
            continue
        eachfile(child, sql, outputfile, state, count, conn)


# 遍历结果
def readfile(filenames, sql, filepath, count, state, conn):
    with codecs.open(filenames, 'r', encoding='gbk') as fp:
        text = fp.read().replace('<?xml version="1.0" encoding="GBK"?>', '<?xml version="1.0" encoding="UTF-8"?>')

    element = ElementTree.fromstring(text.encode('utf-8'))

    for doc in element:
        # 定义参数
        clientguid = ""
        for key in doc.attrib:
            clientguid = doc.attrib[key]
            filepath += (clientguid + "/")
        for items in doc:
            # 定义参数
            attachguid = uuid.uuid1()
            attachname = ""
            contenttype = ""
            # 附件
            storagetype = "NasShareDirectory"
            # attachtag = "leaderApprove_feedback"
            attachtag = "wd25_attach"

            if parse_xml_node(items):
                attachname = parse_xml_node(items)

            if os.path.splitext(attachname)[-1]:
                contenttype = os.path.splitext(attachname)[-1]
            # 插入附件表
            params = (attachguid, attachname, contenttype, clientguid, attachtag, filepath, storagetype, clientguid)
            # 过滤参数为空的数据
            if params is None:
                continue
            # 执行sql语句
            try:
                effect = conn.mssql_exe_sql(sql, params)
                if effect:
                    count += 1
                    print("导入第" + str(count) + "条成功*********" + attachname)
                else:
                    print("sql语句执行失败")

            except Exception as e:
                print(e)
                print(sql%params)
                return


# 解析节点
def parse_xml_node(node):
    if len(node.getchildren()) == 0:
        return node.text if node.text is not None else ''
    else:
        node_dict = {}
        for child in node.getchildren():
            if child.tag in node_dict.keys():
                if not isinstance(node_dict[child.tag], list):
                    node_dict[child.tag] = [node_dict[child.tag]]
                node_dict[child.tag].append(parse_xml_node(child))
            else:
                node_dict[child.tag] = parse_xml_node(child)
        return node_dict

def handleFile():
    conn = getConnect_old()
    count = 0
    # 通知
    type="leaderApprove"
    # filenames = "F:\松江OA\OA数据解析\老OA数据\附件\领导批示反馈"
    filenames = "F:\松江OA\OA数据解析\收文数据\收文管理"
    oupputfile = "D:\OA9Attach\BigFileUpLoadStorage/wd25/"

    # 发文
    # type="fawen"
    # filenames = "E:\\work\\project\\2018\\importdata\\fawen\\BigFileUpLoadStorage"
    # oupputfile="D:\OA9Attach\BigFileUpLoadStorage/fawen/"

    sql = '''
        insert into Frame_AttachInfo_wd25(attachguid,attachfilename,contenttype,CliengGuid,CliengTag,filepath,storagetype,attachstorageguid) 
            values(%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    eachfile(filenames, sql, oupputfile, type, count, conn)

    # 关闭连接
    conn.commitData()
    conn.closeConn()


if __name__ == '__main__':
    handleFile()