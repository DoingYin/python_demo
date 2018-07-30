#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    语法：
        try:
            <语句>
        except <异常类型1><, 异常参数名1>:
            <异常处理代码1>
        except <异常类型2><, 异常参数名2>:
            <异常处理代码2>
        else:
            <没有异常时的处理代码>
        finally:
            <不管是否有异常，最终都会执行的代码>
'''

import sys

#异常操作
# try:
#     f = open('myfile.txt','r',encoding='utf-8')
#     s = f.readline()
#     i = int(s.strip())
# except OSError as err:
#     print("OS error: {0}".format(err))
# except ValueError:
#     print("Could not convert data to an integer.")
# except FileNotFoundError:
#     print("Unexpected error:", sys.exc_info()[0])
#     raise
# else:
#     print('没有异常会执行的异常')
# finally:
#     print('最后执行的代码块')
try:
    file = open('pythondemo.txt','r',encoding='utf-8')
    file.write('测试数据写入，行不行？')
except FileNotFoundError as e1:
    print(e1)
    print('请检查要打开的文件名，没有找到对应的文件')
except Exception as e:
    print(e)
    print('数据写入失败！')
else:
    print('数据写入文件成功！')
finally:
    if 'file' in locals():
        file.close()
        print('关闭文件！')
    print('没有取到对应的文件，不需要关闭！')
