# -*- coding: utf-8 -*-

# student = {'name':'张三', 'age':"18", 'sex':"男"}
# print (student)
# print(student['name'])

# student = {'name':'张三', 'age':"18", 'sex':"男"}
# student['name'] = '李四'
# print(student)

# student = {'name':'张三', 'age':"18", 'sex':"男"}
# student['addr'] = "上海"
# print(student)

student = {'name':'张三', 'age':"18", 'sex':"男",'addr':'上海'}

#del
# del student['sex']
#删除字典
# del student
# print(student)

# student.clear()
# print(student)

# student = {'name':'张三', 'age':"18", 'sex':"男",'addr':'上海'}
# print(student.get('name'))
# #若获取的值不存在，则设为默认值
# print(student.get('addr','江苏'))

# student = {'name':'张三', 'age':"18", 'sex':"男",'addr':'上海'}
# student.keys()
# print(student.keys())

# student = {'name':'张三', 'age':"18", 'sex':"男",'addr':'上海'}
# student.values()
# print(student.values())

# student = {'name':'张三', 'age':"18", 'sex':"男",'addr':'上海'}
# student.items()
# print(student.items())

favorite_place = {'name':'张三','place':['addr1','park','rever']}
print(favorite_place)

favorite_place = {'张三':['addr1','park','rever'],'李四':['上海','杭州','苏州'],'王五':['南京','杭州','成都']}
print(favorite_place['李四'])