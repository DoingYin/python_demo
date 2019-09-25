# -*- coding: utf-8 -*-

'''
    open('文件名'，'打开的模式')
    r：只读的方式打开，如果文件不存在会提示错误
    w：只写的方式打开，如果文件存在则覆盖，不存在则创建
    a：打开一个文件进行追加内容，如果存在则打开，不存在则创建新文件

    r+：读写，会将文件指针调到文件的头部
    w+：读写，文件不存在直接创建，存在则覆盖源文件
    a+：追加读写，会将文件的指针调到文件的尾部
'''

'''
    文件的读取
'''
# 打开文件
# file = open('pythondemo.txt', 'r', encoding='utf-8')
# print(file)
#
# # 文件读写操作
# content = file.read(5)
# print(content)
#
# # 文件关闭
# file.close()

'''
    with open as filename
    with关键字会使python会在不需要的时候自动关闭
'''
# with open('pythondemo.txt', 'r', encoding='utf-8') as file:
#     content = file.read()
#     print(content)


'''
    readlines
    可以按照行的方式把整个文件中的内容进行一次性读取，并且返回的是一个列表，其中每一行的数据为一个元素。
'''
# file = open('pythondemo.txt', 'r', encoding='utf-8')
# print(file)
#
# # 文件读写操作
# content = file.readlines()
# print(content)
#
# # 文件关闭
# file.close()

'''
    逐行读取文件内容
'''
# file = open('pythondemo.txt', 'r', encoding='utf-8')
# i = 1
# for line in file:
#     print('这是第%s行内容：%s' % (i, line))
#     i += 1
# file.close()

'''
    写入文件
    write()
    a:追加内容
    w:覆盖添加新内容
'''
#w:覆盖添加新的内容
# with open('pythondemo.txt', 'w', encoding='utf-8') as file:
#     content = file.write('I am programer!')
#     print(content)  #返回的是成功写入的字符串长度

#a:追加新的内容
with open('pythondemo.txt', 'a', encoding='utf-8') as file:
    content = file.write('\nprogram is vary intersting!')
    print(content)
