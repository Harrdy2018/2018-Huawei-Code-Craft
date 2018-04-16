#coding=utf-8
import datetime
def predicate_FName(st,flavor_name):
    return st.split('\t')[1].strip() in flavor_name
def ifilter_FName(predicate, iterable,flavor_name):
    iterable = iter(iterable)
    for x in iterable:
        if predicate(x,flavor_name):
            yield x
#提取给定数据文件全部数据信息
def extract_DataFile(ecs_lines,period,flavor_Name):
    #print flavor_Name #['flavor1', 'flavor2', 'flavor3']
    #print ecs_lines   #列表里面放字符串['56498c50-84e4\tflavor15\t2015-01-01 19:03:32\n'...]
    #print len(ecs_lines)
    #print period      #时间间隔这里是以7天为例，实际上时间不定
    s_time=ecs_lines[0].split('\t')[2].strip().split(' ')[0].split('-')
    e_time=ecs_lines[-1].split('\t')[2].strip().split(' ')[0].split('-')
    start_time=datetime.datetime(int(s_time[0]),int(s_time[1]),int(s_time[2]))
    end_time=datetime.datetime(int(e_time[0]),int(e_time[1]),int(e_time[2]))
    all_time= (end_time-start_time).days + 1  # 这个计算是要加1的，因为不是从0点开始，比如1号的9点到2号的9点就是两天
    all_seg = int(all_time/ period)
    #print start_time,end_time
    #print all_time,all_seg   #总共150天，以period天为一个段，分21段，不足的直接舍去

    # 把虚拟机名字和时间对应起来
    #print list(ifilter_FName(predicate_FName,ecs_lines,flavor_Name))
    dict_flavorN_to_Time = {}
    for f_Name in flavor_Name:
        store_time = []
        for item in ifilter_FName(predicate_FName,ecs_lines,flavor_Name):
            values = item.split("\t")  # 每一条的values  ['564bffbb-aa7c', 'flavor8', '2015-05-25 01:29:21\n']
            # print values
            if values[1] == f_Name:
                flavor_time = values[2].split(' ')[0].split('-')
                year = int(flavor_time[0])
                month = int(flavor_time[1])
                day = int(flavor_time[2])
                store_time.append([year, month, day])
            else:
                continue
        dict_flavorN_to_Time[f_Name] = store_time
    #print dict_flavorN_to_Time
    #for key in dict_flavorN_to_Time:
        #print key, dict_flavorN_to_Time[key]
    #把虚拟机的名字和每个时间段出现的次数对应起来
    dict_flavorN_to_Counttimes = {}
    for f_Name in flavor_Name:
        per_flavor_time = dict_flavorN_to_Time[f_Name]
        #print per_flavor_time#列表里面套列表[[2015, 2, 10], [2015, 2, 10]]
        length = len(per_flavor_time)
        count = [0] * all_seg
        for j in range(length):
            year = per_flavor_time[j][0]
            month = per_flavor_time[j][1]
            day = per_flavor_time[j][2]
            now_days = datetime.datetime(year, month, day)
            diff_days = (now_days-start_time).days + 1  # 解释同上
            unnecessary=all_time-period*all_seg
            if diff_days>=unnecessary:
                diff_days=diff_days-unnecessary
                if (diff_days <= period):
                    count[0] += 1
                # 能整除的天数比如14天，就应该放在第二段,也就是count[1]
                elif (diff_days > period and diff_days <= period * all_seg and diff_days % period == 0):
                    count[int(diff_days / period) - 1] = 1 + count[int(diff_days / period) - 1]
                elif (diff_days <= period * all_seg):
                    count[int(diff_days / period)] = 1 + count[int(diff_days / period)]
                else:
                    continue
        dict_flavorN_to_Counttimes[f_Name] = count
    #print dict_flavorN_to_Counttimes
    return dict_flavorN_to_Counttimes

#提取输入文件有关信息
def extract_InputFile(input_lines):
    #print input_lines

    #限制条件，物理服务器指标CPU MEM
    physic_server=[0]*2
    physic_server[0]=int(input_lines[0].split(' ')[0])
    physic_server[1]=int(input_lines[0].split(' ')[1])
    #print physic_server

    pre_num=int(input_lines[2].strip())#预测的虚拟机的个数
    #print pre_num             #5整数

    pre_class = []  # 预测的虚拟机的种类
    pre_class_CPU=[]#每个虚拟机的CPU信息
    pre_class_MEM=[]#每个虚拟机的MEM信息
    for i in range(pre_num):
        pre_class.append(input_lines[i + 3].split(' ')[0])
        pre_class_CPU.append(int(input_lines[i + 3].split(' ')[1]))
        pre_class_MEM.append(int(input_lines[i + 3].split(' ')[2].strip())/1024)

    distri_R=['CPU','MEM']#需要优化的资源维度名称（CPU或内存)
    #存放需要优化的资源维度名称
    distri_R_name=distri_R[0] if input_lines[pre_num+4].strip()==distri_R[0] else distri_R[1]
    #print distri_R_name       #CPU字符串

    #时间提取，预测时间多少天为一段
    pre_start_T_str = input_lines[6+pre_num].split(' ')[0].split('-')
    pre_end_T_str=input_lines[7+pre_num].split(' ')[0].split('-')
    start_T=datetime.datetime(int(pre_start_T_str[0]),int(pre_start_T_str[1]),int(pre_start_T_str[2]))
    end_T=datetime.datetime(int(pre_end_T_str[0]),int(pre_end_T_str[1]),int(pre_end_T_str[2]))
    period=(end_T-start_T).days
    #print pre_start_T_str    #['2015', '05', '31']
    #print pre_end_T_str      #['2015', '06', '07']
    #print period             #7每一天是从零点开始的，直接相减就是天数，不需要加1
    return physic_server,pre_num,pre_class,pre_class_CPU,pre_class_MEM,distri_R_name,period
