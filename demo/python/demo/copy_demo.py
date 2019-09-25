# -*- coding: utf-8 -*-
import copy

a = ['1','2','3']
b = a

list1 = ['a','b','c','d']
list2 = copy.deepcopy(list1)

print(list2)

#通过id查看对象在内存中的位置
print(id(a))
print(id(b))

