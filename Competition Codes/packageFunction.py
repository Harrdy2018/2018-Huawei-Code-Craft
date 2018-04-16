#coding=utf-8

def MultiplePackage(N,C,weight,value,num,physic):
    '''
    多重背包问题（每个物品都有次数限制）
    :param N: 预测的虚拟机种类，如N=pre_num
    :param C:输入文件是CPU，那么背包总容量就是MEM，如C=
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
                if f[i][j]<f[i-1][j-k*weight[i]]+k*value[i]<=physic:
                    #状态方程
                    f[i][j]=f[i-1][j-k*weight[i]]+k*value[i]
    return  f

def FindWhat(f,value,weight,i,j,item,num):
    if i>=0:
        if f[i][j]==f[i-1][j]:
            item[i]=0
            FindWhat(f,value,weight,i-1,j,item,num)
        elif j-weight[i]>=0:
            for k in range(num[i]+1):
                if f[i][j]==f[i-1][j-k*weight[i]]+k*value[i]:
                    item[i]=k
                    break
            FindWhat(f,value,weight,i-1,j-item[i]*weight[i],item,num)
