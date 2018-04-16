#coding=utf-8
#两个列表相乘相加
def list_multi(ls1,ls2):
    sum=0
    for i in range(len(ls1)):
        sum+=ls1[i]*ls2[i]
    return sum
#两个列表的减法
def list_sub(big,small):
    ls=[]
    for i in range(len(big)):
        ls.append(big[i]-small[i])
    return ls
#列表叠加处理
def list_add(ls):
    def sum(lista):
        sum=0
        for i in range(len(lista)):
            sum+=lista[i]
        return sum
    lsa=[]
    for i in range(len(ls)):
        lsa.append(sum(ls[0:i+1:1]))
    return lsa

def main():
    print list_add([1,2,3,4])
    print list_multi([0,0,0,1],[2,3,4,5])
if __name__=="__main__":
    main()

