#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time

'''
  单线程  
'''
# def music(musicname):
#     for index in range(3):
#         print("准备播放：%s" % musicname)
#         print("正在播放：%s" % musicname)
#         # for j in range(5):
#         #     print("...")
#         #     time.sleep(0.1)
#         print("%s已经播放结束。" % musicname)
#     print(time.ctime())
#
#
# def movie(moviename):
#     for index in range(3):
#         print("准备播放：%s" % moviename)
#         print("正在播放：%s" % moviename)
#         # for j in range(5):
#         #     print("...")
#         #     time.sleep(0.1)
#         print("%s已经播放结束。" % moviename)
#     print(time.ctime())


'''
    单线程
'''
# if __name__ == '__main__':
#     music("一点点")
#     movie("肖生克的救赎")
#
#     print(time.time())

'''
    多线程
'''


def music(threadName, musicName):
    for index in range(3):
        print("线程%s准备播放：%s" % (threadName, musicName))
        print("线程%s正在播放：%s" % (threadName, musicName))
        for j in range(5):
            print("...", end="")
            time.sleep(0.1)
        print("")
        print("线程%s已经播放结束。" % threadName)
    print(time.ctime())


def movie(threadName, movieName):
    for index in range(3):
        print("线程%s准备播放：%s" % (threadName, movieName))
        print("线程%s正在播放：%s" % (threadName, movieName))
        for j in range(5):
            print("...")
            time.sleep(0.1)
        print("线程%s已经播放结束。" % threadName)
    print(time.ctime())


class myThread(threading.Thread):
    def __init__(self, threadName, threadId, funcName, arg):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.threadId = threadId
        self.funcName = funcName
        self.arg = arg

    def run(self):
        print('线程%s开始,其ID为:%s' % (self.threadName, self.threadId))
        if self.funcName == 'movie':
            movie(self.threadName, self.arg)
        if self.funcName == 'music':
            music(self.threadName, self.arg)
        print('线程%s执行%s方法结束' % (self.threadName, self.funcName))


if __name__ == '__main__':
    thread1 = myThread('thread1', '1', 'movie', '变形金刚')
    thread1.start()

    thread2 = myThread('thread2', '2', 'music', '花蝴蝶')
    thread2.start()

# exitFlag = 0
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开始线程：" + self.name)
#         print_time(self.name, self.counter, 5)
#         print ("退出线程：" + self.name)
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             threadName.exit()
#         time.sleep(delay)
#         print ("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
# if __name__ == '__main__':
#     # 创建新线程
#     thread1 = myThread(1, "Thread-1", 1)
#     thread2 = myThread(2, "Thread-2", 2)
#
#     # 开启新线程
#     thread1.start()
#     thread2.start()
