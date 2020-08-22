# -*- coding: UTF-8 -*-

# def fitness(dis_cus_cus, dis_dep_cus, dis_sta_cus, min_dis_depot, time_win, tolerate_time_win, demand, lines,tons):
#     sudu = 1  #每辆车的速度
#     service_time = 0.25  #每个客户点的服务时间
#     chongdian = 0.5  #充电率
#     haodian = 1  #耗电率
#
#     fitness_value_c = [0 for i in range(len(lines))]
#     vehicle_num = [0 for i in range(len(min_dis_depot))]  # 每个depot需要的车辆数
#
#     for i in range(0, len(lines)):
#         r1 = 0  #一辆车访问的第一个顾客点
#         line = lines[i]
#         total_cus = len(lines[i])
#         for r2 in range(r1, total_cus):
#             total_demand = 0
#             n = line[r1]
#             total_dis = dis_dep_cus[n-1][1]
#             for j in range(r1, r2+1):
#                 node = line[j]
#                 total_demand += demand[node-1]
#                 total_dis += dis_cus_cus[]
#             if total_demand > tons or total_dis + :
#                 fitness_value_c[i] = fitness_value_c[i] + total_demand - tons
#                 path = line[r1:r2+1]
#                 L = len(path)
#
#                 #给第一点分配距离最近的depot，并求到达第一个点的时间
#                 node = path[0]
#                 depot_node = min_dis_depot[node-1][0]
#                 depot_dis = min_dis_depot[node-1][1]
#                 time = depot_dis / sudu
#                 vehicle_num[depot_node] += 1
#
#                 #到第一个点的时间窗
#                 shijinachuang = max(time_win[node][0] - time, 0) + max(time - time_win[node][1], 0)
#
#                 #求路线中达到每个点的时间和时间窗惩罚
#                 for n in range(0, L-1):
#                     time = time + service_time + dis_cus_cus

def fitness(dis_cus_cus, dis_sta_cus, min_dis_depot, min_dis_sta, time_win, tolerate_time_win, demand, lines):
    dianliang = 100  #电池容量
    haodian = 1  #耗电率
    zaizhong = 500  #载重
    chongdian_time = 0.6  #充电时间
    sudu = 40  #电动车的速度
    server_time = 0.5  #服务时间
    a = 0.2  #早到的单位惩罚成本
    b = 0.3  #晚到的单位惩罚成本
    M = float('inf')  #不满足可接受时间窗时的惩罚成本
    c1 = 300  #固定成本
    c2 = 3  #单位距离行驶成本

    fitness_value = [0 for i in range(len(lines))]
    AllCost = [0 for i in range(len(lines))]
    AllVechile = [0 for i in range(len(lines))]
    for i in range(0, len(lines)):
        line = lines[i]
        fore = line[0]  #当前访问的点
        depot_n = min_dis_depot[fore-1][0]  #从最近的depot出发

        carTon = demand[fore-1]  #当前车辆的载重
        carDis = min_dis_depot[fore-1][1]  #当前车辆行驶的总距离
        arriverTime = carDis / sudu  #车辆到达当前点的时间
        carTime = carDis / sudu + server_time
        cf_cost = a * max(time_win[fore-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore-1][1], 0)
        newTon = demand[fore-1]
        newDis = min_dis_depot[fore-1][1]
        # new_cf_cost = a * max(time_win[fore-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore-1][1], 0)
        totalDis = 0
        totalCost = 0

        r = 1       #表示当前需要车辆数

        #遍历每个客户点
        j = 1
        while j < len(line):
            #行驶的距离
            newDis = carDis + dis_cus_cus[fore-1][line[j]-1]

            #当前车辆的载重
            newTon = carTon + demand[line[j]-1]

            #当前车辆到达的时间点和离开的时间点
            arriverTime = carTime + dis_cus_cus[fore-1][line[j]-1] / sudu

            #如果到达j点的总行驶距离大于最大行驶距离，但是载重没有超过最大载重，就去到最近的充电站
            if newDis > dianliang/haodian and newTon <= zaizhong and tolerate_time_win[line[j]-1][0] <= arriverTime <= tolerate_time_win[line[j]-1][1]:
                sta_node = min_dis_sta[fore-1][0]  #寻找最近的充电站充电
                dis_cus2sta = min_dis_sta[fore-1][1]  #去最近的充电站的距离
                dis_sta2cus = dis_sta_cus[sta_node][line[j]-1]  #车辆继续从充电站配送到line[j]
                newDis = carDis + dis_cus2sta + dis_sta2cus  #车辆从当前点到充电站，再从充电站到line[j]的行驶距离
                arriverTime = carTime + (dis_cus2sta + dis_cus2sta) / sudu + chongdian_time  # 车辆从当前点到充电站,再从充电站到line[j]的到达时间

                #如果充电后到达line[j]的时间超过了其接受时间窗，从当前点返回最近的depot
                if arriverTime > tolerate_time_win[line[j]-1][1] or arriverTime < tolerate_time_win[line[j] -1][0]:
                    totalDis += carDis + min_dis_depot[fore - 1][1]
                    totalCost += cf_cost
                    depot_node = min_dis_depot[fore - 1][0]  #找到离当前点最近的depot
                    r += 1  #换一辆车配送line[j]
                    fore = line[j]  #当前配送客户点为line[j]
                    carTon = demand[fore-1]
                    carDis = min_dis_depot[fore-1][1]
                    arriverTime = carDis / sudu
                    carTime = arriverTime + server_time
                    cf_cost = a * max(time_win[fore - 1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore - 1][1], 0)
                else:
                    carDis = newDis
                    carTon = newTon
                    cf_cost += a * max(time_win[line[j]-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[line[j]-1][1], 0)
                    fore = line[j]

            #如果到达j点后的载重超过最大载重，就去最近的depot，换下一辆车
            elif newTon > zaizhong or arriverTime > tolerate_time_win[line[j]-1][1] or arriverTime < tolerate_time_win[line[j] -1][0]:
                totalDis += carDis + min_dis_depot[fore-1][1]
                totalCost += cf_cost
                depot_node = min_dis_depot[line[j]-1][0]  #找到未配送完成的离j点最近的depot
                r += 1  #换一辆车服务
                fore = line[j]
                carDis = min_dis_depot[fore-1][1]
                carTon = demand[fore-1]
                arriverTime = carDis / sudu
                carTime = carDis / sudu + server_time
                cf_cost = a * max(time_win[fore-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[fore-1][1], 0)
            else:
                carDis = newDis
                carTon = newTon
                carTime = arriverTime + server_time
                cf_cost += a * max(time_win[line[j]-1][0] - arriverTime, 0) + b * max(arriverTime - time_win[line[j]-1][1], 0)
                fore = line[j]
            j += 1

        #加上最后一辆车的距离和返程的距离
        totalDis += carDis + min_dis_depot[fore-1][1]

        # print "总行驶里程为: %.1fkm" %(totalDis)

        #目标函数，表示一个路径规划行驶的总距离的倒数越小越好
        Cost = (c1 * r + c2 * totalDis + totalCost)
        # print "总成本为: %.1f" % (Cost)
        # print "使用车辆数目：%d" % (r)

        result = 1 / Cost

        AllVechile[i] = r
        AllCost[i] = Cost
        fitness_value[i] = result

    return fitness_value, AllCost, AllVechile
