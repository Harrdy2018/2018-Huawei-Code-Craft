#coding=utf-8
################################################################################################
#多重背包问题表示每个物品有不同的个数限制，如第i个物品的个数为num[i]
#f[i][j]表示前i件物品恰好放入一个容器为j的背包可以获得的最大价值，且每个物品数量不超过num[i]
#f[i][j]=max{f[i-1][j-k*weight[i]]+k*value[i]}其中0<=k<=min{j/weight[i],num[i]}
################################################################################################
def MultiplePackage(N,C,weight,value,num):
    '''
    多重背包问题（每个物品都有次数限制）
    :param N: 物品的个数，如N=5
    :param C:背包总容量，如C=15
    :param weight: 每个物品的容量数组表示，如weight=[0,5,4,7,2,6]
    :param value: 每个物品的价值数组表示，如value=[0,12,3,10,3,6]
    :param num:每个物品的个数限制，如num=[0,2,4,1,5,3]
    :return: 返回总价值矩阵
    '''
    #初始化f[N+1][C+1]为0，f[i][j]表示前i件物品恰好放入一个容器为j的背包可以获得的最大价值
    f=[[0 for col in range(C+1)] for row in range(N+1)]
    for i in range(1,N+1):
        for j in range(1,C+1):
            #对于物品i最多能取的次数是j/weight[i]与num[i]的较小者
            max_num_i=min(j/weight[i],num[i])
            #初始取k=0为最大，下面的循环是把取了k个物品i能获得的最大价值赋值给f[i][j]
            f[i][j]=f[i-1][j]
            for k in range(max_num_i+1):
                if f[i][j]<f[i-1][j-k*weight[i]]+k*value[i]:
                    #状态方程
                    f[i][j]=f[i-1][j-k*weight[i]]+k*value[i]
    return  f

def FindWhat(f,value,weight,i,j):
    if i>=0:
        if f[i][j]==f[i-1][j]:
            item[i]=0
            FindWhat(f,value,weight,i-1,j)
        elif j-weight[i]>=0:
            for k in range(num[i]+1):
                if f[i][j]==f[i-1][j-k*weight[i]]+k*value[i]:
                    item[i]=k
                    break
            FindWhat(f,value,weight,i-1,j-item[i]*weight[i])

N=5
C=15
weight=[0,5,4,7,2,6]
value=[0,12,3,10,3,6]
num=[0,2,4,1,5,3]
f=MultiplePackage(N,C,weight,value,num)
for row in f:
    print row
item=[0]*6
FindWhat(f,value,weight,N,C)
print item
