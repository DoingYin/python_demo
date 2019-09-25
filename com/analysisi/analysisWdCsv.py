#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from com.analysisi.utils import Utils
from com.analysisi.utils import analysisWdCsvUtils
from com.analysisi.utils import analysisFileAttachUtils
from com.analysisi.utils import analysisDayScheduleUtils
from com.analysisi.utils import analysisLeaderApproveUtils
from com.analysisi.utils import analysisSupervisionExcutiveUtils

'''
    读取文件夹下的csv文件
'''
def readAllFiles(filePath):
    fileList = os.listdir(filePath)
    for file in fileList:
        path = os.path.join(filePath, file)
        if os.path.isfile(path):
            file = open(path, 'r', encoding='utf-8')
            print(path)
            if path.find(".csv") == -1:
                continue
            #流程记录信息
            if path.find("workflow") != -1:
                analysisWdCsvUtils.analysisWorkflowCsv(file)
                pass
            #意见信息
            elif path.find("opinion") != -1:
                analysisWdCsvUtils.analysisOpinionCsv(file)
                pass
            #发文数据
            elif path.find("wd_24") != -1:
                analysisWdCsvUtils.analysisWd24Csv(file)
                pass
            #收文数据
            elif path.find("wd_25") != -1:
                analysisWdCsvUtils.analysisWd25Csv(file)
                pass
            #通知反馈信息
            elif path.find("feedback") != -1:
                analysisWdCsvUtils.analysisNoticeFeedbackCsv(file)
                pass
            #通知信息
            elif path.find("notice") != -1:
                analysisWdCsvUtils.analysisNoticeCsv(file)
                pass
            # 领导日程信息
            elif path.find("schedule") != -1:
                analysisDayScheduleUtils.analysisDayScheduleCsv(file)
                pass
            # 领导批示件
            elif path.find("leaderApprove") != -1:
                analysisLeaderApproveUtils.analysisLeaderCsv(file)
                pass
            elif path.find("supervision") != -1:
                analysisSupervisionExcutiveUtils.analysisSupervisionExcutiveCsv(file)
                pass
        else:
            readAllFiles(path)

'''
    处理工作流数据
'''
def handleWorkflow():
    analysisWdCsvUtils.handle_workflow()

'''
    添加流程处理相关数据
'''
def handleArchiveHandleData(tag):
    analysisWdCsvUtils.addArchiveHandle(tag)

'''
    处理工作和意见信息
'''
def handleWorkflowAndOpinion():
    analysisWdCsvUtils.handleWorkflowAndOpinion()

'''
    封装流程处理信息
'''
def handleWorkflowListData(note):
    analysisWdCsvUtils.handleWorkflowListData(note)

'''
    附件处理
'''
def handleFile(inputForderName, outputForderName, tag):
    analysisFileAttachUtils.handleFile(inputForderName, outputForderName, tag)

'''
    处理领导批示件单位签收信息
'''
def handleSignInfo():
    analysisLeaderApproveUtils.handleSignInfo()

def handleSignInfo_done():
    analysisLeaderApproveUtils.handleSignInfo_done()

'''
    处理单位签收反馈数据
'''
def handleSignAndFeedback():
    analysisLeaderApproveUtils.handleSignFeedback()

'''
    处理领导批示件签收反馈数据
'''
def handleLeaderApproveSignAndFeedback():
    #处理领导批示件单位签收信息
    handleSignInfo()
    #处理领导批示件单位签收情况
    handleSignInfo_done()
    ##处理领导批示件单位签收和反馈情况
    handleSignAndFeedback()

global  testFilePath
testFilePath = "F:\松江OA\OA数据解析\单位数据\公文交换数据"
flag = "\收文"
flag = "\发文"
testFilePath = testFilePath + flag

global  outputForderName
outputForderName = "D:\OA9Attach\BigFileUpLoadStorage/"
if __name__ == "__main__":
    # testFilePath = "G:\数据解析\csv\workflowcsv"
    # testFilePath = "G:\数据解析\csv\wd25csv"
    # testFilePath = "G:\数据解析\csv\opinioncsv"
    # testFilePath = "F:\松江OA\OA数据解析\单位数据\薛涛\财政局\收文"
    #读取文件夹下的文件，将数据存储到数据库(读取收发文数据时，优先读取流程信息并处理)
    # print(Utils.getUnitBaseOuGUid())
    # if Utils.getUnitBaseOuGUid() == None:
    #     exit()
    readAllFiles(testFilePath)
    #处理流程步骤信息，将老数据的流程步骤信息解析为单个步骤的信息
    # handleWorkflow()
    #公文需要添加流程处理相关数据
    if testFilePath.find("收文") != -1:
        handleTag = 'wd_25'
    elif testFilePath.find("发文") != -1:
        handleTag = 'wd_24'
    else:
        exit()
    # handleArchiveHandleData(handleTag)
    #处理流程步骤对应的意见信息
    # handleWorkflowAndOpinion()
    #封装流程处理信息数据
    #工作流标识
    note = Utils.getFirst_alpha(testFilePath) +"_"+ handleTag
    # handleWorkflowListData(note)
    #处理附件，存储附件信息
    #文件解析路径
    inputForderName = "D:\各单位老数据1\oa导出数据\附件\直接发文"
    #文件存储路径
    # outputForderName = "D:\OA9Attach\BigFileUpLoadStorage/"
    # outputForderName = "D:\OA9Attach\BigFileUpLoadStorage/wd24"
    #附件标识
    # tag = "leaderApprove_formal"
    # tag = "leaderApprove_feedback"
    tag = "wd25"
    # handleFile(inputForderName, outputForderName, tag)