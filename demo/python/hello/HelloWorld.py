#-*-coding:utf8 _*_
print("Hello World!")
# 99乘法口诀
for num in range(1, 10):
    for i in range(1, num + 1):
        print(str(num) + '*' + str(i) + "=" + str(num * i), end=" ")
    print()

