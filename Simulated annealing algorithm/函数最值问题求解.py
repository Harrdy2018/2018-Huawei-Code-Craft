#  F(x)=6*x^7+8*x^6+7*x^3+5*x^2-y*x (0<=x<=100)
# 0<=x<=100,输入y,求F(x)的最小值
import math
import numpy as np
def f(x,y):
    result=6*math.pow(x,7)+8*math.pow(x,6)+7*math.pow(x,3)+5*math.pow(x,2)-y*x
    return result

start_T=100                  #初始化温度
end_T=1e-6                   #温度的下界
k=100                        #迭代的次数
ratio=0.99                   #温度的下降率
print("模拟退火算法\nF(x)=6*x^7+8*x^6+7*x^3+5*x^2-y*x (0<=x<=100)")
print("0<=x<=100,输入y,求F(x)的最小值")
y=eval(input("请输入参数y=>>>"))
start_x=0
store_x=start_x
store_f=f(start_x,y)
info=[]

while(start_T>=end_T):
    for i in range(k):
        new_x=start_x+np.random.random()
        new_f=f(new_x,y)
        dE=new_f-store_f
        if(new_x>=0 and new_x<=100):
            if(dE<0 or math.exp(-dE/start_T)>np.random.random()):
                store_x=new_x
                store_f=new_f
                info.append(store_f)
            else:
                continue
        else:
            continue
    start_T=start_T*ratio

print("结束温度：{}".format(start_T))
print("函数最小值：{}".format(min(info)))
