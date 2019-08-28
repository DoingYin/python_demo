#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

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

if __name__ == "__main__":
    # testFilePath = "G:\数据解析\csv\workflowcsv"
    testFilePath = "G:\数据解析\csv\wd25csv"
    testFilePath = "G:\数据解析\csv\opinioncsv"
    testFilePath = "F:\松江OA\OA数据解析\区府办导出数据\常务会议督查\export\ow"
    #读取文件夹下的文件，将数据存储到数据库(读取收发文数据时，优先读取流程信息并处理)
    # readAllFiles(testFilePath)
    #处理流程步骤信息，将老数据的流程步骤信息解析为单个步骤的信息
    # handleWorkflow()
    #处理流程步骤对应的意见信息
    # handleWorkflowAndOpinion()
    #封装流程处理信息数据
    #工作流标识
    note = "supervision_excutive"
    handleWorkflowListData(note)
    #处理附件，存储附件信息
    #文件解析路径
    inputForderName = "F:\松江OA\OA数据解析\区府办导出数据\区府办各模块附件\领导批示反馈"
    #文件存储路径
    outputForderName = "D:\OA9Attach\BigFileUpLoadStorage/leaderApprove/feedback/"
    # outputForderName = "D:\OA9Attach\BigFileUpLoadStorage/wd24"
    #附件标识
    # tag = "leaderApprove_formal"
    tag = "leaderApprove_feedback"
    # tag = "wd24"
    # handleFile(inputForderName, outputForderName, tag)