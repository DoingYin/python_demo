# -*- coding: utf-8 -*-

list = ['jack','mack','mike','fake','tom','sam','alen']
#通过下标访问列表
print(list[1])


list = ['jack','mack','mike','fake',['tom','sam'],'alen']
#通过下标访问列表
print(list[4][0])

'''
列表是一个可变的类型数据，允许对列表里的数据进行修改
通过下标修改列表元素
'''
# list = ['jack','mack','mike','fake','tom','sam','alen']
# list[0] = 'Alen'
# print(list)

# list.append("walloce")
# print(list)

# list.insert(1,"walloce")
# print(list)

#删除最后一个元素
# list = ['jack','mack','mike','fake','tom','sam','alen']
# list.pop()
# print(list)

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# list1.pop(1)
# print(list1)

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# del list1[0]
# print(list1)

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# list1.remove('jack')
# print(list1)

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# name = 'jack'
# print(name in list1)
# print(name not in list1)

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# print(len(list1))

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# print(max(list1))
# print(min(list1))

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# print(list1.count('jack'))

# list1 = ['jack','mack','mike']
# list2 = ['tom','sam']
# list1.extend(list2)
# print(list1)

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# print(list1.index('mike'))

# list1 = ['jack','mack','mike','fake','tom','sam','alen']
# list1.reverse()
# print(list1)

list2 = [2,1,3,5,6,9,5]
list2.sort()
print(list2)