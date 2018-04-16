#coding=utf-8
######################################################################
#完全背包问题表示每个物品可以取无限次
#f[i][j]表示前i件物品恰好放入一个容器为j的背包可以获得的最大价值
#f[i][j]=max{f[i-1][j-k*weight[i]]+k*value[i]}    0<=k<=j/weight[i]
######################################################################
def complete_package(N,C,weight,value):
    '''
    完全背包问题（每个物品可以取无限次）
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
            #注意由于weight,value数组下标从0开始，第i个物品的容量为weight[i]，价值为value[i]
            #C/weight[i]表示物品i最多可以取多少次
            f[i][j]=f[i-1][j]#初始取k=0为最大，下面的循环是把取了k个物品i能获得的最大价值赋值给f[i][j]
            for k in range(j/weight[i]+1):
                if f[i][j]<f[i-1][j-k*weight[i]]+k*value[i]:
                    f[i][j]=f[i-1][j-k*weight[i]]+k*value[i]#状态方程
    return f

N=5
C=15
weight=[0,5,4,7,2,6]
value=[0,12,3,10,3,6]
f=complete_package(N,C,weight,value)
for row in f:
    print row
