# for i in range(0,5):
#     print("我爱Python")
from cgitb import reset

# sum=0
# for i in range(101):
#     sum+=i;
# print( sum)

# listA=[10,20,30,40,50,55]
# for i in range(len(listA)):
#     print(listA[i])
#

nums = int(input("请输入数字："))
for i in range(1,10):
    result = nums * i
    print(f"{nums}x{i}={result}")
