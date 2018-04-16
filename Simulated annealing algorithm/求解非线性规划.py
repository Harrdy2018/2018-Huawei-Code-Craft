'''
Metropolis准则(1953)—以概率接受新状态
若在温度T，当前状态i → 新状态j
若Ej<Ei，则接受 j 为当前状态；
否则，若概率 p=exp[-(Ej-Ei)/KT] 大于[0,1)区间的随机数，则仍接受状态 j 为当前状态；
若不成立，则保留状态 i 为当前状态。
p=exp[-(Ej-Ei)/KT]：在高温下，可接受与当前状态能量差较大的新状态；
在低温下，只接受与当前状态能量差较小的新状态。
'''
'''
求解非线性规划
min f(x)=x1^2+x2^2+8
st. x1^2-x2>=0
    -x1-x2^2+2=0
    x1>=0
    x2>=0
'''
import numpy as np
import math
start_sol_x2=0.5#指定x2的初始解
start_sol_x1=2-start_sol_x2**2
store_x1=start_sol_x1
store_x2=start_sol_x2
store_f=start_sol_x1**2+start_sol_x2**2+8

num=1000#退火次数
start_temp=90#初始温度
end_temp=20#结束温度
ratio=0.98#温度下降比例
info=[]

#numpy.random.random() Return random floats in the half-open interval [0.0, 1.0)
while(start_temp>=end_temp):
    for i in range(num):
        new_x2=store_x2+np.random.random()*0.2#产生随机扰动，新解产生
        new_x1= 2 - new_x2**2
        new_f=new_x1**2+new_x2**2+8
        dE=new_f-store_f
        if(new_x1**2-new_x2>=0 and -new_x1-new_x2**2+2==0 and new_x1>=0 and new_x2>=0):
            if(dE<0 or math.exp(-dE/start_temp)>np.random.random()):
                store_f=new_f
                store_x1=new_x1
                store_x2=new_x2
                info.append([store_x1,store_x2,store_f])
            else:
                continue
        else:
            continue
    start_temp=start_temp*ratio
print("结束温度：{}".format(start_temp))
for i in range(len(info)):
    print("第{0}次退火成功而且解在解空间数据，X1={1},X2={2},f(x)={3}".format(i,info[i][0],info[i][1],info[i][2]))
