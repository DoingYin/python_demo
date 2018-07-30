# -*- coding: utf-8 -*-
# def functionname( parameters ):
#     "函数_文档字符串"
#     function_suite
#     return [expression]

# def name(username):
#     print('名字：'+username)
#
# def person(name,age):
#     print("name is %s and age is %s"%(name,age))
#     return age
# name('mike')
#
# person = person('tom',23)
# print(person)

# 带默认值的参数要放在右边
# def info(addr,name='mike'):
#     print("I'm %s and I'm from %s"%(name,addr))
#
# info('上海','tom')

# *args 是接收未命名的，不定长的参数，参数接收的是元组
# **args 是接收命名的不定长参数，参数接收的是字典
def info(addr, name, *args, **args1):
    print("I'm %s and I'm from %s" % (name, addr))
    print(args)
    print(args1)


# info('上海', 'tom', 'a', 'b', 'c')
# info('上海', 'mike', 'a', 'b', 'c', age='18', sex='男')


def ChangeInt(a):
    a = 10


b = 2
ChangeInt(b)


# print( b ) # 结果是 2

# 可写函数说明
def changeme(mylist):
    "修改传入的列表"
    mylist.append([1, 2, 3, 4])
    print("函数内取值: ", mylist)
    return


# 调用changeme函数
# mylist = [10,20,30]
# changeme( mylist )
# print ("函数外取值: ", mylist)

# lambda [参数] : 表达式 默认返回
# sum = lambda x,y: x+y
#
# print(sum(3,5))

# if表达式成立则返回左边的数，反之返回右边的数值
sum = lambda x, y: x if x > y else y

# 返回5
# print(sum(3, 5))
#
# dict = {'a': 1, 'c': 3, 'b': 2}
# print(dict.items())

'''
    reverse=True    从大到小倒序排序（默认为False）
    {k:v for k,v in dic}    字典推导式
    dict.items()    将字典转换为列表
'''
# dic = sorted(dict.items(), key = lambda item:item[1], reverse=True)
# print(dic)
# print({k:v for k,v in dic})

'''
    结果:
    [('c', 3), ('b', 2), ('a', 1)]
    {'c': 3, 'b': 2, 'a': 1}
'''

# list01 = [
#     {'name': 'mike', 'age': 19},
#     {'name': 'jone', 'age': 20},
#     {'name': 'alen', 'age': 17}
# ]
# list01 = sorted(list01, key=lambda item: item['age'], reverse=True)
# print(list01)
'''
    高阶函数
     map(func, seq[, seq[, seq...]) -> list
     filter(func, seq) -> list or tuple or string
     reduce(func, seq[, initvalue])
'''
# map
list01 = [1, 2, 3, 4, 5]
list02 = [2, 4, 6, 8, 10]
new_list0 = map(lambda x: x * 2, list01)
new_list1 = map(lambda x, y: x * y, list01, list02)
print(list(new_list0))  # 将map转为list

# filter
list01 = [1, 2, 3, 4, 5]
filter1 = filter(lambda x: x % 2 == 0, list01)
print(list(filter1))

# reduce
from functools import reduce

list01 = [1, 2, 3, 4, 5]
reduce1 = reduce(lambda x, y: x + y, list01)
print(reduce1)
