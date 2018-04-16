# coding=utf-8
import packageFunction
import extractFunction
import listFunction
import Models
def predict_vm(ecs_lines, input_lines):
    result=[]
    ######################################################################################################
    #提取输入文件基本信息，根据此信息写程序
    physic_server,pre_num, pre_class, pre_class_CPU,pre_class_MEM,distri_R_name, period=extractFunction.extract_InputFile(input_lines)
    #print physic_server#限制条件[2, 4]CPU<=2 and MEM<=4，注意物理服务器的规格有很多种
    #print pre_num#虚拟机有几种类型
    #print pre_class#['flavor1', 'flavor2', 'flavor3']
    #print pre_class_CPU#预测的虚拟机CPU[1, 1, 1]
    #print pre_class_MEM#预测的虚拟机MEM[1, 2, 4]
    #print distri_R_name#以谁为标注优化，另外一个就是约束，也就是背包容量
    #print period
    #####################################################################################################
    #data_list表示单纯的数值，字典是加了虚拟机索引的
    dict_flavorN_to_Counttimes = extractFunction.extract_DataFile(ecs_lines, period, pre_class)
    #return result
    per_pre_flavor = []  # 每一种预测虚拟机的数量
    for i in range(pre_num):
        ls= dict_flavorN_to_Counttimes[pre_class[i]]
        ls_a=[]
        for item in ls:
            if item>0:
                ls_a.append(item)
        #滤波处理
        ls_average=round(Models.average(ls_a))
        for i in range(len(ls)):
            if ls[i]>3*ls_average:
                ls[i]=3*ls_average
        #选择模型
        model=3
        if model==1:
            #SMA
            N=Models.SMA(ls)
            d=Models.average(ls[-1:-(N+1):-1])
            per_pre_flavor.append(int(round(1.109*d+0.65)))
        if model==2:
            #WMA
            N=Models.WMA(ls)
            d=Models.weighted_average(ls[-1:-(N+1):-1])
            per_pre_flavor.append(int(round(1.2*d+0.1)))
        if model==3:
            #EMA
            #如果开始不转整数False 1.5*d 75.758  True 1.6*d 73.777
            #如果转整False 1.64*d 76.957    ratio=0.8 1.33d 79.601
            #d=Models.EMA(ls,wilder=False,ratio=0.8)
            #d=int(round(d))
            #per_pre_flavor.append(int(round(1.33*d)))
            ls=listFunction.list_add(ls)
            d=Models.E_model().TES(ls,1)
            d=d-ls[-1]
            per_pre_flavor.append(int(round(d)))
    #print per_pre_flavor

    if (distri_R_name == 'CPU'):
        N = pre_num
        C = physic_server[1]
        weight = [0]
        weight.extend(pre_class_MEM)
        value = [0]
        value.extend(pre_class_CPU)
        num = [0]
        num.extend(per_pre_flavor)
        # print num
        physic = physic_server[0]
        info_physic = []
        info_item = []  # 所有背包的数组信息
        while num > [0] * (pre_num + 1):
            f = packageFunction.MultiplePackage(N, C, weight, value, num, physic)
            item = [0] * (pre_num + 1)
            packageFunction.FindWhat(f, value, weight, N, C, item, num)
            info_item.append(item)
            num = listFunction.list_sub(num, item)
        count_physic=len(info_item)

        if (count_physic >= 2 and listFunction.list_multi(info_item[-1][1::],pre_class_CPU) <0.3*physic_server[0]):  # 判断CPU利用率
            count_physic = count_physic - 1
            per_pre_flavor=listFunction.list_sub(per_pre_flavor, info_item[-1][1::])  # 减去不符合的虚拟机
        #print info_item, len(info_item)

        all_pre_flavorNum = 0
        for i in range(pre_num):
            all_pre_flavorNum += per_pre_flavor[i]
        result.append(str(all_pre_flavorNum))
        for i in range(pre_num):
            result.append(pre_class[i] + ' ' + str(per_pre_flavor[i]))
        result.append('')

        for i in range(0,count_physic):
            s = str(i+1)
            for b in range(len(info_item[i])):
                if info_item[i][b]> 0:
                    s += ' ' + pre_class[b - 1] + ' ' + str(info_item[i][b]) + ' '
                else:
                    continue
            info_physic.append(s.strip())
        #print info_physic
        #print count_physic
        result.append(str(count_physic))
        for info in info_physic:
            result.append(info)
    else:
        N = pre_num
        C = physic_server[0]
        weight = [0]
        weight.extend(pre_class_MEM)
        value = [0]
        value.extend(pre_class_CPU)
        num = [0]
        num.extend(per_pre_flavor)
        # print num
        physic = physic_server[1]
        info_physic = []
        info_item=[]#所有背包的数组信息
        while num > [0] * (pre_num + 1):
            f = packageFunction.MultiplePackage(N, C, value, weight, num, physic)
            item = [0] * (pre_num + 1)
            packageFunction.FindWhat(f, weight, value, N, C, item, num)
            info_item.append(item)
            num = listFunction.list_sub(num, item)
        count_physic=len(info_item)

        if(count_physic>=2 and listFunction.list_multi(info_item[-1][1::],pre_class_MEM)<0.3*physic_server[1]):#判断MEM利用率
            count_physic=count_physic-1
            per_pre_flavor=listFunction.list_sub(per_pre_flavor,info_item[-1][1::])#减去不符合的虚拟机
        #print info_item,len(info_item)

        all_pre_flavorNum = 0
        for i in range(pre_num):
            all_pre_flavorNum += per_pre_flavor[i]
        result.append(str(all_pre_flavorNum))
        for i in range(pre_num):
            result.append(pre_class[i] + ' ' + str(per_pre_flavor[i]))
        result.append('')

        for i in range(0,count_physic):
            s = str(i+1)
            for b in range(len(info_item[i])):
                if info_item[i][b]> 0:
                    s += ' ' + pre_class[b - 1] + ' ' + str(info_item[i][b]) + ' '
                else:
                    continue
            info_physic.append(s.strip())
        #print info_physic
        #print count_physic
        result.append(str(count_physic))
        for info in info_physic:
            result.append(info)
    return result
