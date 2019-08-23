#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import codecs
import uuid
from os import stat

from xml.etree import ElementTree
from com.database.ConnectDataBase import ConnectionDatabase

'''
    连接数据库
'''
def getConnect_old():
    __conn = ConnectionDatabase("localhost", "sa", "11111", "oa9History")
    return __conn

'''
    遍历指定目录下的文件
'''
def eachfile(filepath, outputfile, tag, conn):
    pathdir = os.listdir(filepath)
    counter = 0
    for dir in pathdir:
        child = os.path.join('%s\%s' % (filepath, dir))
        if os.path.isfile(child):
            if child.find("basicInfo") != -1:
                counter =readfile(child, outputfile, tag, conn)
            continue
        counter += eachfile(child, outputfile, tag, conn)
    return counter

'''
    解析文件夹下的xml附件信息
'''
def readfile(filenames, filepath, tag, __conn):
    counter = 0
    with codecs.open(filenames, 'r', encoding='gbk') as fp:
        text = fp.read().replace('<?xml version="1.0" encoding="GBK"?>', '<?xml version="1.0" encoding="UTF-8"?>')

    # 设置默认编码
    element = ElementTree.fromstring(text.encode('utf-8'))

    #遍历文件中的信息
    flag = 0
    for doc in element:
        # 定义参数
        clientguid = ""
        for key in doc.attrib:
            clientguid = doc.attrib[key]
            filepath += (clientguid + "/")
        for items in doc:
            # 定义参数
            attachinfo = {}

            #文件存储路径
            attachinfo['filepath'] = filepath

            #文件主键
            attachguid = uuid.uuid1()
            attachinfo['attachguid'] = attachguid

            #文件名
            attachname = ""
            if parse_xml_node(items):
                attachname = parse_xml_node(items)
            attachinfo['attachname'] = attachname

            #文件信息
            statinfo = getFileInfo(filenames.replace("basicInfo.xml", attachname))
            attachinfo['AttachLength'] = statinfo.st_size

            #附件类别
            contenttype = ""
            if os.path.splitext(attachname)[-1]:
                contenttype = os.path.splitext(attachname)[-1]
            attachinfo['contenttype'] = contenttype

            # 附件存储类型
            storagetype = "NasShareDirectory"
            attachinfo['storagetype'] = storagetype

            #附件标识
            attachtag = "attach"
            for key in items.attrib:
                if key == "name":
                    if items.attrib[key] == "正文" and flag == 0:
                        attachtag = "formal"
                        flag = 1
            attachinfo['attachtag'] = attachtag

            #关联的clientguid
            attachinfo['clientguid'] = clientguid

            #note
            attachinfo['note'] = "imported_"+ tag

            # 插入附件表
            if insertAttachData(__conn, attachinfo):
                counter += 1
        flag = 0
    return  counter


'''
    获取文件信息
    st_mode: inode 保护模式
    -File mode: file type and file mode bits (permissions).
    st_ino: inode 节点号。
    -Platform dependent, but if non-zero, uniquely identifies the file for a given value of st_dev.
    ——the inode number on Unix,
    ——the file index on Windows
    st_dev: inode 驻留的设备。
    -Identifier of the device on which this file resides.
    st_nlink:inode 的链接数。
    -Number of hard links.
    st_uid: 所有者的用户ID。
    -User identifier of the file owner.
    st_gid: 所有者的组ID。
    -Group identifier of the file owner.
    st_size:普通文件以字节为单位的大小；包含等待某些特殊文件的数据。
    -Size of the file in bytes, if it is a regular file or a symbolic link. The size of a symbolic link is the length of the pathname it contains, without a terminating null byte.
    st_atime: 上次访问的时间。
    -Time of most recent access expressed in seconds.
    st_mtime: 最后一次修改的时间。
    -Time of most recent content modification expressed in seconds.
    st_ctime:由操作系统报告的"ctime"。在某些系统上（如Unix）是最新的元数据更改的时间，在其它系统上（如Windows）是创建时间（详细信息参见平台的文档）。
    st_atime_ns
    -Time of most recent access expressed in nanoseconds as an integer
    st_mtime_ns
    -Time of most recent content modification expressed in nanoseconds as an integer.
    st_ctime_ns
    -Platform dependent:
    ——the time of most recent metadata change on Unix,
    ——the time of creation on Windows, expressed in nanoseconds as an integer.
'''
def getFileInfo(filepath):
    return stat(filepath)

'''
    解析的数据入库
'''
def insertAttachData(__conn, attachinfo):
    sql = '''
            insert into Frame_AttachInfo(
                attachguid,attachfilename,contenttype,CliengGuid,CliengTag, filepath, storagetype, attachstorageguid,
                note, AttachLength) values(%s,%s,%s,%s,%s,%s,%s,%s,%s, %d)
        '''
    # 插入附件表
    params = (attachinfo['attachguid'], attachinfo['attachname'], attachinfo['contenttype'],
              attachinfo['clientguid'], attachinfo['attachtag'], attachinfo['filepath'],
              attachinfo['storagetype'], attachinfo['clientguid'], attachinfo['note'],
              attachinfo['AttachLength'])
    # 执行sql语句
    try:
        effect = __conn.mssql_exe_sql(sql, params)
    except Exception as e:
        print(e)
        print(sql%params)
    return effect


'''
    解析节点
'''
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

'''
    附件处理
'''
def handleFile(inputForderName, outputForderName, tag):
    __conn = getConnect_old()
    # 通知
    type="leaderApprove"

    #读取文件的路径（需要遍历获取附件信息的路径）
    # filenames = "F:\松江OA\OA数据解析\老OA数据\附件\领导批示反馈"
    # filenames = "F:\松江OA\OA数据解析\老OA数据\附件\收文管理"
    # filenames = "F:\松江OA\OA数据解析\发文库和实例/fawen\BigFileUpLoadStorage"

    #文件存储的路径（用于系统中读取）
    # oupputfile = "D:\OA9Attach\BigFileUpLoadStorage/wd24/"

    #文件标识
    #正文
    # tag = "leaderApprove_formal"
    #反馈附件
    # tag = "wd24"

    counter = eachfile(inputForderName, outputForderName, tag, __conn)
    print("一共解析附件信息：%d 条。"%counter)

    # 关闭连接
    __conn.commitData()
    __conn.closeConn()