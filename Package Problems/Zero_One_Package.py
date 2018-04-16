#coding=utf-8
######################################################################
#0-1背包问题表示每个物品只有取和不取的状态，即只能取0个或者1个
#f[i][j]表示前i件物品恰好放入一个容器为j的背包可以获得的最大价值
#f[i][j]=max{f[i-1][j],f[i][j-weight[i]]+value[i]}
######################################################################
def ZeroOnePackage(N,C,weight,value):
    '''
    0-1背包问题（每个物品只能取0或者1次）
    :param N: 物品的个数，如N=5
    :param C:背包总容量，如C=15
    :param weight: 每个物品的容量数组表示，如weight=[0,5,4,7,2,6]
    :param value: 每个物品的价值数组表示，如value=[0,12,3,10,3,6]
    :return: 返回总价值矩阵
    '''
    #初始化f[N+1][C+1]为0，f[i][j]表示前i件物品恰好放入一个容器为j的背包可以获得的最大价值
    f=[[0 for col in range(C+1)] for row in range(N+1)]
    for i in range(1,N+1):
        for j in range(1,C+1):
            if weight[i]<=j:
                f[i][j] = max(f[i - 1][j], f[i-1][j - weight[i]] + value[i])
            else:#总容量j小于物品i的容量时，直接不考虑物品i
                f[i][j] = f[i - 1][j]
    return f
N=5
C=15
weight=[0,5,4,7,2,6]
value=[0,12,3,10,3,6]
f=ZeroOnePackage(N,C,weight,value)
for row in f:
    print row
