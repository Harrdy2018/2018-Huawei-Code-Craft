#coding=utf-8
#动态规划
def FindMax(vlist,wlist,totalWeight,totalLength):
    resArr=[]
    [resArr.append([0]*(totalWeight+1)) for i in range(totalLength+1)]
    for i in range(1,totalLength+1):
        for j in range(1,totalWeight+1):
            if wlist[i]<=j:
                resArr[i][j]= max(resArr[i - 1][j-wlist[i]]+ vlist[i], resArr[i-1][j])
            else:#第i个物品包装不进去
                resArr[i][j]= resArr[i-1][j]
    return resArr


def FindWhat(resArr,vlist,wlist,i,j):
    if i>=0:
        if resArr[i][j]==resArr[i-1][j]:
            item[i]=0
            FindWhat(resArr,vlist,wlist,i-1,j)
        elif j-wlist[i]>=0 and resArr[i][j]==resArr[i-1][j-wlist[i]]+vlist[i]:
            item[i]=1
            FindWhat(resArr,vlist,wlist,i-1,j-wlist[i])

if __name__=='__main__':
    v=[0,3,4,5,6]
    w=[0,2,3,4,5]
    weight=8
    n=4
    result=FindMax(v, w, weight, n)
    print result
    for ls in result:
        print ls
    item=[0]*5
    FindWhat(result,v,w,n,weight)
    print item
