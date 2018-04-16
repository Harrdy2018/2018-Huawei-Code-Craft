#coding=utf-8
import random
import math
class E_model:
    def EMA(self,data,wilder,ratio):
        #Exponential Moving Average指数移动平均，适用于时间序列无明显的趋势变化
        #Y(t+1)=aX(t)+(1-a)Y(t)
        #a---平滑系数，加权因子,取值范围[0,1]
        #X(t)---时期t的实测值  Y(t)---时期t的预测值
        #初值的确定：取第一期的实际值为初值；取最初几期的平均值为初值
        n=len(data)
        if ratio==None:
            if wilder==False:
                ratio=float(2)/(n+1)
            else:
                ratio=float(1)/n
        predicted=[0]*n
        predicted[0]=int(round(average(data)))
        for i in range(1,n):
            predicted[i]=int(round(ratio*data[i-1]+(1-ratio)*predicted[i-1]))
        return ratio*data[-1]+(1-ratio)*predicted[-1]
    def DES(self,data,period):
        #二次指数平滑法
        ratio=ratio_for_ES(data,2,period)
        pre1=pre(data,ratio)
        pre2=pre(pre1,ratio)
        a=2*pre1[-1]-pre2[-1]
        b=float(ratio)*(pre1[-1]-pre2[-1])/(1-ratio)
        return a+b*period
    def TES(self,data,period):
        #三次指数平滑法
        ratio=ratio_for_ES(data,3,period)
        predicted1 = pre(data, ratio)
        predicted2 = pre(predicted1, ratio)
        predicted3 = pre(predicted2, ratio)
        a = 3 * predicted1[-1] - 3 * predicted2[-1] + predicted3[-1]
        b=float(ratio)*((6-5*ratio)*predicted1[-1]-2*(5-4*ratio)*predicted2[-1]+(4-3*ratio)*predicted3[-1]) / (1 - ratio) ** 2 / 2
        c = float(ratio) ** 2 * (predicted1[-1] - 2 * predicted2[-1] + predicted3[-1]) / (1 - ratio) ** 2 / 2
        return a+b *period+c*period**2

def WMA(data):
    #Weighted Moving Average加权移动平均
    n=len(data)
    pre=[]
    for N in range(1,n-1):
        predicted = list(data)  # 工厂函数，浅复制
        for i in range(N,n):
            predicted[i]=int(round((weighted_average(data[i-N:i:1]))))
        #print predicted
        pre.append(predicted)
    mse=[]
    for item in pre:
        mse.append(MSE(data,item))
    #对于此模型如何确定N,即一次移动多少即可
    N=mse.index(min(mse))+1
    return N
def SMA(data):
    #Simple Moving Average简单移动平均
    n=len(data)
    pre=[]
    for N in range(1,n-4):
        predicted = list(data)  # 工厂函数，浅复制
        for i in range(N,n):
            predicted[i]=int(round((average(data[i-N:i:1]))))
        pre.append(predicted)
    mse=[]
    for item in pre:
        mse.append(MSE(data,item))
    #对于此模型如何确定N,即一次移动多少即可
    N=mse.index(min(mse))+1
    return N
def weighted_average(data):
    #加权平均数
    N=len(data)
    sum=0
    for i in range(N):
        sum+=(i+1)*data[i]
    return float(sum)*2/(N*(N+1))
def average(data):
    sum=0
    for item in data:
        sum+=item
    return float(sum)/len(data)
def MSE(observed,predicted):
    #Mean Squared Error均方误差
    N=len(observed)
    mse=0
    for i in range(N):
        mse+=(observed[i]-predicted[i])**2
    mse=float(mse)/N
    return mse
def ratio_for_ES(data,times,period):
    '''
    根据MSE寻找二次指数平滑和三次指数平滑最好的平滑系数
    :param data: 实际观察值
    :param times: 二次指数或者三次指数
    :return: 最好的平滑系数
    '''
    def find_real_predicte(predicted,ratio,period):
        n=len(predicted)#n=2则为二次平滑
        N=len(predicted[0])
        real_predic=[0]*(N-1)
        if n==2:
            pre1=predicted[0]
            pre2=predicted[1]
            for i in range(N-1):
                a = 2*pre1[i]-pre2[i]
                b = float(ratio)*(pre1[i] - pre2[i])/(1 - ratio)
                real_predic[i]=a+b*period
        if n==3:
            pre1=predicted[0]
            pre2=predicted[1]
            pre3=predicted[2]
            for i in range(N-1):
                a=3 *pre1[i]-3*pre2[i]+pre3[i]
                b=float(ratio)*((6-5*ratio)*pre1[i]-2 *(5-4 * ratio)*pre2[i]+(4 - 3 * ratio)*pre3[i])/(1-ratio)**2/2
                c=float(ratio)**2*(pre1[i]-2*pre2[i] + pre3[i])/(1-ratio) ** 2/2
                real_predic[i]=a+b*period+c*period**2
        return real_predic
    mse = []
    for i in range(0,30, 1):
        predicted = []
        ratio = float(i) /30
        predicted.append(pre(data, ratio))
        for j in range(times-1):
            predicted.append(pre(predicted[j],ratio))
        mse.append(MSE(data[1::],find_real_predicte(predicted,ratio,period)))
    loca_mse= mse.index(min(mse))
    ratio = float(loca_mse)/30
    return ratio
def pre(data, ratio):
    '''
    S(t)=aY(t)+(1-a)S(t-1)
    适用于二次指数平滑和三次指数平滑
    :param data: 原始列表数据Y(t)
    :param ratio: 平滑系数a
    :return: S(t)
    '''
    n = len(data)
    predicted = [0] * (n + 1)
    predicted[0] = data[0]
    for i in range(0, n):
        predicted[i + 1] = ratio * data[i] + (1 - ratio) * predicted[i]
    predicted = predicted[1::1]
    return predicted
def main():
    flavor3=[2, 1, 2, 0, 3, 1, 3, 2, 0, 0, 4, 0, 3, 4, 1, 0, 0, 2, 2, 7, 2]
    flavor2=[0, 0, 2, 0, 2, 4, 2, 13, 0, 0, 0, 1, 0, 0, 1, 17, 6, 20, 9, 10, 4]
    flavor1=[0, 0, 0, 0, 0, 2, 1, 2, 1, 0, 1, 1, 4, 1, 0, 1, 3, 1, 5, 4, 3]
    print pre([1,2,3,4],0.5)
if __name__=="__main__":
    main()
