#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

#获取当前路径
# print(os.getcwd())

# with open('pythondemo.txt', 'a', encoding='utf-8') as file:
#     print('文件已经创建')
#     file.write('文件已经创建好了')

#重命名文件
#os.rename('pythondemo.txt','python.txt')

#返回文件夹下的文件和文件夹
# print(os.listdir('E:\IdeaWorkspace\python_demo'))

#删除文件
# os.remove('python.txt')

#创建目录文件夹
# os.mkdir('study')

#删除文件夹
# os.rmdir('study')

#遍历创建多层级文件夹
# os.makedirs('study\demo')

#遍历删除多层级文件夹
# os.removedirs('study\demo')

#判断是否为文件
# print(os.path.isfile('study'))

#判断是否为文件夹
# print(os.path.isdir('study'))

#判断文件夹是否存在
# print(os.path.exists('study\demo'))

#返回路径中的文件和文件夹
print(os.path.split('study/test.txt'))